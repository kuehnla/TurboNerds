from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import User, Lab, Section, Course


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
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("This phone number is already in use.")
        return phone


class TaAssignment(forms.ModelForm):
    ta = forms.ModelChoiceField(queryset=User.objects.filter(is_assistant=True))
    lab = forms.ModelChoiceField(queryset=Lab.objects.all())

    class Meta:
        model = Lab
        fields = ['ta', 'lab']

    def __init__(self, course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lab'].queryset = Lab.objects.filter(course=course)


class InstructorAssignment(forms.ModelForm):
    instructor = forms.ModelChoiceField(queryset=User.objects.filter(is_instructor=True))
    section = forms.ModelChoiceField(queryset=Section.objects.all())

    class Meta:
        model = Lab
        fields = ['instructor', 'section']

    def __init__(self, course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.filter(course=course)


class CreateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'department', 'number', 'semester']
