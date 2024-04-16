from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
<<<<<<< HEAD
    path('login/', LoginView.as_view(), name="login"),
=======

>>>>>>> b399895618a39f47409230b758dd399aa2fefabc
]
