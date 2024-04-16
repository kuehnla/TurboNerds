from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .forms import (
    RegistrationForm,
    EditProfileForm
)
from .models import UserProfile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
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