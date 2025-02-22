from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import traceback  
from .models import Patient 
from django.contrib.auth import update_session_auth_hash
from .models import *
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test

from datetime import datetime



def CustomLogoutView(request):
    logout(request)
    return redirect('login')




def sign_up(request):
    form=UserRegisterForm()
    try:
        if request.method == "POST":
            form =UserRegisterForm(request.POST, request.FILES)
            if form.is_valid():  
                form.save() 
                username=form.cleaned_data.get('username')
                messages.success(request,f'welcome{username}, your account is created')
                return redirect('HospitalApp:user_home')
            else:
                print("c")
                messages.error(request, "Invalid data entered") 
            return render(request, 'HospitalApp/sign_up.html', {'form': form})
        else:            
            form=UserRegisterForm()
            return render(request, 'HospitalApp/sign_up.html', {'form': form})
    except Exception as e:
        print(e)  
        messages.error(request, "An error occurred while entering data")
        return redirect('HospitalApp:sign_up')


def home(request):
    return render(request,'HospitalApp/homes.html')

def user_home(request):
    return render(request,'HospitalApp/user_home.html')

def about_us(request):
    return render(request,'HospitalApp/about_us.html')

def user_about_us(request):
    return render(request,'HospitalApp/user_about_us.html')

def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect('HospitalApp:user_view_profile') 

def services(request):
    return render(request,'HospitalApp/services.html')

def user_services(request):
    return render(request,'HospitalApp/user_services.html')



def doctor(request):
    doctors = Doctor.objects.all() 
    return render(request,'HospitalApp/doctors.html', {'doctors': doctors})

def user_doctor(request):
    doctors = Doctor.objects.all()
    return render(request,'HospitalApp/user_doctor.html', {'doctors': doctors})



def departments(request):
    return render(request,'HospitalApp/departments.html')

def departments(request):
    departments = Department.objects.all()  
    return render(request, 'HospitalApp/departments.html', {'departments': departments})

def user_departments(request):
    return render(request,'HospitalApp/user_departments.html')



def is_doctor(user):
    return user.is_authenticated and user.user_type == "doctor"

def is_patient(user):
    return user.is_authenticated and user.user_type == "patient"

def is_admin(user):
    return user.is_authenticated and user.user_type == "admin" and user.is_superuser
        

def feedback(request):
    form = FeedbackForm()
    try:
        if request.method == "POST":
            form = FeedbackForm(request.POST, request.FILES)
            if form.is_valid():  
                form.save() 
                messages.success(request, "Thank you for the time")  
                return redirect('HospitalApp:feedback')
            else:
                messages.error(request, "Invalid data entered") 
            return render(request, 'HospitalApp/feedback.html', {'form': form})
        else:
            form = FeedbackForm()
            return render(request, 'HospitalApp/feedback.html', {'form': form})
    except Exception as e:
        print(e)  
        messages.error(request, "An error occurred while entering data")
        return redirect('HospitalApp:feedback')

 
def user_feedback(request):
    form = FeedbackForm()
    try:
        if request.method == "POST":
            form = FeedbackForm(request.POST, request.FILES)
            if form.is_valid():  
                form.save() 
                messages.success(request, "Thank you for the time")  
                return redirect('HospitalApp:feedback')
            else:
                messages.error(request, "Invalid data entered") 
            return render(request, 'HospitalApp/user_feedback.html', {'form': form})
        else:
            form = FeedbackForm()
            return render(request, 'HospitalApp/user_feedback.html', {'form': form})
    except Exception as e:
        print(e)  
        messages.error(request, "An error occurred while entering data")
        return redirect('HospitalApp:user_feedback')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from .forms import AppointmentForm
from .models import Appointment, Patient
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url="login")
@user_passes_test(is_patient)
def user_appointment(request):
    form = AppointmentForm(request.POST or None)
    selected_doctor_id = request.GET.get("doctor") or request.POST.get("doctor")
    selected_date = request.GET.get("appointment_date") or request.POST.get("appointment_date")
    booked_slots = []


    # Get booked slots for selected doctor and date
    if selected_doctor_id and selected_date:
        booked_slots = Appointment.objects.filter(
            doctor_id=selected_doctor_id, appointment_date=selected_date, is_booked=True
        ).values_list("appointment_slot", flat=True)

    if request.method == "POST":
        patient = get_object_or_404(Patient, user=request.user)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.is_booked = True

            # Set appointment date explicitly
            appointment.appointment_date = selected_date
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect("HospitalApp:user_view_profile")
        else:
            messages.error(request, f"Invalid data entered: {form.errors}")

    return render(request, "HospitalApp/user_appointment.html",
                  {"form": form,"booked_slots": list(booked_slots),"selected_doctor_id": selected_doctor_id,"selected_date": selected_date,})


@login_required(login_url="login")
@user_passes_test(is_patient)
def user_view_appointment(request):
    return render(request,'HospitalApp/user_view_appointment.html')


# @login_required(login_url="login")
# @user_passes_test(is_patient)
# def user_view_profile(request):
#     form = PatientForm()
#     return render(request,'HospitalApp/user_view_profile.html')

def reference(request):
    return render(request,'HospitalApp/index.html')


# def make_appointment(request):
#     form = AppointmentForm()
#     doctors = Doctor.objects.all()  
#     return render(request, 'appointment.html', {'form': form, 'doctors': doctors})

def packages(request):
    return render(request,'HospitalApp/packages.html')



def book_package(request):
    form = PackagesForm()
    try:
        if request.method == "POST":
            form = PackagesForm(request.POST, request.FILES)
            if form.is_valid():  
                form.save() 
                messages.success(request, "Thank you for the time")  
                return redirect('HospitalApp:book_package')
            else:
                messages.error(request, "Invalid data entered") 
            return render(request, 'HospitalApp/book_package.html', {'form': form})
        else:
            form = PackagesForm()
        return render(request, 'HospitalApp/book_package.html', {'form': form})
    except Exception as e:
        print(e)  
        messages.error(request, "An error occurred while entering data")
        return redirect('HospitalApp:book_packages')

def facility(request):
    return render(request,'HospitalApp/facility.html')

# def login(request):
#     return render(request,'HospitalApp/login.html')

# def forgetpassword(request):
#     return render(request,'HospitalApp/forgetpassword.html')

# def sign_up(request):
#     return render(request,'HospitalApp/sign_up.html')

def patient_profile(request):
    patient = get_object_or_404(Patient, user=request.user)
    pending_count = Appointment.objects.filter(patient=patient,status="Booked").count()
    completed_count = Appointment.objects.filter(patient=patient,status="Completed").count()
    return render(request,'HospitalApp/patient_profile.html', {'patient':patient, 'pending_count': pending_count,
        'completed_count': completed_count,})


def CustomLoInView(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                
                if user.user_type == "patient":  # Redirect doctors to their dashboard
                    login(request, user)
                    if Patient.objects.filter(user=user).exists():  
                        return redirect("HospitalApp:user_home")  
                    else:  
                        return redirect("HospitalApp:add_patient") 
                
                else:
                    messages.error(request, "Access denied.")
            else:
                messages.error(request, "Invalid username or password.")
    
    return render(request, "HospitalApp/user_login.html", {"form": form})




def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('HospitalApp:change_password')

        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect('HospitalApp:change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  
        return redirect('HospitalApp:home')

    return render(request, 'HospitalApp/change_password.html')





# def blood_donation(request):
#     return render(request,'HospitalApp/blood_donation.html')

# def blood_donar(request):
#     form = DonorForm()
#     return render(request,'HospitalApp/blood_donar.html',  {'form': form})

# def blood_availability(request):
#     return render(request, 'HospitalApp/blood_availability.html')



@login_required(login_url="login")
@user_passes_test(is_patient) # Ensures only logged-in users can access this view
def add_patient(request):
    form = PatientForm()  # Initialize the form

    try:
        if request.method == "POST":
            form = PatientForm(request.POST, request.FILES)
            if form.is_valid():
                patient = form.save(commit=False)  # Create patient object, but don't save yet

                # Ensure user is assigned correctly
                if request.user.is_authenticated:
                    patient.user = request.user 
                    patient.has_completed_details=True 
                    patient.save()  # Now save to database
                    
                    messages.success(request, "Patient details added successfully!")
                    return redirect('HospitalApp:user_home')
                else:
                    messages.error(request, "You must be logged in to add a patient.")
                    return redirect('HospitalApp:login')  # Redirect to login

            else:
                messages.error(request, "Invalid data entered. Please check your details.")

    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging log
        messages.error(request, "An error occurred while adding the patient.")

    return render(request, 'HospitalApp/add_patient.html', {'form': form})  # Render form in all cases


def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)  # Get patient by ID

    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES, instance=patient)  # Pre-fill form with existing data
        if form.is_valid():
            
            form.save()  
            messages.success(request, "Patient details updated successfully!")
            return redirect('HospitalApp:user_home')
        else:  
            messages.error(request, "Invalid data. Please check the fields.")
    else:
        form = PatientForm(instance=patient)
    return render(request, 'HospitalApp/add_patient.html', {'form': form, 'patient': patient})



@login_required(login_url="login")
@user_passes_test(is_patient)
def user_view_profile(request):
    patient = get_object_or_404(Patient, user=request.user)  
    appointments = Appointment.objects.filter(patient=patient) 
    return render(request, 'HospitalApp/user_view_profile.html', {'patient': patient, 'appointments':appointments})

def add_medical_record(request):
    form = MedicalRecordForm()
    return render(request, 'HospitalApp/add_medical_record.html', {'form': form})

