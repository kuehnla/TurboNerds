from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Lab, Section, Course


class Users:

    def display_home(request):

        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_assistant:
            labs = request.user.lab_set.all()
            return render(request, 'ta_home.html', {'labs': labs, 'user': request.user,
                                                    'request': request})

        if request.user.is_instructor:
            sections = request.user.section_set.all()
            return render(request, 'instructor_home.html', {'sections': sections,
                                                            'user': request.user, 'request': request})

        if request.user.is_admin:
            courses = Course.objects.prefetch_related(
                Prefetch('lab_set', queryset=Lab.objects.order_by('start_time')),
                Prefetch('section_set', queryset=Section.objects.order_by('start_date'))
            ).all()
            return render(request, 'course/course_assignments.html', {'courses': courses})

        return HttpResponse("User not found or not authorized.")

    def display_other(request, email):

        if not request.user.is_authenticated:
            return redirect('login')

        user = User.objects.filter(email=email).first()

        if user is not None and user.is_assistant:
            labs = user.lab_set.all()
            return render(request, 'ta_home.html', {'labs': labs, 'user': user})

        if user is not None and user.is_instructor:
            sections = user.section_set.all()
            return render(request, 'instructor_home.html', {'sections': sections, 'user': user})

        return HttpResponse("User not found or not authorized.")
