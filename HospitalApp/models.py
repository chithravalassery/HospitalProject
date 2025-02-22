from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    class Meta:  
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['id']

    def is_patient(self):
        return self.user_type == 'patient'

    def is_doctor(self):
        return self.user_type == 'doctor'

    def is_admin(self):
        return self.is_superuser or self.user_type == 'admin'


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    notes = models.TextField(verbose_name="Details")
    department_photo = models.ImageField(upload_to='media/department_photos/')

    def __str__(self):
        return self.name


class Patient(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="patient_profile")
    name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    phone = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{10,15}$', message="Enter a valid phone number")])
    email = models.EmailField()
    emergency_contact = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{10,15}$', message="Enter a valid phone number")])
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    admission_date = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    has_completed_details = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='media/profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Doctor(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    STATUS_CHOICES = [('Active', 'Active'), ('Resigned', 'Resigned'), ('Retired', 'Retired'), ('Transferred', 'Transferred'), ('Terminated', 'Terminated')]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="doctor_profile")
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    phone = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{10}$', message="Enter a valid phone number")])
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    license_no = models.CharField(max_length=50, unique=True, verbose_name="License Number")
    experience = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='media/doctor_photos/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"Dr. {self.name} ({self.department.name})"

from django.core.validators import RegexValidator
from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [('Booked', 'Booked'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    SLOT_CHOICES = [(i, f"Slot {i}") for i in range(1, 6)]  # 5 predefined slots

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_slot = models.IntegerField(choices=SLOT_CHOICES)
    phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\d{10,15}$', message="Enter a valid phone number")]
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Booked')
    notes = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)

    is_booked = models.BooleanField(default=False, editable=False)  # Auto-set when booked, hidden from forms


    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} on {self.appointment_date}, Slot {self.appointment_slot}"


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Your Name")
    email = models.EmailField(verbose_name="Your Email")
    message = models.TextField(verbose_name="Your Feedback")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.email})"


class Package(models.Model):
    PACKAGE_CHOICES = [('Basic', 'Basic'), ('Comprehensive', 'Comprehensive'), ('Advanced', 'Advanced')]

    name = models.CharField(max_length=100, verbose_name="Your Name")
    email = models.EmailField(verbose_name="Your Email")
    phone = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{10,15}$', message="Enter a valid phone number")], verbose_name="Your Phone Number")
    package_type = models.CharField(max_length=100, choices=PACKAGE_CHOICES, default='Basic', verbose_name="Select Package")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Package Inquiry from {self.name} ({self.email})"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    record_date = models.DateField()
    description = models.TextField()
    report = models.FileField(upload_to='media/medical_reports/', blank=True, null=True)
    prescription = models.FileField(upload_to='media/prescription/', blank=True, null=True)

    def __str__(self):
        return f"Medical Record for {self.patient.name} on {self.record_date}"
