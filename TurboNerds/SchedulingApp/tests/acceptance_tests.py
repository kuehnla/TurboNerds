from django.test import TestCase, Client
from ..models import User, Course, Section, Lab
from django.urls import reverse


class CourseAssignmentTests(TestCase):

    def setUp(self):
        self.client = Client()

        # create a ta
        self.ta = User.objects.create(email="janedoe@uwm.edu", first_name="Jane", last_name="Doe",
                                      phone="1234567890", role="TA", is_instructor=False, is_assistant=True,
                                      is_admin=False)
        self.ta.set_password('hellowrld12!')
        self.ta.save()
        # create an instructor
        self.instructor = User.objects.create(email='johndoe@uwm.edu', first_name="John", last_name="Doe",
                                              phone="4147654321", role="Instructor",
                                              is_instructor=True, is_assistant=False, is_admin=False)
        self.instructor.set_password('hellowrld12!')
        self.instructor.save()
        # create a course
        self.course = Course.objects.create(department="CS", number="001", name="Intro to Compsci", semester="Fall")
        self.course.save()
        # create a section
        self.section = Section.objects.create(course=self.course, instructor=self.instructor, section_name="001",
                                              start_date="2024-09-04", end_date="2024-12-21", start_time="10:00:00",
                                              end_time="11:00:00", days="Tu Th")
        self.section.save()
        # create a lab
        self.lab = Lab.objects.create(assistant=self.ta, lab_name="lab 1", course=self.course, start_time="10:00:00",
                                      end_time="11:00:00", days="Mo We")
        self.lab.save()
        self.course_url = reverse('course_assignment')

    def test_response(self):
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, 302)

    def test_template(self):
        url = reverse('login')

        login_response = self.client.post(url, {'username': 'johndoe@uwm.edu', 'password': 'hellowrld12!'})

        self.assertEqual(login_response.status_code, 302)
        response = self.client.get(self.course_url)
        self.assertTemplateUsed(response, 'course/course_assignments.html')

    def test_information(self):
        url = reverse('login')

        login_response = self.client.post(url, {'username': 'johndoe@uwm.edu', 'password': 'hellowrld12!'})

        self.assertEqual(login_response.status_code, 302)
        response = self.client.get(self.course_url)
        self.assertContains(response, "Course Information")
        self.assertContains(response, "Intro to Compsci (CS 1)")

        self.assertContains(response, "Labs:")
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "lab 1")
        self.assertContains(response, "10 a.m. - 11 a.m.")

        self.assertContains(response, "Sections:")
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Sept. 4, 2024 - Dec. 21, 2024")
        self.assertContains(response, "Start Time: 10 a.m. - 11 a.m.")

    def test_not_contains(self):
        url = reverse('login')

        login_response = self.client.post(url, {'username': 'johndoe@uwm.edu', 'password': 'hellowrld12!'})

        self.assertEqual(login_response.status_code, 302)
        response = self.client.get(self.course_url)
        self.assertNotContains(response, "Compsci 300")
