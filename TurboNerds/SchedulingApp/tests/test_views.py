from django.test import TestCase, Client
from django.urls import reverse
from ..models import *


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.assign_ta_url = reverse('assign_ta', args=['test@uwm.edu'])
        User.objects.create_user(email='test@uwm.edu', first_name= 'hello', last_name= 'world', password='Turbo123',
                                 phone='1234567890', role='TA', is_active=True, is_instructor=False, is_admin=False)
        


    def test_assign_Tas(self):
        response = self.client.get(self.assign_ta_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'course/ta_assignments.html')

    def test_ta_home(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instructor_home.html')

    def test_instructors_home(self):
        response = self.client.get(reverse('instructor_home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instructor_home.html')

    def test_supervisor_home(self):
        response = self.client.get(reverse('supervisor_home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'supervisor_home.html')
