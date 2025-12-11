from django.shortcuts import render, redirect, get_object_or_404
from repo_app.models import Doctor
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


API_BASE_URL = "http://127.0.0.1:8001/api"  # Порт 8001!
API_USER = "kar"  # Логін суперюзера на ПОРТУ 8001
API_PASS = "1234"  # Пароль суперюзера на ПОРТУ 8001


def api_employee_list(request):
    # Ініціалізуємо хелпер
    helper = NetworkHelper(API_BASE_URL, API_USER, API_PASS)

    error_message = None

    # --- ЛОГІКА ВИДАЛЕННЯ ---
    if request.method == "POST":
        # Отримуємо ID з прихованого поля форми
        emp_id = request.POST.get("employee_id")

        if emp_id:
            # Викликаємо метод DELETE нашого хелпера
            # 'employees' - це частина URL (endpoint) з router.register
            success = helper.delete_item("employees", emp_id)

            if success:
                return redirect("api_list")  # Перезавантажуємо сторінку
            else:
                error_message = "Не вдалося видалити об'єкт через API"

    # --- ЛОГІКА ВІДОБРАЖЕННЯ СПИСКУ ---
    # Отримуємо список працівників через API
    employees = helper.get_list("employees")

    context = {"employees": employees, "error_message": error_message}
    return render(request, "web_app/api_employee_list.html", context)


def api_position_list(request):
    helper = NetworkHelper(API_BASE_URL, API_USER, API_PASS)
    error_message = None

    # --- ВИДАЛЕННЯ ---
    if request.method == "POST":
        pos_id = request.POST.get("position_id")
        if pos_id:
            # Стукаємо на ендпоінт 'positions'
            success = helper.delete_item("positions", pos_id)
            if success:
                return redirect("api_positions")
            else:
                error_message = "Помилка видалення посади"

    # --- ОТРИМАННЯ СПИСКУ ---
    # Стукаємо на ендпоінт 'positions'
    positions = helper.get_list("positions")

    return render(
        request,
        "web_app/api_positions_list.html",
        {"positions": positions, "error_message": error_message},
    )
