from django.db import models
from .models import *


class Supervisor(User):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.role = models.CharField(max_length=20, choices=ROLES.choices, default="Supervisor")
        self.is_admin = True

    @staticmethod
    def create_course(department, number, name, semester):
        try:
            Course.objects.get(department=department, number=number, semester=semester, name=name)
        except Course.DoesNotExist:
            course = Course.objects.create(department=department, number=number, name=name, semester=semester)
            return course
        else:
            return "This course already exists"

    @staticmethod
    def create_section(course, instructor, section_name, start_date, end_date, start_time, end_time, days):
        x = Section.objects.filter(course=course, instructor=instructor).first()
        if x is None:
            x = Section.objects.create(course=course, instructor=instructor, section_name=section_name,
                                       start_date=start_date, end_date=end_date, start_time=start_time,
                                       end_time=end_time, days=days)
            return x
        else:
            return "This section already exists"

    def create_user(self, email, first_name, last_name, password, phone, is_instructor, is_assistant, is_admin,
                    is_superuser):
        try:
            User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return MyUserManager.create_user(self.objects, email, password, first_name, last_name, phone, is_instructor,
                                             is_assistant, is_admin, is_superuser)
        else:
            return "User with given email already exists"

    @staticmethod
    def create_lab(assistant, lab_name, course, start_time, end_time, days):
        try:
            c = course.name
            Course.objects.get(name=c)
            Lab.objects.get(lab_name=lab_name)
        except Course.DoesNotExist:
            return "Cannot add lab to course that does not exist"
        except Lab.DoesNotExist:
            lab = Lab.objects.create(assistant=assistant, lab_name=lab_name, course=course, start_time=start_time,
                                     end_time=end_time,
                                     days=days)
            return lab
        else:
            return "This lab already exists"

    def delete_course(self, course):
        if not (self.is_admin or self.is_superuser):
            return "No permission to delete course"
        try:
            c = Course.objects.get(name=course.name)
        except Course.DoesNotExist:
            return "Cannot delete course that does not exist"
        else:
            c.delete()

    def delete_section(self, section):
        if not (self.is_admin or self.is_superuser):
            return "No permission to delete section"
        try:
            s = Section.objects.get(section_name=section.section_name)
        except Section.DoesNotExist:
            return "Cannot delete section that does not exist"
        else:
            s.delete()

    def delete_lab(self, lab):
        if not (self.is_admin or self.is_superuser):
            return "No permission to delete lab"
        try:
            lb = Lab.objects.get(lab_name=lab.lab_name)
        except Lab.DoesNotExist:
            return "Cannot delete lab that does not exist"
        else:
            lb.delete()

    def assign_assistant(self, lab, assistant):
        if not (self.is_admin or self.is_superuser):
            return "No permission to assign teaching assistant"
        try:
            ta = User.objects.get(email=assistant.email)
            lb = Lab.objects.get(lab_name=lab.lab_name)
        except User.DoesNotExist and Lab.DoesNotExist:
            return "Lab and TA must both exist"
        else:
            Lab.objects.filter(lab_name=lab.lab_name).update(assistant=assistant)

    def assign_instructor(self, section, instructor):
        if not (self.is_admin or self.is_superuser):
            return "No permission to assign instructor"
        try:
            instr = User.objects.get(email=instructor.email)
            sec = Section.objects.get(section_name=section.section_name)
        except User.DoesNotExist and Section.DoesNotExist:
            return "Lab and TA must both exist"
        else:
            Section.objects.filter(section_name=section.section_name).update(instructor=instructor)
