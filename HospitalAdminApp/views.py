from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from HospitalApp.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test




# Create your views here.

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_home')  # Already logged in as admin
        else:
            messages.error(request, "You are not authorized to access this page.")
            return redirect('user_home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_superuser:  # Ensure only superusers can log in
                login(request, user)
                messages.success(request, "Admin login successful!")
                return redirect('admin_home')
            else:
                messages.error(request, "Invalid credentials. Please try again.")  # Generic error message
        else:
            messages.error(request, "Invalid credentials. Please try again.")  # Same message for all failures

    return render(request, 'HospitalAdminApp/admin_template/login.html')


def is_doctor(user):
    return user.is_authenticated and user.user_type == "doctor"

def is_patient(user):
    return user.is_authenticated and user.user_type == "patient"

def is_admin(user):
    return user.is_authenticated and user.user_type == "admin" or user.is_superuser
        
def home(request):
    return render(request,'HospitalAdminApp/admin_template/home.html')

# def patient(request):
#     return render(request,'HospitalAdminApp/admin_template/patient.html')

def sign_up(request):
    form = StaffRegisterForm()
    try:
        if request.method == "POST":
            form = StaffRegisterForm(request.POST, request.FILES)
            if form.is_valid(): 
                user = form.save()  # Save the user
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account for {username} is created')
                return redirect('admin_home')  # Redirect to doctor profile creation
            else:
                messages.error(request, "Invalid data entered")
                 
        else:
            print("e")            
            form = StaffRegisterForm()  # Use form instance instead of model
            return render(request, 'HospitalAdminApp/admin_template/sign_up.html', {'form': form})
    
    except Exception as e:
        print(f"Error during sign-up: {e}")  # Log error for debugging
        messages.error(request, "An error occurred while entering data")
    return render(request, 'HospitalAdminApp/admin_template/sign_up.html', {'form': form})

def doctor(request):
    doctors = Doctor.objects.all() 
    return render(request,'HospitalAdminApp/admin_template/doctor.html', {'doctors': doctors})

def department(request):
    departments = Department.objects.all()
    return render(request,'HospitalAdminApp/admin_template/department.html', {'departments': departments})



        
@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def add_department(request):
    form=DepartmentForm()
    try:
        if request.method=="POST":
            form=DepartmentForm(request.POST,request.FILES)
            if form.is_valid:
                form.save()
                messages.success(request,"Department added Successfully")
                return redirect('add_department')
            else:
                messages.error(request, "Invalid data entered")
            return render(request,'HospitalAdminApp/admin_template/add_department.html', {'form': form} )
        else:
            form=DepartmentForm()
        return render(request,'HospitalAdminApp/admin_template/add_department.html', {'form': form} )
    except Exception as e:
        print(e)
        messages.error(request, "An error occurred while adding the department")
        return redirect('add_department')

@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)  # Fetch department by ID

    if request.method == "POST":
        form = DepartmentForm(request.POST, request.FILES, instance=department)  # Load existing data into form
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department')  # Redirect to department list after update
        else:
            messages.error(request, f"Invalid data entered: {form.errors}")

    else:
        form = DepartmentForm(instance=department)  # Pre-fill form with department details

    return render(request, 'HospitalAdminApp/admin_template/edit_department.html', {'form': form, 'department': department})

@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, "Department deleted successfully!")
    return redirect('department')



@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)  # Get the doctor by ID

    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance=doctor)  # Load form with existing data
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor details updated successfully!")
            return redirect('admin_home')  # Redirect to admin dashboard after update
        else:
            messages.error(request, "Invalid data entered. Please check your details.")

    else:
        form = DoctorForm(instance=doctor)  # Pre-fill form with doctor's current details

    return render(request, 'HospitalAdminApp/admin_template/edit_doctor.html', {'form': form, 'doctor': doctor})

@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    messages.success(request, "Doctor record deleted successfully!")
    return redirect('doctor') 


@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def patient(request):
    patients = Patient.objects.all()  
    return render(request, 'HospitalAdminApp/admin_template/view_patient.html', {'patients': patients})
            

@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)  # Fetch the patient by ID

    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES, instance=patient)  # Load existing data into form
        if form.is_valid():
            form.save()
            messages.success(request, "Patient details updated successfully!")
            return redirect('patient')  # Redirect to patient list after update
        else:
            messages.error(request, f"Invalid data entered: {form.errors}")

    else:
        form = PatientForm(instance=patient)  # Pre-fill form with patient details

    return render(request, 'HospitalAdminApp/admin_template/edit_patient.html', {'form': form, 'patient': patient})

@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    messages.success(request, "Patient record deleted successfully!")
    return redirect('patient')


@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def appointment(request):
    appointments= Appointment.objects.all() 
    return render(request,'HospitalAdminApp/admin_template/appointment.html', {'appointments': appointments})


@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect('appointment') 

@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def admin_home(request):
    total_doctors = Doctor.objects.count()
    total_appointment = Appointment.objects.count()
    total_patient = Patient.objects.count()
    total_department = Department.objects.count()
    return render(request,'HospitalAdminApp/admin_template/adminapp_home.html', {'total_doctor': total_doctors, 'total_appointment': total_appointment,'total_patient':total_patient, 'total_department':total_department})