from django.shortcuts import render, redirect
from .models import User


class Users:

    def display_home(request):

        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_assistant:
            labs = request.user.lab_set.all()
            return render(request, 'ta_home.html', {'labs': labs, 'user': request.user, 'request': request})

        if request.user.is_instructor:
            sections = request.user.section_set.all()
            return render(request, 'instructor_home.html', {'sections': sections, 'user': request.user})

        if request.user.is_admin:
            return render(request, 'supervisor_home.html', {})

    def display_other(request, email):

        if not request.user.is_authenticated:
            return redirect('login')

        user = User.objects.filter(email=email).first()
        labs = user.lab_set.all()

        return render(request, 'ta_home.html', {'labs': labs, 'user': user})
