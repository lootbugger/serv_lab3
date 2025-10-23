from .django_orm import (
    DjangoPatientRepository,
    DjangoDoctorRepository,
    DjangoAppointmentRepository,
    DjangoDepartmentRepository,
)


class RepositoryRegistry:
    def __init__(self):
        self.patients = DjangoPatientRepository()
        self.doctors = DjangoDoctorRepository()
        self.appointments = DjangoAppointmentRepository()
        self.departments = DjangoDepartmentRepository()


db_repository = RepositoryRegistry()
