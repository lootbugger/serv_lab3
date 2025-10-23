from django.test import TestCase
from repo_app.repositories.main import db_repository
import datetime


class RepositoryDemoTest(TestCase):
    def test_run_repository_demo(self):
        print("\n" + "=" * 70)
        print(" DEMONSTRATION START: Running Repository Test")
        print("=" * 70 + "\n")

        print("--- CREATING ENTITIES (ADD) ---")

        print("Adding Department...")
        dep_data = {"name": "Internal Medicine Department"}
        department_obj = db_repository.departments.add(dep_data)
        print(f"Created: {department_obj.name} (ID: {department_obj.id})")

        print("\nAdding Patient...")
        patient_data = {
            "name": "Makar Kuznetsov",
            "email": "makar@example.com",
            "phone_number": "0501234567",
        }
        patient_obj = db_repository.patients.add(patient_data)
        print(f"Created: {patient_obj.name} (ID: {patient_obj.id})")

        print("\nAdding Doctor...")
        doctor_data = {
            "name": "Dr. Ivan Petrenko",
            "email": "dr.petrenko@example.com",
            "phone_number": "0997654321",
            "speciality": "General Practitioner",
            "department": department_obj,
        }
        doctor_obj = db_repository.doctors.add(doctor_data)
        print(f"Created: {doctor_obj.name} (ID: {doctor_obj.id})")

        print("\nAdding Appointment...")
        appt_data = {
            "patient": patient_obj,
            "doctor": doctor_obj,
            "schedule_date": datetime.datetime(
                2025, 10, 30, 10, 0, tzinfo=datetime.timezone.utc
            ),
        }
        appt_obj = db_repository.appointments.add(appt_data)
        print(f"Created: {appt_obj} (ID: {appt_obj.id})")

        print("\n--- DATA SUCCESSFULLY ADDED (within transaction) ---")

        print("\n" + "=" * 70)
        print("--- READING ENTITIES (GET_ALL, GET_BY_ID) ---")

        print("\n[GET_ALL] List of all patients:")
        all_patients = db_repository.patients.get_all()
        for p in all_patients:
            print(f" > ID: {p.id}, Name: {p.name}")

            self.assertEqual(p.name, "Makar Kuznetsov")

        doctor_id_to_find = doctor_obj.id
        print(f"\n[GET_BY_ID] Finding Doctor with ID={doctor_id_to_find}:")
        found_doctor = db_repository.doctors.get_by_id(doctor_id_to_find)
        if found_doctor:
            print(f" > Found: {found_doctor.name}")
            print(f" > Department: {found_doctor.department.name}")
            self.assertEqual(found_doctor.speciality, "General Practitioner")
        else:
            print(" > Doctor not found.")

        print("\n[GET_ALL] List of all appointments:")
        all_appointments = db_repository.appointments.get_all()
        for appt in all_appointments:
            print(
                f" > ID: {appt.id}, Patient: {appt.patient.name}, Doctor: {appt.doctor.name}"
            )
            self.assertEqual(appt.patient.id, patient_obj.id)

        print("\n" + "=" * 70)
        print(" DEMONSTRATION FINISHED: Test will now roll back changes.")
        print("=" * 70 + "\n")
