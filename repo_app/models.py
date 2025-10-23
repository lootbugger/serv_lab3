from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    class Meta:
        db_table = "patient"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "department"

    def __str__(self):
        return self.name


class Diagnosis(models.Model):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    diagnosis_date = models.DateTimeField()

    class Meta:
        db_table = "diagnosis"

    def __str__(self):
        return f"{self.code} - {self.description}"


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)

    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    class Meta:
        db_table = "doctor"

    def __str__(self):
        return f"Dr. {self.name} ({self.speciality})"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    schedule_date = models.DateTimeField()

    class Meta:
        db_table = "appointment"

    def __str__(self):
        return f"Appt for {self.patient.name} with {self.doctor.name} on {self.schedule_date.strftime('%Y-%m-%d')}"


class Encounter(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    encounter_date = models.DateTimeField()

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        db_column="apointment_id",
        null=True,
        blank=True,
    )

    diagnoses = models.ManyToManyField(
        Diagnosis, through="EncounterDiagnosis", related_name="encounters"
    )

    class Meta:
        db_table = "encounter"

    def __str__(self):
        return f"Encounter {self.id} ({self.type}) for {self.patient.name}"


class Order(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    order_date = models.DateTimeField()

    class Meta:
        db_table = "order"

    def __str__(self):
        return f"Order {self.id} ({self.type}) for {self.encounter.id}"


class Invoice(models.Model):
    encounter = models.ForeignKey(
        Encounter, on_delete=models.CASCADE, null=True, blank=True
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.BigIntegerField()
    invoice_date = models.DateTimeField()

    class Meta:
        db_table = "invoice"

    def __str__(self):
        return f"Invoice {self.id} for {self.amount}"


class EncounterDiagnosis(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)

    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.PROTECT)

    class Meta:
        db_table = "encounter_diagnosis"

        unique_together = (("encounter", "diagnosis"),)

    def __str__(self):
        return f"{self.encounter} <-> {self.diagnosis}"
