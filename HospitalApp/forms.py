from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Patient, Appointment, Doctor, Feedback, Package, Department, MedicalRecord

CustomUser = get_user_model()  # Ensure we use the custom user model

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }


class StaffRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'user_type', 'email', 'password1', 'password2']

        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'user_type': 'Select Role',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'  # Assign user_type as 'doctor'
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name', 'dob', 'gender', 'email',
            'phone', 'address_line1', 'address_line2', 
            'emergency_contact', 'admission_date', 'profile_photo'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit phone number'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 1'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 2'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter emergency contact number'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }



class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        input_formats=['%Y-%m-%d']  # Ensures Django correctly parses YYYY-MM-DD format
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_slot', 'phone']
        
        widgets = {
            'phone': forms.TextInput(
                attrs={'type': 'tel', 'class': 'form-control', 'placeholder': 'Enter phone number'}
            ),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Appointment  # Ensure Appointment contains these fields or use a different model
        fields = ['prescription', 'notes']

        labels = {
            'prescription': 'Add the prescription',
            'notes': 'Disease'
        }

        widgets = {
            'prescription': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user','status']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialization'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit phone number'}),
            'department': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select department'}),
            'license_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter license number'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter years of experience'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
           'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter your feedback or complaint here'}),
        }


class PackagesForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'email', 'phone', 'package_type']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Department Name'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter Details', 'rows': 4}),
            'department_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'record_date', 'description', 'report', 'prescription']

        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
