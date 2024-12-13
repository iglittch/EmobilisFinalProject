from django.contrib import admin
from .models import Patient, Doctor, Hospital, Appointment

admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Appointment)
admin.site.register(Patient)
