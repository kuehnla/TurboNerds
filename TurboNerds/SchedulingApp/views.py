from django.shortcuts import render, redirect

from .forms import RegistrationForm, EditProfileForm
from .models import User
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
    #submitted = False
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        #form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']

            if role == 'Instructor':
                user_profile = User.objects.create(first_name=first_name, last_name=last_name,
                                           email=email, phone=phone, is_instructor=True, is_admin=False,
                                           is_assistant=False)

            elif role == 'Supervisor':
                user_profile = User.objects.create(first_name=first_name, last_name=last_name,
                                           email=email, phone=phone, is_instructor=False, is_admin=True,
                                           is_assistant=False)

            else:
                user_profile =User.objects.create(first_name=first_name, last_name=last_name,
                                           email=email, phone=phone, is_instructor=False, is_admin=False,
                                           is_assistant=True)

            user_profile.save()

            return redirect('home')
    else:
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})


def edit_profile(request,email):
    if request.method == 'POST':
        user = User.objects.get(email=email)
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.phone = request.POST['phone']

            User.objects.filter(email=email).update(first_name=user.first_name
                                                    , last_name=user.last_name, email=user.email, phone=user.phone)
            return redirect('home')
    else:
        user = User.objects.get(email=email)
        form = EditProfileForm(instance=user)
        return render(request, 'accounts/edit_profile.html', {'login':user,'form': form})

class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html/'
    next_page = './home.html'
