from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



app_name = 'HospitalApp'
urlpatterns = [
    
    path('user_home', views.user_home, name='user_home' ),
    
    # path('user_homepage', views.user_homepage),
    path('user_about_us', views.user_about_us, name='user_about_us'),
    path('user_services', views.user_services, name="user_services"),
     path('user_doctor', views.user_doctor, name="user_doctor"),
    path('departments', views.departments, name="department"),
    path('user_departments', views.user_departments, name="user_department"),
    path('feed_back', views.feedback,name='feedback'),
    path('user_feedback', views.user_feedback,name='user_feedback'),
    path('patient_profile', views.patient_profile, name="patient_profile"),
    path('user_appointment', views.user_appointment,name= 'user_appointment'),
    path('user_view_appointment', views.user_view_appointment, name="user_view_appointment"),
   
    path('user_view_profile', views.user_view_profile, name="user_view_profile"),
    path('add_patient', views.add_patient, name="add_patient"),
    path('edit_patient/<int:pk>', views.edit_patient, name='edit_patient'),
    path('delete_appointment/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('change_password', views.change_password, name='change_password'),
    # path('login', views.login, name='login'),
    # path('forgetpassword', views.forgetpassword, name='forgetpassword'),
    path('sign_up', views.sign_up,name='sign_up'),
    path('packages', views.packages),
    path('book_packages', views.book_package,name='book_package' ),
    # path('blood_donation', views.blood_donation, name='blood_donation'),
    # path('blood_donar', views.blood_donar, name='blood_donar'),
    # path('blood_availability', views.blood_availability, name='blood_availability'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('add_medical_record', views.add_medical_record, name='add_medical_record'),


]


