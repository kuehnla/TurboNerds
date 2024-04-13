from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from TurboNerds.SchedulingApp.forms import (
    RegistrationForm,
    EditProfileForm
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')
        else:
            form = RegistrationForm()

            args = {'form': form}
            return render(request, 'accounts/register.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)