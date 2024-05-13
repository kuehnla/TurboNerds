from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', views.Logins.logout_user, name='logout'),

    path('home/', views.HomeViews.home, name='home'),
    path('', views.HomeViews.home, name='home'),
    path('<str:email>', views.HomeViews.otherhome, name='otherhome'),

    path('register/', views.ProfileModification.register, name='register'),
    path('edit_information/<str:email>', views.ProfileModification.edit_profile, name='edit_profile'),
    path('course_information/', views.CourseInformation.course_assignment, name='course_assignment'),
    path('user_information/<str:email>', views.CourseInformation.read_information, name='user_information'),
    path('assign_ta/<str:email>', views.CourseInformation.assign_Tas, name='assign_ta'),
    path('delete/<str:email>', views.ProfileModification.delete, name='delete'),
    path('success/', views.SuccessEdit.success, name='success')
]
