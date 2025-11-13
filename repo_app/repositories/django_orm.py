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

    def update(self, pk: Any, data: dict) -> Optional[Patient]:
        try:
            patient = Patient.objects.get(pk=pk)
            for key, value in data.items():
                setattr(patient, key, value)
            patient.save()
            return patient
        except Patient.DoesNotExist:
            return None

    def delete(self, pk: Any) -> None:
        try:
            patient = Patient.objects.get(pk=pk)
            patient.delete()
        except Patient.DoesNotExist:
            pass


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

    def update(self, pk: Any, data: dict) -> Optional[Doctor]:
        try:
            doctor = Doctor.objects.get(pk=pk)

            for key, value in data.items():
                setattr(doctor, key, value)

            doctor.save()
            return doctor
        except Doctor.DoesNotExist:
            return None

    def delete(self, pk: Any) -> None:
        try:
            doctor = Doctor.objects.get(pk=pk)
            doctor.delete()
        except Doctor.DoesNotExist:
            pass


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

    def update(self, pk: Any, data: dict) -> Optional[Appointment]:
        try:
            appointment = Appointment.objects.get(pk=pk)
            for key, value in data.items():
                setattr(appointment, key, value)
            appointment.save()
            return appointment
        except Appointment.DoesNotExist:
            return None

    def delete(self, pk: Any) -> None:
        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.delete()
        except Appointment.DoesNotExist:
            pass


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

    def update(self, pk: Any, data: dict) -> Optional[Department]:
        try:
            department = Department.objects.get(pk=pk)
            for key, value in data.items():
                setattr(department, key, value)
            department.save()
            return department
        except Department.DoesNotExist:
            return None

    def delete(self, pk: Any) -> None:
        try:
            department = Department.objects.get(pk=pk)
            department.delete()
        except Department.DoesNotExist:
            pass
