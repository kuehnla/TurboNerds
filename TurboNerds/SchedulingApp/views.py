from django.shortcuts import render, redirect

from .forms import RegistrationForm, EditProfileForm, TaAssignment
from .models import User, Course, Section, Lab
from django.db.models import Prefetch
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


# Create your views here.
class HomeViews:
    def ta_home(request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'home.html')
    def instructor_home(request):
        if not request.user.is_authenticated:
            return redirect('login')
        name = "Instructor"
        return render(request, 'instructor_home.html', {"name": name})
    def supervisor_home(request):
        return render(request, 'supervisor_home.html', {})

class CourseInformation:
    from django.db.models import Prefetch
    from django.shortcuts import render
    from .models import Course, Lab, Section

    def course_assignment(request):
        if not request.user.is_authenticated:
            return redirect('login')
        courses = Course.objects.prefetch_related(
            Prefetch('lab_set', queryset=Lab.objects.order_by('start_time')),
            Prefetch('section_set', queryset=Section.objects.order_by('start_date'))
        ).all()
        return render(request, 'course/course_assignments.html', {'courses': courses})

    def assign_Tas(request,email):
        if not request.user.is_authenticated:
            return redirect('login')
        instructor = User.objects.get(email=email)
        course = Section.objects.filter(instructor=instructor).values_list('course', flat=True).first()
        if not course:
            messages.error(request, 'Instructor not associated with any courses.')
            return redirect('home')
        if request.method == 'POST':
            form = TaAssignment(course, request.POST)
            if form.is_valid():
                ta = form.cleaned_data['ta']
                lab = form.cleaned_data['lab']
                lab.assistant = ta
                lab.save()
                messages.success(request, 'TA successfully assigned to lab.')
                return redirect('course_assignment')
        else:
            form = TaAssignment(course)
        return render(request, 'course/ta_assignments.html', {'form': form})



    def read_information(request):
        if not request.user.is_authenticated:
            return redirect('login')
        users = User.objects.all()

        return render(request, 'course/user_information.html', {'users': users})



class ProfileModification:
    def register(request):

    #submitted = False
        if request.method == "POST":
            form = RegistrationForm(request.POST)

            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                role = form.cleaned_data['role']

                if role == 'Instructor':
                    user = User.objects.filter(email=email).update( is_instructor=True, is_admin=False,
                                           is_assistant=False)

                elif role == 'Supervisor':
                    user = User.objects.filter(email=email).update(is_instructor=False, is_admin=True,
                                           is_assistant=False)

                else:
                    user = User.objects.filter(email=email).update( is_instructor=False, is_admin=False,
                                           is_assistant=True)



                return redirect('supervisor_home')
        else:
            form = RegistrationForm()

        return render(request, 'accounts/register.html', {'form': form})


    def edit_profile(request,email):
        if not request.user.is_authenticated:
            return redirect('login')
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
                return redirect('instructor_home')
        else:

            user = User.objects.get(email=email)
            form = EditProfileForm(instance=user)
            return render(request, 'accounts/edit_profile.html', {'login':user,'form': form})

class Logins:

    def logout_user(request):
        logout(request)
        return redirect('home')


from django.http import HttpResponseRedirect

class CustomLoginView(LoginView):
    def get_success_url(self):
        # Get the user object after successful login
        user = self.request.user

        # Assuming you have a profile or a field in your user model indicating the role
        # You can replace this logic with your actual logic to determine the user's role
        if user.is_authenticated:
            if user.is_instructor:
                return reverse_lazy('instructor_home')
            elif user.is_admin:
                return reverse_lazy('supervisor_home')
            elif user.is_assistant:
                return reverse_lazy('home')
        # If the user's role is not defined, redirect to some default URL
        return reverse_lazy('default_home')  # You need to define this URL in your urls.py