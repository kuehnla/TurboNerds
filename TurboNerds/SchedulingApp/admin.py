from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Course
from .models import Section
from .models import Lab
from .models import UserProfile

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lab)
admin.site.register(UserProfile)