from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # Ensure user field is unique
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    cancer_type = models.CharField(max_length=100, blank=True, null=True)
    treatment_status = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255, default='Unknown Doctor')  # Store doctor's name directly
    hospital_name = models.CharField(max_length=255)  # Store hospital name directly
    appointment_date = models.DateTimeField()
    reason_for_visit = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Scheduled')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment with {self.doctor_name} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
