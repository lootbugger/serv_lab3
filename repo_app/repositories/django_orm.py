from typing import Any, List, Optional

from repo_app.models import (
    Appointment,
    Department,
    Doctor,
    Patient,
)

from .base import AbstractRepository


class DjangoPatientRepository(AbstractRepository[Patient]):
    def get_all(self) -> List[Patient]:
        return Patient.objects.all()

    def get_by_id(self, pk: Any) -> Optional[Patient]:
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return None

    def add(self, data: dict) -> Patient:
        return Patient.objects.create(**data)


class DjangoDoctorRepository(AbstractRepository[Doctor]):
    def get_all(self) -> List[Doctor]:
        return Doctor.objects.select_related("department").all()

    def get_by_id(self, pk: Any) -> Optional[Doctor]:
        try:
            return Doctor.objects.select_related("department").get(pk=pk)
        except Doctor.DoesNotExist:
            return None

    def add(self, data: dict) -> Doctor:
        return Doctor.objects.create(**data)


class DjangoAppointmentRepository(AbstractRepository[Appointment]):
    def get_all(self) -> List[Appointment]:
        return Appointment.objects.select_related("patient", "doctor").all()

    def get_by_id(self, pk: Any) -> Optional[Appointment]:
        try:
            return Appointment.objects.select_related("patient", "doctor").get(pk=pk)
        except Appointment.DoesNotExist:
            return None

    def add(self, data: dict) -> Appointment:
        return Appointment.objects.create(**data)


class DjangoDepartmentRepository(AbstractRepository[Department]):
    def get_all(self) -> List[Department]:
        return Department.objects.all()

    def get_by_id(self, pk: Any) -> Optional[Department]:
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return None

    def add(self, data: dict) -> Department:
        return Department.objects.create(**data)
