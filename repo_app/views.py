from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


from .serializers import (
    PatientSerializer,
    DoctorSerializer,
    AppointmentSerializer,
    DepartmentSerializer,
)


from .repositories.main import db_repository


class PatientList(APIView):
    def get(self, request, format=None):
        patients = db_repository.patients.get_all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            new_patient = db_repository.patients.add(serializer.validated_data)
            return Response(
                PatientSerializer(new_patient).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):
    def get_object(self, pk):
        patient = db_repository.patients.get_by_id(pk)
        if patient is None:
            raise Http404
        return patient

    def get(self, request, pk, format=None):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            updated_patient = db_repository.patients.update(
                pk, serializer.validated_data
            )
            return Response(PatientSerializer(updated_patient).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.get_object(pk)
        db_repository.patients.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentList(APIView):
    def get(self, request, format=None):
        departments = db_repository.departments.get_all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            new_department = db_repository.departments.add(serializer.validated_data)
            return Response(
                DepartmentSerializer(new_department).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetail(APIView):
    def get_object(self, pk):
        department = db_repository.departments.get_by_id(pk)
        if department is None:
            raise Http404
        return department

    def get(self, request, pk, format=None):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            updated_department = db_repository.departments.update(
                pk, serializer.validated_data
            )
            return Response(DepartmentSerializer(updated_department).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.get_object(pk)
        db_repository.departments.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorList(APIView):
    def get(self, request, format=None):
        doctors = db_repository.doctors.get_all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            new_doctor = db_repository.doctors.add(serializer.validated_data)
            return Response(
                DoctorSerializer(new_doctor).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetail(APIView):
    def get_object(self, pk):
        doctor = db_repository.doctors.get_by_id(pk)
        if doctor is None:
            raise Http404
        return doctor

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            updated_doctor = db_repository.doctors.update(pk, serializer.validated_data)
            return Response(DoctorSerializer(updated_doctor).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.get_object(pk)
        db_repository.doctors.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentList(APIView):
    def get(self, request, format=None):
        appointments = db_repository.appointments.get_all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            new_appt = db_repository.appointments.add(serializer.validated_data)
            return Response(
                AppointmentSerializer(new_appt).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetail(APIView):
    def get_object(self, pk):
        appt = db_repository.appointments.get_by_id(pk)
        if appt is None:
            raise Http404
        return appt

    def get(self, request, pk, format=None):
        appt = self.get_object(pk)
        serializer = AppointmentSerializer(appt)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        appt = self.get_object(pk)
        serializer = AppointmentSerializer(appt, data=request.data, partial=True)
        if serializer.is_valid():
            updated_appt = db_repository.appointments.update(
                pk, serializer.validated_data
            )
            return Response(AppointmentSerializer(updated_appt).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.get_object(pk)
        db_repository.appointments.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
