from django.urls import path
from . import views
from .views import appointment_success 

urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('accounts/signup/', views.custom_signup, name='signup'),  
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('signup/redirect/', views.signup_redirect, name='signup_redirect'),
    path('signup/patient/', views.patient_signup, name='patient_signup'),  # Correct the duplicate
    path('signup/doctor/', views.signup_doctor, name='signup_doctor'),
    path('signup/hospital/', views.signup_hospital, name='signup_hospital'),
    path('patient/<int:patient_id>/', views.patient_profile, name='patient_profile'),
    path('patient/edit/<int:patient_id>/', views.patient_edit, name='patient_edit'),
    path('cancel-appointment/<int:id>/', views.cancel_appointment, name='cancel-appointment'),
    path('update-appointment/<int:id>/', views.update_appointment, name='update-appointment'),
    path('appointment/success/', appointment_success, name='appointment_success'),
    path('dashboard/patient/', views.patient_dashboard, name='patient-dashboard'),  # Corrected duplicate
    path('appointments/', views.patient_appointments, name='patient_appointments'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('doctor/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('hospital/<int:id>/', views.hospital_detail, name='hospital_detail'),
]
