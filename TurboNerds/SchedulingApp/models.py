from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class ROLES(models.TextChoices):
    Supervisor = "Supervisor"
    Instructor = "Instructor"
    TA = "TA"


# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, phone,
                    is_instructor, is_assistant, is_admin, is_superuser):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_instructor=is_instructor,
            is_assistant=is_assistant,
            is_admin=is_admin,
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name,
                         phone, is_instructor, is_assistant, is_admin):
        user = self.create_user(email, password, first_name, last_name, phone,
                                is_instructor, is_assistant, is_admin, is_superuser=True)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # password = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    role = models.CharField(max_length=20, choices=ROLES.choices, default="TA")
    is_instructor = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone',
                       'is_instructor', 'is_assistant', 'is_admin']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def is_staff(self):
        return self.is_admin


class Course(models.Model):
    department = models.CharField(max_length=30)
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    semester = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Lab(models.Model):
    assistant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_assistant': True}
    )
    lab_name = models.CharField(max_length=3, default="000")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.TimeField(default="HH:MM:SS")
    end_time = models.TimeField(default="HH:MM:SS")
    days = models.CharField(max_length=10, default="Mo")

    def __str__(self):
        return self.lab_name


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_instructor': True}
    )
    section_name = models.CharField(max_length=3, default="001")
    start_date = models.DateField(default="YYYY-MM-DD")
    end_date = models.DateField(default="YYYY-MM-DD")
    start_time = models.TimeField(default="HH:MM:SS")
    end_time = models.TimeField(default="HH:MM:SS")
    days = models.CharField(max_length=10, default="Tu/Th")

    def __str__(self):
        return self.section_name
