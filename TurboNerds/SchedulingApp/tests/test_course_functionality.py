from django.test import TestCase, Client
from ..models import User, Course, Section, Lab
from django.urls import reverse
from datetime import date

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
        self.course = Course.objects.create(department="COMPSCI", number="001", name="Intro to Compsci", semester="Fall")
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
        self.assertContains(response, "Intro to Compsci (COMPSCI 1)")

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

class CourseCreationTests(TestCase):
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

        self.supervisor = User.objects.create(email="smith@uwm.edu", first_name = "John", last_name="Smith",
                                              phone="4142342343", role="Supervisor", is_instructor=False,
                                              is_assistant=False, is_admin=True)
        self.supervisor.set_password('hellowrld12!')
        self.supervisor.save()

    def test_course_creation_view(self):
        # Test the course creation view with valid data
        data = {
            'name': 'Test',
            'department': 'COMPSCI',
            'number': '001',
            'semester': 'Spring'
        }
        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('course_creation'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(name='Test').exists())

    def test_course_creation_invalid_semsester(self):
        # Test the course creation view with invalid data
        data = {
            'name': 'Test',
            'department': 'COMPSCI',
            'number': '101',
            'semester': 'Spring 2024'
        }

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('course_creation'), data)
        self.assertEqual(response.status_code, 200)  # Assert status code for form validation error
        self.assertFalse(Course.objects.filter(name='Test').exists())

    def test_course_creation_invalid_number(self):
        # Test the course creation view with invalid data
        data = {
            'name': 'Test',
            'department': 'COMPSCI',
            'number': 'abc',
            'semester': 'Spring 2024'
        }

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('course_creation'), data)
        self.assertEqual(response.status_code, 200)  # Assert status code for form validation error
        self.assertFalse(Course.objects.filter(name='Test').exists())

    def test_course_creation_invalid_name(self):
        # Test the course creation view with invalid data
        data = {
            'name': 'This is a very long string that exceeds 30 characters.',
            'department': 'COMPSCI',
            'number': '101',
            'semester': 'Spring 2024'
        }

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('course_creation'), data)
        self.assertEqual(response.status_code, 200)  # Assert status code for form validation error
        self.assertFalse(Course.objects.filter(name='This is a very long string that exceeds 30 characters.').exists())

    def test_course_creation_invalid_department(self):
        # Test the course creation view with invalid data
        data = {
            'name': 'test',
            'department': 'TEST',
            'number': '101',
            'semester': 'Spring 2024'
        }

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('course_creation'), data)
        self.assertEqual(response.status_code, 200)  # Assert status code for form validation error
        self.assertFalse(Course.objects.filter(name='test').exists())

class SectionCreationTests(TestCase):
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

        self.supervisor = User.objects.create(email="smith@uwm.edu", first_name="John", last_name="Smith",
                                              phone="4142342343", role="Supervisor", is_instructor=False,
                                              is_assistant=False, is_admin=True)
        self.supervisor.set_password('hellowrld12!')
        self.supervisor.save()

        self.course = Course.objects.create(department="COMPSCI", number="001", name="Intro to Compsci",
                                            semester="Fall")
        self.course.save()
    def test_section_creation(self):


        data = {'course': '1',
            'instructor': '2',
            'section_name': '001',
            'start_date': date(2024, 5, 31),
            'end_date': date(2024, 6, 14),
            'start_time': '15:49:02',
            'end_time': '16:17:13',
            'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 302)

    def test_invalid_course(self):
        data = {'course': self.course.name,
                'instructor': '2',
                'section_name': '001',
                'start_date': date(2024, 5, 31),
                'end_date': date(2024, 6, 14),
                'start_time': '15:49:02',
                'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

    def test_invalid_instructor(self):
        data = {'course': '1',
                'instructor': self.instructor.email,
                'section_name': '001',
                'start_date': date(2024, 5, 31),
                'end_date': date(2024, 6, 14),
                'start_time': '15:49:02',
                'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

    def test_invalid_section_name(self):
        data = {'course': '1',
                'instructor': '2',
                'section_name': 'Hello',
                'start_date': date(2024, 5, 31),
                'end_date': date(2024, 6, 14),
                'start_time': '15:49:02',
                'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Hello').exists())

    def test_invalid_start_date(self):
        data = {'course': '1',
                'instructor': '2',
                'section_name': '001',
                'start_date': '2024, 5, 31',
                'end_date': date(2024, 6, 14),
                'start_time': '15:49:02',
                'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

    def test_invalid_end_date(self):
        data = {'course': self.course.name,
                'instructor': '2',
                'section_name': '001',
                'start_date': date(2024, 5, 31),
                'end_date': '2024, 6, 14',
                'start_time': '15:49:02',
                'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

    def test_invalid_start_time(self):
        data = {'course': '1',
                'instructor': '2',
                'section_name': '001',
                'start_date': date(2024, 5, 31),
                'end_date': date(2024, 6, 14),
                'start_time': '154902',
                'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

    def test_invalid_end_time(self):
        data = {'course': '1',
                'instructor': '2',
                'section_name': '001',
                'start_date': date(2024, 5, 31),
                'end_date': date(2024, 6, 14),
                'start_time': '15:49:02',
                'end_time': '161713',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

    def test_invalid_days(self):
        data = {'course': '1',
                'instructor': '2',
                'section_name': '001',
                'start_date': date(2024, 5, 31),
                'end_date': date(2024, 6, 14),
                'start_time': '15:49:02',
                'end_time': '16:17:13',
                'days': ['Monday', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

    def test_null_data(self):
        data = {}
        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(section_name='Section 001').exists())

class LabCreationTests(TestCase):
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

        self.supervisor = User.objects.create(email="smith@uwm.edu", first_name="John", last_name="Smith",
                                              phone="4142342343", role="Supervisor", is_instructor=False,
                                              is_assistant=False, is_admin=True)
        self.supervisor.set_password('hellowrld12!')
        self.supervisor.save()

        self.course = Course.objects.create(department="COMPSCI", number="001", name="Intro to Compsci",
                                            semester="Fall")
        self.course.save()

    def test_lab_creation(self):


        data = {'course': '1',
            'assistant': '1',
            'lab_name': '001',
            'start_time': '15:49:02',
            'end_time': '16:17:13',
            'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('lab_creation'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Lab.objects.filter(lab_name='001').exists())

    def test_invalid_course(self):
        data = {'course': '2',
            'assistant': '1',
            'lab_name': '001',
            'start_time': '15:49:02',
            'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Lab.objects.filter(lab_name='001').exists())

    def test_invalid_assistant(self):
        data = {'course': '1',
            'assistant': '2',
            'lab_name': '001',
            'start_time': '15:49:02',
            'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Lab.objects.filter(lab_name='001').exists())

    def test_invalid_start_time(self):
        data = {'course': '1',
            'assistant': '1',
            'lab_name': '001',
            'start_time': '154902',
            'end_time': '16:17:13',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Lab.objects.filter(lab_name='001').exists())

    def test_invalid_end_time(self):
        data = {'course': '1',
            'assistant': '1',
            'lab_name': '001',
            'start_time': '15:49:02',
            'end_time': '161713',
                'days': ['Mo', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Lab.objects.filter(lab_name='001').exists())
    def test_invalid_days(self):
        data = {'course': '1',
            'assistant': '1',
            'lab_name': '001',
            'start_time': '15:49:02',
            'end_time': '16:17:13',
                'days': ['Monday', 'Fri']}

        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('section_creation'), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Lab.objects.filter(lab_name='001').exists())