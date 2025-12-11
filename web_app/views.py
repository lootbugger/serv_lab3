from django.shortcuts import render, redirect, get_object_or_404
from repo_app.models import Doctor
from repo_app.repositories.main import db_repository
from .forms import DoctorForm


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

