import concurrent.futures
import time
from math import pi

import pandas as pd
import plotly.express as px
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category20c, Spectral6, Viridis10
from bokeh.plotting import figure
from bokeh.transform import cumsum, factor_cmap
from django.db import connection
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView

from repo_app.models import Diagnosis, Doctor, Encounter, Invoice
from repo_app.repositories.main import db_repository

from .forms import DoctorForm
from .NetworkHelper import NetworkHelper


def doctor_list(request):
    doctors = db_repository.doctors.get_all()
    return render(request, "web_app/doctor_list.html", {"doctors": doctors})


def doctor_detail(request, pk):
    doctor = db_repository.doctors.get_by_id(pk)
    return render(request, "web_app/doctor_detail.html", {"doctor": doctor})


def doctor_form(request, pk=None):
    if pk:
        doctor = get_object_or_404(Doctor, pk=pk)
        form = DoctorForm(request.POST or None, instance=doctor)
    else:
        form = DoctorForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("doctor_list")

    return render(request, "web_app/doctor_form.html", {"form": form})


def doctor_delete(request, pk):
    if request.method == "POST":
        db_repository.doctors.delete(pk)
        return redirect("doctor_list")


API_BASE_URL = "http://127.0.0.1:8001/api"
API_USER = "kar"
API_PASS = "1234"


def api_employee_list(request):
    helper = NetworkHelper(API_BASE_URL, API_USER, API_PASS)
    error_message = None

    if request.method == "POST":
        emp_id = request.POST.get("employee_id")
        if emp_id:
            success = helper.delete_item("employees", emp_id)
            if success:
                return redirect("api_list")
            else:
                error_message = "Не вдалося видалити об'єкт через API"

    employees = helper.get_list("employees")
    context = {"employees": employees, "error_message": error_message}
    return render(request, "web_app/api_employee_list.html", context)


def api_position_list(request):
    helper = NetworkHelper(API_BASE_URL, API_USER, API_PASS)
    error_message = None

    if request.method == "POST":
        pos_id = request.POST.get("position_id")
        if pos_id:
            success = helper.delete_item("positions", pos_id)
            if success:
                return redirect("api_positions")
            else:
                error_message = "Помилка видалення посади"

    positions = helper.get_list("positions")
    return render(
        request,
        "web_app/api_positions_list.html",
        {"positions": positions, "error_message": error_message},
    )


class MedicalAnalyticsAPI(APIView):
    """
    API для отримання агрегованих даних (6 складних запитів).
    Використовуємо прямий ORM, бо це складна аналітика.
    """

    def get(self, request):
        doctors_activity = (
            Doctor.objects.annotate(total_encounters=Count("encounter"))
            .values("name", "speciality", "total_encounters")
            .order_by("-total_encounters")
        )

        doctors_revenue = (
            Doctor.objects.annotate(total_money=Sum("encounter__invoice__amount"))
            .values("name", "total_money")
            .order_by("-total_money")
        )

        try:
            top_diagnoses = (
                Diagnosis.objects.annotate(cases_count=Count("encounters"))
                .values("code", "description", "cases_count")
                .order_by("-cases_count")[:5]
            )
        except Exception:
            top_diagnoses = []

        monthly_revenue = (
            Invoice.objects.annotate(month=TruncMonth("invoice_date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        dept_avg_check = (
            Invoice.objects.values("encounter__doctor__department__name")
            .annotate(avg_bill=Avg("amount"))
            .order_by("-avg_bill")
        )

        visit_types = (
            Encounter.objects.values("type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return Response(
            {
                "doctors_activity": list(doctors_activity),
                "doctors_revenue": list(doctors_revenue),
                "top_diagnoses": list(top_diagnoses),
                "monthly_revenue": list(monthly_revenue),
                "dept_avg_check": list(dept_avg_check),
                "visit_types": list(visit_types),
            }
        )


def analytics_dashboard(request):
    data = Invoice.objects.select_related(
        "encounter__doctor", "encounter__doctor__department"
    ).values(
        "amount",
        "invoice_date",
        "encounter__type",
        "encounter__doctor__name",
        "encounter__doctor__speciality",
        "encounter__doctor__department__name",
    )
    df = pd.DataFrame(data)

    diag_data = (
        Diagnosis.objects.annotate(count=Count("encounters"))
        .values("code", "description", "count")
        .order_by("-count")[:5]
    )
    df_diag = pd.DataFrame(diag_data)

    doc_data = (
        Doctor.objects.annotate(visit_count=Count("encounter"))
        .values("name", "visit_count")
        .order_by("-visit_count")[:10]
    )
    df_docs = pd.DataFrame(doc_data)

    if df.empty:
        return render(request, "web_app/dashboard.html", {"message": "Дані відсутні!"})

    df.rename(
        columns={
            "encounter__type": "visit_type",
            "encounter__doctor__name": "doctor",
            "encounter__doctor__speciality": "speciality",
            "encounter__doctor__department__name": "department",
        },
        inplace=True,
    )

    all_specs = sorted(df["speciality"].unique())
    selected_spec = request.GET.get("speciality")
    if selected_spec and selected_spec != "All":
        df = df[df["speciality"] == selected_spec]

    stats = {
        "total_revenue": df["amount"].sum(),
        "total_visits": len(df),
        "avg_check": round(df["amount"].mean(), 2) if not df.empty else 0,
        "max_check": df["amount"].max() if not df.empty else 0,
    }

    graphs = {}

    rev_dept = df.groupby("department")["amount"].sum().reset_index()
    fig1 = px.bar(
        rev_dept,
        x="department",
        y="amount",
        title="1. 💰 Виручка по департаментах",
        color="department",
    )
    graphs["chart1"] = fig1.to_html(full_html=False)

    vis_type = df["visit_type"].value_counts().reset_index()
    vis_type.columns = ["type", "count"]
    fig2 = px.pie(vis_type, values="count", names="type", title="2. 🏥 Типи візитів")
    graphs["chart2"] = fig2.to_html(full_html=False)

    df["day"] = pd.to_datetime(df["invoice_date"]).dt.date
    daily = df.groupby("day")["amount"].sum().reset_index()
    fig3 = px.line(
        daily, x="day", y="amount", title="3. 📈 Динаміка доходу", markers=True
    )
    graphs["chart3"] = fig3.to_html(full_html=False)

    if not df_diag.empty:
        fig4 = px.bar(
            df_diag,
            x="count",
            y="code",
            orientation="h",
            title="4. 🦠 Топ-5 Діагнозів",
            text="description",
            color="count",
        )
        graphs["chart4"] = fig4.to_html(full_html=False)

    if not df_docs.empty:
        fig5 = px.bar(
            df_docs,
            x="name",
            y="visit_count",
            title="5. 👨‍⚕️ Завантаженість лікарів (Візити)",
            color="visit_count",
        )
        graphs["chart5"] = fig5.to_html(full_html=False)

    avg_dept = df.groupby("department")["amount"].mean().reset_index()
    fig6 = px.bar(
        avg_dept,
        x="department",
        y="amount",
        title="6. 💳 Середній чек по відділеннях",
        color="amount",
    )
    graphs["chart6"] = fig6.to_html(full_html=False)

    return render(
        request,
        "web_app/dashboard.html",
        {
            "graphs": graphs,
            "stats": stats,
            "all_specs": all_specs,
            "selected_spec": selected_spec,
        },
    )


def analytics_dashboard_bokeh(request):
    data = Invoice.objects.select_related(
        "encounter__doctor", "encounter__doctor__department"
    ).values(
        "amount",
        "invoice_date",
        "encounter__type",
        "encounter__doctor__department__name",
        "encounter__doctor__speciality",
    )
    df = pd.DataFrame(data)

    diag_data = (
        Diagnosis.objects.annotate(count=Count("encounters"))
        .values("code", "count")
        .order_by("-count")[:5]
    )
    df_diag = pd.DataFrame(diag_data)

    doc_data = (
        Doctor.objects.annotate(visit_count=Count("encounter"))
        .values("name", "visit_count")
        .order_by("-visit_count")[:10]
    )
    df_docs = pd.DataFrame(doc_data)

    if df.empty:
        return render(
            request, "web_app/dashboard_bokeh.html", {"message": "Дані відсутні!"}
        )

    df.rename(
        columns={
            "encounter__type": "visit_type",
            "encounter__doctor__department__name": "department",
            "encounter__doctor__speciality": "speciality",
        },
        inplace=True,
    )

    all_specs = sorted(df["speciality"].unique())
    selected_spec = request.GET.get("speciality")
    if selected_spec and selected_spec != "All":
        df = df[df["speciality"] == selected_spec]

    stats = {
        "total_revenue": df["amount"].sum(),
        "total_visits": len(df),
        "avg_check": round(df["amount"].mean(), 2),
    }

    rev_dept = df.groupby("department")["amount"].sum().reset_index()
    source1 = ColumnDataSource(rev_dept)
    depts = rev_dept["department"].tolist()
    p1 = figure(
        x_range=depts,
        height=300,
        title="1. Виручка по департаментах",
        toolbar_location=None,
    )
    p1.vbar(
        x="department",
        top="amount",
        width=0.8,
        source=source1,
        fill_color=factor_cmap("department", palette=Spectral6, factors=depts),
    )
    p1.add_tools(HoverTool(tooltips=[("Сума", "@amount")]))

    vis_type = df["visit_type"].value_counts().reset_index()
    vis_type.columns = ["type", "count"]
    vis_type["angle"] = vis_type["count"] / vis_type["count"].sum() * 2 * pi
    vis_type["color"] = (
        Category20c[len(vis_type)] if len(vis_type) > 2 else ["#3182bd", "#6baed6"]
    )
    source2 = ColumnDataSource(vis_type)
    p2 = figure(
        height=300,
        title="2. Типи візитів",
        toolbar_location=None,
        tooltips="@type: @count",
        x_range=(-0.5, 1.0),
    )
    p2.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="type",
        source=source2,
    )
    p2.axis.visible = False

    df["day"] = pd.to_datetime(df["invoice_date"]).dt.date
    daily = df.groupby("day")["amount"].sum().reset_index()
    source3 = ColumnDataSource(daily)
    p3 = figure(x_axis_type="datetime", height=300, title="3. Динаміка доходу")
    p3.line(x="day", y="amount", line_width=2, source=source3, color="green")
    p3.add_tools(
        HoverTool(
            tooltips=[("Дата", "@day{%F}"), ("Сума", "@amount")],
            formatters={"@day": "datetime"},
        )
    )

    if not df_diag.empty:
        codes = df_diag["code"].tolist()
        source4 = ColumnDataSource(df_diag)
        p4 = figure(
            y_range=codes, height=300, title="4. Топ-5 Діагнозів", toolbar_location=None
        )
        p4.hbar(
            y="code", right="count", height=0.8, source=source4, fill_color="orange"
        )
        p4.add_tools(HoverTool(tooltips=[("Кількість", "@count")]))
    else:
        p4 = figure(title="Немає даних про діагнози")

    if not df_docs.empty:
        docs = df_docs["name"].tolist()
        source5 = ColumnDataSource(df_docs)
        p5 = figure(
            x_range=docs,
            height=300,
            title="5. Топ лікарів (Візити)",
            toolbar_location=None,
        )
        p5.vbar(
            x="name",
            top="visit_count",
            width=0.8,
            source=source5,
            fill_color=factor_cmap("name", palette=Viridis10, factors=docs),
        )
        p5.xaxis.major_label_orientation = 0.5
    else:
        p5 = figure(title="Немає даних про лікарів")

    avg_dept = df.groupby("department")["amount"].mean().reset_index()
    depts_avg = avg_dept["department"].tolist()
    source6 = ColumnDataSource(avg_dept)
    p6 = figure(x_range=depts_avg, height=300, title="6. Середній чек по відділеннях")
    p6.vbar(
        x="department", top="amount", width=0.8, source=source6, fill_color="purple"
    )
    p6.add_tools(HoverTool(tooltips=[("Середній чек", "@amount")]))

    script, divs = components(
        {
            "chart1": p1,
            "chart2": p2,
            "chart3": p3,
            "chart4": p4,
            "chart5": p5,
            "chart6": p6,
        },
        theme="light_minimal",
    )

    return render(
        request,
        "web_app/dashboard_bokeh.html",
        {
            "script": script,
            "divs": divs,
            "stats": stats,
            "all_specs": all_specs,
            "selected_spec": selected_spec,
        },
    )


def simulate_heavy_query(_):
    """
    Симуляція "важкого" запиту до БД.
    Аргумент _ не використовується, потрібен для map.
    """

    list(Invoice.objects.all().aggregate(total=Sum("amount")).values())

    connection.close()


def performance_dashboard(request):
    """
    Проводить експеримент і малює графік залежності часу від потоків.
    """
    n_requests = 200
    thread_options = [1, 2, 4, 8, 16]
    results = []

    for n_threads in thread_options:
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
            list(executor.map(simulate_heavy_query, range(n_requests)))

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        results.append(
            {
                "threads": n_threads,
                "time": duration,
                "speed_gain": 0,
            }
        )

    base_time = results[0]["time"]
    for res in results:
        if res["time"] > 0:
            res["speed_gain"] = round(base_time / res["time"], 2)
        else:
            res["speed_gain"] = 0

    df = pd.DataFrame(results)

    fig = px.line(
        df,
        x="threads",
        y="time",
        markers=True,
        title=f"⏱️ Час виконання {n_requests} запитів до БД",
        labels={"threads": "Кількість потоків", "time": "Час (сек)"},
    )

    fig.update_layout(xaxis=dict(tickmode="linear", tick0=1, dtick=1))

    graph_html = fig.to_html(full_html=False)

    return render(
        request,
        "web_app/performance.html",
        {"graph": graph_html, "results": results, "n_requests": n_requests},
    )
