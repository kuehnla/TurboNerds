from django.shortcuts import render, redirect
from django.db import models
from .models import User, Course, ROLES, MyUserManager, Lab, Section





class Users:
    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     self.role = models.CharField(max_length=20, choices=ROLES.choices, default="Supervisor")
    #     self.is_admin = True
    #     self.id = 1

    def display_home(request):

        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_assistant:
            labs = request.user.lab_set.all()
            return render(request, 'home.html', {'labs': labs, 'user': request.user})

        if request.user.is_instructor:
            name = "Instructor"
            return render(request, 'instructor_home.html', {"name": name})

        if request.user.is_admin:
            return render(request, 'supervisor_home.html', {})
