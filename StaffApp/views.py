
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from HospitalApp.models import *
from HospitalApp.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa


from django.template.loader import get_template







def generate_prescription_pdf(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    
    # Load the template
    template = get_template('StaffApp/staff_template/pdf_template.html')
    context = {'appointment': appointment}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescription_{appointment.id}.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors while generating the PDF', status=500)
    
    return response




# Create your views here.

def is_doctor(user):
    return user.is_authenticated and user.user_type == "doctor"

def is_patient(user):
    return user.is_authenticated and user.user_type == "patient"

def is_admin(user):
    return user.is_authenticated and user.user_type == "admin" and user.is_superuser



def base(request):
    return render(request,'StaffApp/staff_template/staff_base.html')


@login_required(login_url='staff_login')
def staff_home(request):
    doctor = get_object_or_404(Doctor, user=request.user) 
    pending_count = Appointment.objects.filter(doctor=doctor,status="Booked").count()
    completed_count = Appointment.objects.filter(doctor=doctor,status="Completed").count()
    return render(request,'StaffApp/staff_template/staff_home.html', {'doctor': doctor, 'pending_count': pending_count,
        'completed_count': completed_count})






@login_required(login_url='staff_login')
def staff_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user) 
    return render(request,'StaffApp/staff_template/staff_profile.html', {'doctor': doctor})





def staff_login(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                
                if user.user_type == "doctor":  # Redirect doctors to their dashboard
                    login(request, user)
                    if Doctor.objects.filter(user=user).exists():  
                        return redirect("staff_home")  
                    else:  
                        return redirect("add_doctor") 
                
                else:
                    messages.error(request, "Access denied.")
            else:
                messages.error(request, "Invalid username or password.")
    
    return render(request, "StaffApp/staff_template/staff_login.html", {"form": form})


@login_required(login_url="staff_login")
@user_passes_test(is_doctor) # Ensures only logged-in users can access this view
def add_doctor(request):
    form = DoctorForm()  # Initialize the form

    try:
        if request.method == "POST":
            form = DoctorForm(request.POST, request.FILES)
            if form.is_valid():
                doctor = form.save(commit=False)  

                # Ensure user is assigned correctly
                if request.user.is_authenticated:
                    doctor.user = request.user  # Assign logged-in user
                    doctor.save()  # Now save to database
                    messages.success(request, "Doctor details added successfully!")
                    return redirect('staff_home')
                else:
                    messages.error(request, "You must be logged in to add adoctor.")
                    return redirect('staff_login')  # Redirect to login

            else:
                print(form.errors)
                messages.error(request, "Invalid data entered. Please check your details.")

    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging log
        messages.error(request, "An error occurred while adding the doctor.")

    return render(request, 'StaffApp/staff_template//add_doctor.html', {'form': form})  # Render form in all cases




def about(request):
    return render(request,'StaffApp/staff_template/about.html')

def services(request):
    return render(request,'StaffApp/staff_template/services.html')


@login_required(login_url='staff_login')
def schedule(request):
    now = timezone.now().date()
    
    # Get the logged-in doctor
    doctor = get_object_or_404(Doctor, user=request.user)

    # Filter appointments only for this doctor
    appointments = Appointment.objects.filter(doctor=doctor)  
    return render(request,'StaffApp/staff_template/schedules.html', {'doctor': doctor, 'appointments': appointments  })

# @login_required
# def schedules(request):
#     # Get the currently logged-in doctor
#     doctor = request.user  # Assuming doctors are users in your system

#     # Fetch appointments that belong to this doctor
#     appointments = Appointment.objects.filter(doctor=doctor).order_by('appointment_date')

#     return render(request, 'StaffApp/staff_template/schedules.html', {'appointments': appointments})



@login_required(login_url="staff_login")
@user_passes_test(is_doctor)
def add_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)  # Get the specific appointment

    if request.method == "POST":
        form = PrescriptionForm(request.POST, request.FILES, instance=appointment)  # Bind the form to the appointment
        if form.is_valid():
            appointment.status = "Completed"
            form.save() 
            messages.success(request, "Prescription added successfully.")
            return redirect('staff_home')  # Redirect after success
        else:
            messages.error(request, "Invalid data entered. Please check your details.")
    else:
        form = PrescriptionForm(instance=appointment) 

    return render(request, 'StaffApp/staff_template/add_prescription.html', {'form': form, 'appointment': appointment})


@login_required(login_url='staff_login')
def view_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)  # Get the specific appointment
    
    return render(request,'StaffApp/staff_template/view_prescription.html', {'appointment':appointment} )


# @login_required(login_url='staff_login')
# def staff_profile(request, doctor_id):
#     now = timezone.now()
    
#     # Get the logged-in doctor
#     doctor = get_object_or_404(Doctor, user=request.user)

#     # Filter appointments only for the logged-in doctor
#     past_appointments = Appointment.objects.filter(doctor_id=doctor.id, appointment_date__lt=now.date())  
#     future_appointments = Appointment.objects.filter(doctor_id=doctor.id, appointment_date__gte=now.date())  

#     return render(request, 'StaffApp/staff_template/staff_profile.html', {'doctor': doctor, 'past_appointments': past_appointments, 'future_appointments': future_appointments })


@login_required(login_url='staff_login')
def staff_profile(request):
    now = timezone.now().date()
    
    # Get the logged-in doctor
    doctor = get_object_or_404(Doctor, user=request.user)

    # Filter appointments only for this doctor
    past_appointments = Appointment.objects.filter(doctor=doctor, appointment_date__lt=now)  
    future_appointments = Appointment.objects.filter(doctor=doctor, appointment_date__gte=now)  

    return render(request,'StaffApp/staff_template/staff_profile.html', {'doctor': doctor, 'past_appointments': past_appointments, 'future_appointments': future_appointments })



@login_required(login_url='staff_login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  
        return redirect('staff_home')

    return render(request, 'StaffApp/staff_template/change_password.html')


def staff_logout(request):
    logout(request)
    return redirect('staff_login')

def admin(request):
    return render(request,'StaffApp/staff_template/admin.html')



# def home(request):
#     return render(request,'HospitalApp/home.html')

