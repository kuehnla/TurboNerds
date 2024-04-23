from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import User, Lab


# use of django forms
# from .models import User

# use of django forms


class RegistrationForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'password', 'email', 'phone', 'role')

class EditProfileForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone')

class TaAssignment(forms.ModelForm):
    ta = forms.ModelChoiceField(queryset=User.objects.filter(is_assistant=True))
    lab = forms.ModelChoiceField(queryset=Lab.objects.all())

    class Meta:
        model = Lab
        fields = ['ta', 'lab']

    def __init__(self, course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lab'].queryset = Lab.objects.filter(course=course)