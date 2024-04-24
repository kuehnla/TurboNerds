from django.db import models
from models import User, Course, ROLES, MyUserManager, Lab, Section


class Supervisor(User):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_supervisor': True})
    role = models.CharField(max_length=20, choices=ROLES.choices, default="Supervisor")
    is_admin = models.BooleanField(default=True)


    @staticmethod
    def create_course(department, number, name, semester):
        try:
            Course.objects.get(department, number, semester, name)
        except Course.DoesNotExist:
            course = Course(department, number, name, semester)
            course.save()
            return course
        else:
            return "This course already exists"


    def create_user(self, email, first_name, last_name, password,, phone, role, is_instructor, is_assistant, is_admin,
                    is_superuser):
        try:
            User.objects.get(email)
        except User.DoesNotExist:
            return MyUserManager.create_user(self.objects, email, password, first_name, last_name, phone, is_instructor,
                                             is_assistant, is_admin, is_superuser)
        else:
            return "User with given email already exists"

    @staticmethod
    def create_lab(lab_name, course, start_time, end_time, days):
        try:
            Course.objects.get(course.name)
        except Course.DoesNotExist:
            return "Cannot add lab to course that does not exist"
        else:
            lab = Lab(lab_name, course, start_time, end_time, days)
            lab.save()
            return lab

    @staticmethod
    def delete_course(course):
        try:
            c = Course.objects.get(course.name)
        except Course.DoesNotExist:
            return "Cannot delete course that does not exist"
        else:
            c.delete()

    @staticmethod
    def delete_lab(lab):
        try:
            l = Lab.objects.get(lab.name)
        except Course.DoesNotExist:
            return "Cannot delete lab that does not exist"
        else:
            l.delete()

    @staticmethod
    def assign_assistant(self, lab, assistant):
        try:
            ta = User.objects.get(email=assistant.email)
            l = Lab.objects.get(lab.lab_name)
        except User.DoesNotExist and Lab.DoesNotExist:
            return "Lab and TA must both exist"
        else:
            l.assistant = models.ForeignKey(ta, on_delete=models.CASCADE)

    @staticmethod
    def assign_instructor(self, section, instructor):
        try:
            instr = User.objects.get(email=instructor.email)
            sec = Section.objects.get(section.name)
        except User.DoesNotExist and Section.DoesNotExist:
            return "Lab and TA must both exist"
        else:
            sec.instructor = models.ForeignKey(instr, on_delete=models.CASCADE)











