"""
URL configuration for studenthub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from studenthubapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.login_view, name='login_url'),
    path('logout/', views.logout_view, name='logout_url'),
    path('/home', views.home, name='home_url'),
    path('addstudent/', views.student_add, name='addstudent_url'),
    path('showstudent/', views.showstudent, name='showstudent_url'),
    path('editstudent/<int:id>/', views.studentedit, name='editstudent_url'),
    path('deletestudent/<int:id>/', views.studentdelete, name='deletestudent_url'),
    path('addbatch/', views.batch_add, name='addbatch_url'),
    path('showbatch/', views.showbatch, name='showbatch_url'),
    path('editbatch/<int:id>/', views.batchedit, name='editbatch_url'),
    path('deletebatch/<int:id>/', views.batchdelete, name='deletebatch_url'),
    path('markattendance/', views.mark_attendance, name='mark_attendance_url'),
    path('showattendance/', views.show_attendance, name='show_attendance_url'),
    path('editattendance/<int:id>/', views.edit_attendance, name='edit_attendance_url'),
    path('deleteattendance/<int:id>/', views.delete_attendance, name='delete_attendance_url'),
    path('attendancecount/', views.attendance_count, name='attendance_count_url'),
    path('contactus/', views.contactus, name='contactus_url'),
    path('aboutus/', views.aboutus, name='aboutus_url'),
]
