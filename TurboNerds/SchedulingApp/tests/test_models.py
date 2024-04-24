from django.test import TestCase

from ..models import *


# Create your tests here.
class AdminTestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name='Dean', last_name='Griffin', phone='414-444-1234',
                            email='Dean@uwm.edu', is_instructor=False, is_assistant=False,
                            is_admin=True)

    def test_admin_creation(self):
        # Assert properties of admin user
        dean = User.objects.get(first_name='Dean')
        self.assertEqual(dean.email, 'Dean@uwm.edu', msg=('Admin email incorrect: Expected: Dean@uwm.edu Was: ',
                                                          dean.email))
        self.assertEqual(dean.phone, '414-444-1234', msg=('Admin phone number incorrect: Expected:'
                                                          '0123456789 Was: ', dean.phone))
        self.assertEqual(dean.last_name, 'Griffin', msg=('Admin last name incorrect: Expected: Griffin Was: ',
                                                         dean.last_name))


class InstructorTestCase(TestCase):

    def setUp(self):
        User.objects.create(last_name='Rock', email='rock@uwm.edu', phone='414-444-1234',
                            is_assistant=False, is_admin=False, is_instructor=True,
                            )

    def test_instructor_creation(self):
        # Assert properties of instructor user using get request
        rock = User.objects.get(last_name='Rock')
        self.assertEqual(rock.email, 'rock@uwm.edu', msg=('Instructor email incorrect: Expected:'
                                                          'rock@uwm.edu Was: ', rock.email))
        self.assertEqual(rock.phone, '414-444-1234', msg=('Instructor phone number incorrect: Expected: '
                                                          '414-444-1234 Was: ', rock.phone))


class TATestCase(TestCase):

    def setUp(self):
        User.objects.create(first_name='Tarun', last_name='Eapen', email='tarun@uwm.edu', phone='414-000-1234',
                            is_assistant=True, is_instructor=False, is_admin=False,
                            )

    def test_TA_creation(self):
        # Assert properties of TA user using get request
        tarun = User.objects.get(first_name='Tarun')
        self.assertEqual(tarun.email, 'tarun@uwm.edu', msg=('TA email incorrect: Expected: tarun@uwm.edu Was: ',
                                                            tarun.email))
        self.assertEqual(tarun.phone, '414-000-1234', msg=('TA phone number incorrect: Expected: 0987654321 Was: ',
                                                           tarun.phone))


class CourseCreationTestCase(TestCase):

    def setUp(self):
        Course.objects.create(name='Intro to Software Engineering', semester='Spring', department='CS'
                              , number='361')

    def test_course_creation(self):
        current = Course.objects.get(name='Intro to Software Engineering')
        self.assertEqual(current.semester, 'Spring', msg=("Course semester incorrect: Expected: Spring Was: ",
                                                          current.semester))
        self.assertEqual(current.number, 361, msg=("Course number incorrect: Expected: 361 Was: ", current.number))
        self.assertEqual(current.department, 'CS', msg=("Course department incorrect: Expected: CS Was: ",
                                                        current.department))
