from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import User, Lab, Section, Course
from django.forms.widgets import DateInput


# use of django forms
# from .models import User

# use of django forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2')


class EditProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone')

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != self.instance.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone != self.instance.phone:
            if not phone.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            if len(phone) != 10:
                raise forms.ValidationError("Phone number must be 10 digits long.")
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("This phone number is already in use.")
        return phone


class TaAssignment(forms.ModelForm):
    ta = forms.ModelChoiceField(queryset=User.objects.filter(is_assistant=True))

    class Meta:
        model = Lab
        fields = ['ta']

    def __init__(self, course, lab, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_id = course
        self.lab_id = lab

    def save(self, commit=True):
        instance = super(TaAssignment, self).save(commit=False)
        instance.course = self.course_id
        if commit:
            instance.save()
        return instance



class InstructorAssignment(forms.ModelForm):
    instructor = forms.ModelChoiceField(queryset=User.objects.filter(is_instructor=True))
    section = forms.ModelChoiceField(queryset=Section.objects.all())

    class Meta:
        model = Lab
        fields = ['instructor', 'section']

    def __init__(self, course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.filter(course=course)
        self.course_id = course


class CreateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'department', 'number', 'semester']


class LabCreation(forms.ModelForm):
    DAYS_CHOICES = [
        ('Mo', 'Mo'),
        ('Tu', 'Tu'),
        ('Wed', 'Wed'),
        ('Th', 'Th'),
        ('Fri', 'Fri'),
    ]
    days = forms.MultipleChoiceField(choices=DAYS_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Lab
        fields = ['assistant', 'lab_name', 'start_time', 'end_time', 'days']
        labels = {
            'assistant': 'Assistant',
            'lab_name': 'Lab name',
            'start_time': 'Start time (HH:MM:SS)',
            'end_time': 'End time (HH:MM:SS)',
            'days': 'Days'
        }

    def __init__(self, course, *args, **kwargs):
        super(LabCreation, self).__init__(*args, **kwargs)
        self.course_id = course

    def save(self, commit=True):
        instance = super(LabCreation, self).save(commit=False)
        instance.course = self.course_id
        if commit:
            instance.save()
        return instance


class SectionCreation(forms.ModelForm):
    DAYS_CHOICES = [
        ('Mo', 'Mo'),
        ('Tu', 'Tu'),
        ('Wed', 'Wed'),
        ('Th', 'Th'),
        ('Fri', 'Fri'),
    ]
    days = forms.MultipleChoiceField(choices=DAYS_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Section
        fields = ['instructor', 'section_name', 'start_date', 'end_date', 'start_time', 'end_time', 'days']
        labels = {
            'instructor': 'Instructor',
            'section_name': 'Section name',
            'start_date': 'Start date (mm/dd/yyyy)',
            'end_date': 'End date (mm/dd/yyyy)',
            'start_time': 'Start time (HH:MM:SS)',
            'end_time': 'End time (HH:MM:SS)',
            'days': 'Days'
        }

    def __init__(self, course, *args, **kwargs):
        super(SectionCreation, self).__init__(*args, **kwargs)
        self.course_id = course

        self.fields['start_date'].widget = DateInput(attrs={'type': 'date'})
        self.fields['end_date'].widget = DateInput(attrs={'type': 'date'})
        # self.fields['days'].widget = Select(choices=self.DAYS_CHOICES)

    def save(self, commit=True):
        instance = super(SectionCreation, self).save(commit=False)
        instance.course = self.course_id
        if commit:
            instance.save()
        return instance


# class CreateLab(forms.ModelForm):
#     class Meta:
#         model = Lab
#         fields = ['assistant', 'lab_name', 'start_time', 'end_time', 'days']
#
#     def __init__(self, course, *args, **kwargs):
#         super(CreateLab, self).__init__(*args, **kwargs)
#         self.course_id = course
#
#     def save(self, commit=True):
#         instance = super(CreateLab, self).save(commit=False)
#         instance.course = self.course_id
#         if commit:
#             instance.save()
#         return instance
#
#
# class CreateSection(forms.ModelForm):
#     class Meta:
#         model = Section
#         fields = ['instructor', 'start_date', 'end_date', 'start_time', 'end_time', 'days']
#
#     def __init__(self, course, *args, **kwargs):
#         super(CreateSection, self).__init__(*args, **kwargs)
#         self.course_id = course
#
#     def save(self, commit=True):
#         instance = super(CreateSection, self).save(commit=False)
#         instance.course = self.course_id
#         if commit:
#             instance.save()
#         return instance
