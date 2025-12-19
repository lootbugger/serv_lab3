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
    path("dashboard/", views.analytics_dashboard, name="dashboard"),
    path("api/analytics/", views.MedicalAnalyticsAPI.as_view(), name="api_analytics"),
    path("dashboard-v2/", views.analytics_dashboard_bokeh, name="dashboard_v2"),
    path("performance/", views.performance_dashboard, name="performance"),
]
