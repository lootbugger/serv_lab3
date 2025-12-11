from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_list, name="doctor_list"),
    path("doctor/<int:pk>/", views.doctor_detail, name="doctor_detail"),
    path("doctor/new/", views.doctor_form, name="doctor_create"),
    path("doctor/<int:pk>/edit/", views.doctor_form, name="doctor_edit"),
    path("doctor/<int:pk>/delete/", views.doctor_delete, name="doctor_delete"),
    path("api_employee_list/", views.api_employee_list, name="api_employee_list"),
    path("api_positions_list/", views.api_position_list, name="api_position_list"),
]
