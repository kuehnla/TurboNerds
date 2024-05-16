from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import *


class TestUrls(SimpleTestCase):
    def test_login_urls_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_register_urls_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, ProfileModification.register)

    def test_edit_profile_urls_resolves(self):
        url = reverse('edit_profile', args=['nate@uwm.edu'])
        self.assertEqual(resolve(url).func, ProfileModification.edit_profile)

    def test_course_assignment_urls_resolves(self):
        url = reverse('course_assignment')
        self.assertEqual(resolve(url).func, CourseInformation.course_assignment)

    def test_user_information_urls_resolves(self):
        url = reverse('user_information')
        self.assertEqual(resolve(url).func, CourseInformation.read_information)

    def test_assign_ta_urls_resolves(self):
        url = reverse('assign_ta', args=['nate@uwm.edu'])
        self.assertEqual(resolve(url).func, CourseInformation.assign_tas)

    def test_logout_urls_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, Logins.logout_user)

    def test_supervisor_home_urls_resolves(self):
        url = reverse('supervisor_home')
        self.assertEqual(resolve(url).func, HomeViews.supervisor_home)

    def test_instructor_home_urls_resolves(self):
        url = reverse('instructor_home')
        self.assertEqual(resolve(url).func, HomeViews.instructor_home)

    def test_ta_home_urls_resolves(self):
        url = reverse('ta_home')
        self.assertEqual(resolve(url).func, HomeViews.ta_home)

