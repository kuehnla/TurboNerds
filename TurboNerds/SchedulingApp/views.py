from django.shortcuts import render, redirect

from .forms import RegistrationForm, EditProfileForm

from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views


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


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html/'
    next_page = './home.html'
