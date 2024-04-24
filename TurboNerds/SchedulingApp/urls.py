from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.HomeViews.ta_home, name='home'),
    path('ta_home/', views.HomeViews.ta_home, name='home'),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('register/', views.ProfileModification.register, name='register'),
    path('edit_information/<str:email>', views.ProfileModification.edit_profile, name='edit_profile'),
    path('course_information/', views.CourseInformation.course_assignment, name='course_assignment'),
    path('user_information/', views.CourseInformation.read_information, name='user_information'),
    path('assign_ta/<str:email>', views.CourseInformation.assign_Tas, name='assign_ta'),
    path('instructor_home/', views.HomeViews.instructor_home, name='instructor_home'),
    path('logout/', views.Logins.logout_user, name='logout'),
    path('supervisor_home/', views.HomeViews.supervisor_home, name='supervisor_home'),
]
