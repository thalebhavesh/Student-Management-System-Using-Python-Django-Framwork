from django import forms
from studenthubapp.models import Student, Batch,Attendance


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields = ['first_name', 'last_name', 'address', 'email', 'city', 'course','batch']
        widgets = {
            'address': forms.TextInput(attrs={'size': 50}), 
        }

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

class MultipleAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    student_attendance = forms.CharField(widget=forms.HiddenInput(), required=False)