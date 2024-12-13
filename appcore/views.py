from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
import logging
from .models import Patient, Doctor, Appointment, Hospital
from datetime import datetime

logger = logging.getLogger(__name__)

# Create your views here.

def landing_page(request):
    return render(request, 'landing.html')

@login_required
def patient_dashboard(request):
    # Hardcoded list of doctors with 'id' added
    doctors = [
        {'id': 1, 'name': 'Dr. John Smith', 'specialty': 'Cardiologist', 'hospital': 'City Hospital'},
        {'id': 2, 'name': 'Dr. Jane Doe', 'specialty': 'Dermatologist', 'hospital': 'Sunshine Clinic'},
        {'id': 3, 'name': 'Dr. Emily White', 'specialty': 'Neurologist', 'hospital': 'Greenwood Medical Center'},
        {'id': 4, 'name': 'Dr. Alex Brown', 'specialty': 'Orthopedic', 'hospital': 'City Hospital'},
    ]
    
    # Hardcoded list of hospitals with 'id' added
    hospitals = [
        {'id': 1, 'name': 'City Hospital', 'location': 'New York'},
        {'id': 2, 'name': 'Sunshine Clinic', 'location': 'Los Angeles'},
        {'id': 3, 'name': 'Greenwood Medical Center', 'location': 'Chicago'},
        {'id': 4, 'name': 'Mountainview Health', 'location': 'San Francisco'},
    ]
    
    doctor_search = request.GET.get('doctor_search', '')
    hospital_search = request.GET.get('hospital_search', '')

    try:
        doctor_id = int(request.GET.get('doctor_id', ''))
        hospital_id = int(request.GET.get('hospital_id', ''))
    except ValueError:
        doctor_id = None
        hospital_id = None
    
    # Filter doctors and hospitals based on search input
    if doctor_search:
        doctors = [doctor for doctor in doctors if doctor_search.lower() in doctor['name'].lower()]
    
    if hospital_search:
        hospitals = [hospital for hospital in hospitals if hospital_search.lower() in hospital['name'].lower()]

    try:
        patient = Patient.objects.get(email=request.user.email)
    except Patient.DoesNotExist:
        patient = None

    appointments = Appointment.objects.filter(patient=patient)

    # Handle the form submission for booking an appointment
    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        appointment_date = request.POST['appointment_date']
        reason_for_visit = request.POST['reason_for_visit']

        # Create the appointment
        doctor = next(doctor for doctor in doctors if doctor['id'] == int(doctor_id))  # Find the doctor by id
        appointment = Appointment(
            patient=patient,
            doctor_name=doctor['name'],
            appointment_date=datetime.strptime(appointment_date, '%Y-%m-%dT%H:%M'),
            reason_for_visit=reason_for_visit,
            status='Scheduled'  # Assuming default status is 'Scheduled'
        )
        appointment.save()

        # Redirect to the same page or show a success message
        return redirect('patient-dashboard')

    context = {
        'patient': patient,
        'appointments': appointments,
        'doctors': doctors,
        'hospitals': hospitals
    }
    
    return render(request, 'patient_dashboard.html', context)

@login_required
def doctor_dashboard(request):
    appointments = ["Appointment 1", "Appointment 2", "Appointment 3"]  # Sample data
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})

def hospital_dashboard(request):
    return render(request, 'hospital_dashboard.html')

def custom_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after sign-up
            role = request.POST.get('role')  # Role is included in the form

            if role == 'patient':
                # Explicitly ensure the user is logged in
                return redirect('patient-dashboard')
            elif role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('landing-page')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

def signup_redirect(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        if role == 'patient':
            return redirect('patient_signup') 
        elif role == 'doctor':
            return redirect('signup_doctor')
        elif role == 'hospital':
            return redirect('signup_hospital') 

    return render(request, 'signup.html')

def signup_patient(request):
    return render(request, 'signup_patient.html')

def signup_doctor(request):
    return render(request, 'signup_doctor.html')

def signup_hospital(request):
    return render(request, 'signup_hospital.html')
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
def patient_signup(request):
    if request.method == 'POST':
        # Extract data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        cancer_type = request.POST.get('cancer_type', '')  # Optional
        treatment_status = request.POST.get('treatment_status')
        emergency_contact = request.POST.get('emergency_contact')

        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('patient_signup')

        try:
            # Create a regular User account (not a superuser)
            password = "securepassword"  # You can use a default password or random generation
            user = User.objects.create_user(username=email, email=email, password=password)
            
            # Create the Patient instance and link it to the newly created user
            patient = Patient.objects.create(
                user=user,  # Ensure that user is linked to the patient
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                dob=dob,
                address=address,
                cancer_type=cancer_type,
                treatment_status=treatment_status,
                emergency_contact=emergency_contact
            )

            # Log the user in automatically
            login(request, user)

            # Redirect to the patient dashboard after logging in
            return redirect('patient-dashboard')

        except IntegrityError:
            # If an IntegrityError occurs (e.g., duplicate entry), show a message
            messages.error(request, "There was an error creating your account. Please try again.")
            return redirect('patient_signup')

    return render(request, 'signup_patient.html')

def patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patient_profile.html', {'patient': patient})

def patient_edit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        # Manually handling patient editing
        patient.first_name = request.POST.get('first_name', patient.first_name)
        patient.last_name = request.POST.get('last_name', patient.last_name)
        patient.dob = request.POST.get('dob', patient.dob)
        patient.address = request.POST.get('address', patient.address)
        
        patient.save()
        return redirect('patient_profile', patient_id=patient.id)

    return render(request, 'signup_form.html', {'patient': patient})

def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('patient-dashboard')  # Redirecting to patient-dashboard after deletion

@login_required
def patient_appointments(request):
    appointments = Appointment.objects.filter(patient_name=request.user.get_full_name())
    return render(request, 'appointments_list.html', {'appointments': appointments})

def update_appointment(request, id):
    # Get the appointment by ID
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == 'POST':
        # Extract data from the POST request and update the appointment
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        reason_for_visit = request.POST.get('reason_for_visit')

        # Update the appointment fields
        appointment.doctor_id = doctor_id
        appointment.appointment_date = appointment_date
        appointment.reason_for_visit = reason_for_visit

        # Save the updated appointment
        appointment.save()

        # Redirect to the patient dashboard after update
        return redirect('patient-dashboard')

    # If GET request, just render the page with the appointment details
    return render(request, 'update_appointment.html', {'appointment': appointment})

@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('patient_appointments')

@login_required
def create_appointment(request):
    if request.method == 'POST':
        patient_name = request.user.first_name + " " + request.user.last_name
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        
        doctor = get_object_or_404(Doctor, id=doctor_id)

        Appointment.objects.create(
            patient_name=patient_name,
            doctor=doctor,
            appointment_date=appointment_date.split('T')[0],
            time=appointment_date.split('T')[1]
        )
        return redirect('appointment_success')

    doctors = Doctor.objects.all()
    return render(request, 'create_appointment.html', {'doctors': doctors})

def appointment_success(request):
    return render(request, 'appointment_success.html')

def cancel_appointment(request, id):
    # Logic to cancel the appointment
    appointment = Appointment.objects.get(id=id)
    appointment.status = 'Cancelled'
    appointment.save()
    return redirect('patient-dashboard')  

def book_appointment(request):
    if request.method == 'POST':
        doctor = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        reason_for_visit = request.POST.get('reason_for_visit')

        try:
            appointment_date_parsed = timezone.datetime.fromisoformat(appointment_date)
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('patient-dashboard')

        # Check if the user has a patient profile
        try:
            patient = Patient.objects.get(email=request.user.email)
        except Patient.DoesNotExist:
            messages.error(request, "Patient profile not found.")
            return redirect('patient-dashboard')

        # Check for conflicting appointments
        conflict = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date_parsed
        ).exists()

        if conflict:
            messages.error(request, "The selected time slot is already booked. Please choose another.")
            return redirect('patient-dashboard')

        # Save the appointment
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date_parsed,
            reason_for_visit=reason_for_visit
        )
        appointment.save()
        messages.success(request, "Appointment booked successfully!")
        return redirect('patient-dashboard')

    return render(request, 'patient_dashboard.html')

from django.shortcuts import render

def doctor_detail(request, id):
    # Hardcoded list of doctors (or just one doctor for the details)
    doctors = [
        {'id': 1, 'name': 'Dr. John Smith', 'specialty': 'Cardiologist', 'hospital': 'City Hospital'},
        {'id': 2, 'name': 'Dr. Jane Doe', 'specialty': 'Dermatologist', 'hospital': 'Sunshine Clinic'},
        {'id': 3, 'name': 'Dr. Emily White', 'specialty': 'Neurologist', 'hospital': 'Greenwood Medical Center'},
        {'id': 4, 'name': 'Dr. Alex Brown', 'specialty': 'Orthopedic', 'hospital': 'City Hospital'},
    ]
    
    doctor = next((doctor for doctor in doctors if doctor['id'] == id), None)
    
    if doctor is None:
        return render(request, '404.html')  # Return a 404 page if doctor is not found

    return render(request, 'doctor_detail.html', {'doctor': doctor})
from django.shortcuts import render

def hospital_detail(request, id):
    # Hardcoded list of hospitals (or just one hospital for the details)
    hospitals = [
        {'id': 1, 'name': 'City Hospital', 'location': '123 Main St, City Center'},
        {'id': 2, 'name': 'Sunshine Clinic', 'location': '456 Oak Ave, Sunshine Park'},
        {'id': 3, 'name': 'Greenwood Medical Center', 'location': '789 Pine Rd, Greenwood'},
    ]
    
    hospital = next((hospital for hospital in hospitals if hospital['id'] == id), None)
    
    if hospital is None:
        return render(request, '404.html')  # Return a 404 page if hospital is not found

    return render(request, 'hospital_detail.html', {'hospital': hospital})
