from django.db import models


# Create your models here.


class User(models.Model):
  login = models.CharField(max_length=30)
  password = models.CharField(max_length=30)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.EmailField(max_length=254)
  phone = models.CharField(max_length=11)
  created_at = models.DateTimeField(auto_now_add=True)
  is_instructor = models.BooleanField()
  is_assistant = models.BooleanField()
  is_admin = models.BooleanField(default=False)


class Course:
  department = models.CharField(max_length=30)
  number = models.IntegerField()
  name = models.CharField(max_length=30)
  semester = models.CharField(max_length=30)


class Lab(models.Model):
  assistant = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'is_assistant': True}
  )
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  days = models.CharField(max_length=10, default="Mo We")


class Section(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  instructor = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'is_instructor': True}
  )
  start_date = models.DateField()
  end_date = models.DateField()
  start_time = models.TimeField()
  end_time = models.TimeField()
  days = models.CharField(max_length=10, default="Tu Th")
