from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student, Batch, Attendance
from .forms import StudentForm, BatchForm, AttendanceForm, MultipleAttendanceForm, LoginForm
import json
from django.contrib.auth import logout
from django.http import JsonResponse
from collections import defaultdict

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == 'admin' and password == 'admin':
                return redirect('home_url')
            else:
                 error_message = "Invalid credentials"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_url')

def home(request):
    return render(request, 'home.html')

def contactus(request):
    return render(request, 'contactus.html')

def aboutus(request):
    return render(request, 'aboutus.html')


def student_add(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showstudent_url')
    return render(request, 'addstudent.html', {'form': form})


def showstudent(request):
    students = Student.objects.all()
    return render(request, 'showstudent.html', {'students': students})


def studentedit(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('showstudent_url')
    else:
        form = StudentForm(instance=student)
    return render(request, 'editstudent.html', {'form': form})


def studentdelete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('showstudent_url')
    return render(request, 'deletestudent.html', {'student': student})


def batch_add(request):
    form = BatchForm()
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showbatch_url')
    return render(request, 'addbatch.html', {'form': form})


def showbatch(request):
    batches = Batch.objects.all()
    return render(request, 'showbatch.html', {'batches': batches})


def batchedit(request, id):
    batch = get_object_or_404(Batch, id=id)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            return redirect('showbatch_url')
    else:
        form = BatchForm(instance=batch)
    return render(request, 'editbatch.html', {'form': form})


def batchdelete(request, id):
    batch = get_object_or_404(Batch, id=id)
    if request.method == 'POST':
        batch.delete()
        return redirect('showbatch_url')
    return render(request, 'deletebatch.html', {'batch': batch})


def mark_attendance(request):
    batches = Batch.objects.all()
    students = None
    selected_batch = None

    if request.method == 'POST':
        form = MultipleAttendanceForm(request.POST)
        selected_batch_id = request.POST.get('batch')
        if selected_batch_id:
            selected_batch = Batch.objects.get(id=selected_batch_id)
            students = Student.objects.filter(batch=selected_batch)

        if form.is_valid() and students is not None:
            date = form.cleaned_data['date']
            student_attendance = form.cleaned_data['student_attendance']
            if student_attendance:
                student_attendance = json.loads(student_attendance)
                for student_id, status in student_attendance.items():
                    student = Student.objects.get(id=student_id)
                    Attendance.objects.create(student=student, date=date, status=status)
            return redirect('show_attendance_url')
    else:
        form = MultipleAttendanceForm()

    return render(request, 'mark_attendance.html', {
        'form': form,
        'batches': batches,
        'students': students,
        'selected_batch': selected_batch
    })


def show_attendance(request):
    batches = Batch.objects.all()
    selected_batch = None
    selected_date = None
    attendance_records = Attendance.objects.all()

    if request.method == 'GET':
        selected_batch_id = request.GET.get('batch')
        selected_date = request.GET.get('date')
        if selected_batch_id:
            selected_batch = Batch.objects.get(id=selected_batch_id)
            attendance_records = attendance_records.filter(student__batch=selected_batch)
        if selected_date:
            attendance_records = attendance_records.filter(date=selected_date)


    return render(request, 'show_attendance.html', {
        'attendance_records': attendance_records,
        'batches': batches,
        'selected_batch': selected_batch,
        'selected_date': selected_date,
        
    })

def edit_attendance(request, id):
    attendance_record = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance_record)
        if form.is_valid():
            form.save()
            return redirect('show_attendance_url')
    else:
        form = AttendanceForm(instance=attendance_record)
    return render(request, 'edit_attendance.html', {'form': form, 'attendance_record': attendance_record})

def delete_attendance(request, id):
    attendance_record = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        attendance_record.delete()
        return redirect('show_attendance_url')
    return render(request, 'delete_attendance.html', {'attendance_record': attendance_record})

def attendance_count(request):
    batches = Batch.objects.all()
    selected_batch = None
    student_attendance = {}

    if request.method == 'GET':
        selected_batch_id = request.GET.get('batch')
        if selected_batch_id:
            selected_batch = Batch.objects.get(id=selected_batch_id)
            attendance_records = Attendance.objects.filter(student__batch=selected_batch)

            # Calculate attendance counts for students in the selected batch
            for record in attendance_records:
                if record.student not in student_attendance:
                    student_attendance[record.student] = {'P': 0, 'A': 0}
                student_attendance[record.student]['P' if record.status == 'P' else 'A'] += 1

    return render(request, 'attendance_count.html', {
        'batches': batches,
        'selected_batch': selected_batch,
        'student_attendance': student_attendance.items()
    })