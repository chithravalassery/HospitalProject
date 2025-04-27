from django.urls import path
from . import views

urlpatterns = [
    path('base', views.base),
    path('add_doctor',views.add_doctor, name='add_doctor'),
    path('staff_home', views.staff_home, name="staff_home"),
    path('staff_login', views.staff_login, name='staff_login'),
    path('about', views.about,  name='about'),
    path('services', views.services,  name='services'),
    path('staff_profile', views.staff_profile,  name='staff_profile'),
    path('staff_logout', views.staff_logout, name='staff_logout'),
    path('schedule', views.schedule, name='schedule'),
    path('add_prescription/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
    path('view_prescription/<int:appointment_id>/', views.view_prescription, name='view_prescription'),
    path('admin', views.admin),
    path('change_password', views.change_password, name="change_password"),
    path('download_prescription/<int:appointment_id>/', views.generate_prescription_pdf, name='download_prescription'),

    
]
