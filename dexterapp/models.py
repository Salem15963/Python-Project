from django.db import models


# Create your models here.
class Doctor(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    phone=models.IntegerField(null=False)
    national_id=models.IntegerField(null=False)
    desc=models.TextField(null=False)
    role=models.CharField(max_length=255)
    create_at=models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now=True)

class Clinic(models.Model):
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=500)
    create_at=models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now=True)
    doctor_clinc=models.ForeignKey(Doctor, related_name="doctor",on_delete=models.CASCADE)

class Patient(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    national_id=models.IntegerField(null=False)
    gender=models.CharField(max_length=255)
    phone=models.IntegerField(null=False)
    email=models.EmailField(max_length=255)
    desc=models.TextField(null=False)
    date_of_birth=models.DateField(null=True)
    last_visit_date=models.DateField(null=True)
    allergies=models.TextField(null=True)
    create_at=models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now=True)
    clinic=models.ForeignKey(Clinic, related_name="clinic",on_delete=models.CASCADE)


class Appointment(models.Model):
    national_id=models.IntegerField(default = None)
    start_time=models.DateField()
    end_time=models.DateField()
    title=models.CharField(max_length=255)
    doctor_appoint=models.ForeignKey(Doctor, related_name="doctor_appoint",on_delete=models.CASCADE)
    patient_appoint=models.ForeignKey(Patient, related_name="patient_appoint",on_delete=models.CASCADE)
    create_at=models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now=True)

class Payment(models.Model):
    amount=models.IntegerField(null=True)
    date=models.DateField()
    method=models.CharField(max_length=255)
    doctor_payment=models.ForeignKey(Doctor, related_name="doctor_payment",on_delete=models.CASCADE)
    patient_payment=models.ForeignKey(Patient, related_name="patient_payment",on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
