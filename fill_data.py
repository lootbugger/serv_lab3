import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab3.settings")
django.setup()

from repo_app.models import (
    Patient,
    Department,
    Diagnosis,
    Doctor,
    Appointment,
    Encounter,
    Invoice,
    EncounterDiagnosis,
)


def create_fake_data():
    print("🧹 Очищення старих даних (опціонально)...")
    Invoice.objects.all().delete()
    Encounter.objects.all().delete()
    Appointment.objects.all().delete()

    print("🚀 Починаємо генерацію...")

    dept_names = ["Surgery", "Cardiology", "Pediatrics", "Neurology", "Therapy"]
    departments = []
    for name in dept_names:
        dept, _ = Department.objects.get_or_create(name=name)
        departments.append(dept)

    diagnoses_data = [
        ("A00", "Cholera"),
        ("J00", "Common Cold"),
        ("I10", "Hypertension"),
        ("E11", "Type 2 Diabetes"),
        ("S82", "Fracture of lower leg"),
    ]
    diagnoses = []
    for code, desc in diagnoses_data:
        diag, _ = Diagnosis.objects.get_or_create(
            code=code, defaults={"description": desc, "diagnosis_date": timezone.now()}
        )
        diagnoses.append(diag)

    doctors = []
    specialities = [
        "Surgeon",
        "Cardiologist",
        "Pediatrician",
        "Neurologist",
        "Therapist",
    ]
    for i in range(10):
        dept = random.choice(departments)
        doc, _ = Doctor.objects.get_or_create(
            name=f"Dr. House {i}",
            defaults={
                "email": f"doc{i}@hospital.com",
                "phone_number": f"555-00-{i}",
                "speciality": random.choice(specialities),
                "department": dept,
            },
        )
        doctors.append(doc)

    patients = []
    for i in range(20):
        pat, _ = Patient.objects.get_or_create(
            name=f"Patient {i}",
            defaults={"email": f"pat{i}@email.com", "phone_number": f"099-000-{i}"},
        )
        patients.append(pat)

    encounter_types = [
        "Initial consultation",
        "Follow-up",
        "Emergency",
        "Routine Checkup",
    ]

    for _ in range(150):
        pat = random.choice(patients)
        doc = random.choice(doctors)
        date = timezone.now() - timedelta(days=random.randint(0, 60))

        appt = Appointment.objects.create(patient=pat, doctor=doc, schedule_date=date)

        if random.random() > 0.1:
            enc = Encounter.objects.create(
                patient=pat,
                doctor=doc,
                type=random.choice(encounter_types),
                encounter_date=date + timedelta(hours=random.randint(1, 4)),
                appointment=appt,
            )

            rand_diag = random.choice(diagnoses)

            ed = EncounterDiagnosis(encounter=enc, diagnosis=rand_diag)
            EncounterDiagnosis.objects.bulk_create([ed], ignore_conflicts=True)

            Invoice.objects.create(
                encounter=enc,
                amount=random.randint(5, 50) * 100,
                invoice_date=enc.encounter_date + timedelta(minutes=30),
            )

    print("✅ Дані успішно згенеровано!")


if __name__ == "__main__":
    create_fake_data()
