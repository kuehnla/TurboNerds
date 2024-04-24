from django.test import TestCase, Client
from django.urls import reverse
from ..models import *


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.assign_ta_url = reverse('assign_ta', args=['test@uwm.edu'])
        self.test_TA1 = User.objects.create(email='test1@uwm.edu', first_name='hello', last_name='world',
                                            password='Turbo123',
                                            phone='1234567890', role='TA', is_assistant=True, is_instructor=False,
                                            is_admin=False)
        self.test_TA2 = User.objects.create(email='test2@uwm.edu', first_name='hello', last_name='world',
                                            password='Turbo123',
                                            phone='1234567890', role='TA', is_assistant=True, is_instructor=False,
                                            is_admin=False)
        self.test_course = Course.objects.create(department='CS', number=361, name='Software Stuff',
                                                 semester='Fall')

    def test_assign_Tas(self):
        response = self.client.get(self.assign_ta_url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'course/ta_assignments.html')

    def test_assign_Tas__POST_add_ta(self):
        Lab.objects.create(assistant=self.test_TA2, lab_name='Test Lab', course=self.test_course,
                           start_time='10:00:00', end_time='11:00:00', days='Mo We')

        response = self.client.post(self.assign_ta_url, {
            'assistant': self.test_TA1,
            'lab_name': 'Test Lab',
            'course': self.test_course,
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'days': 'Mo We'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.test_course.lab_set.first().lab_name, 'Test Lab')
        self.assertEqual(self.test_course.lab_set.first().assistant.email, 'test1@uwm.edu')

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

    def test_course_assignment_display(self):
        response = self.client.get(reverse('course_assignment'))

        self.assertEqual(response.status_code, 302)
