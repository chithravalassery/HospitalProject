from django.urls import path
from . import views

urlpatterns = [

    # path('staff_login',views.staff_login),
    path('sign_up',views.sign_up, name='staff_sign_up'),
    path('admin_home',views.admin_home, name='admin_home'),
    path('admin_login',views.admin_login, name='admin_login'),
    path('admin_logout/', views.CustomLogoutView, name='admin_logout'),





    path('patient',views.patient, name="patient"),
    path('edit_patient/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:pk>/', views.delete_patient, name='delete_patient'),


    path('doctor',views.doctor, name="doctor"),
    path('edit_doctor/<int:pk>', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:pk>/', views.delete_doctor, name='delete_doctor'),

    path('department',views.department,name='department' ),
    path('add_department',views.add_department, name='add_department'),
    path('edit_department/<int:pk>/', views.edit_department, name='edit_department'),
    path('delete_department/<int:pk>/', views.delete_department, name='delete_department'),

    path('appointment',views.appointment, name="appointment"),
    path('delete_appointment/<int:pk>/', views.delete_appointment, name='delete_appointment'),

    #

]