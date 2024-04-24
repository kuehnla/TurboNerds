from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Course, Lab, User, Section
from ..forms import TaAssignment, RegistrationForm, EditProfileForm

class TestTaAssignmentForm(TestCase):
    def setUp(self):
        # Create a Course
        self.course = Course.objects.create(
            department='Computer Science',
            number=101,
            name='Introduction to Computer Science',
            semester='Spring 2024'
        )

        # Create Users
        self.instructor = get_user_model().objects.create(
            email='instructor@example.com',
            password='instructorpassword',
            first_name='Jane',
            last_name='Doe',
            phone='9876543210',
            is_instructor=True,
            is_assistant=False,
            is_admin=False
        )

        self.ta = get_user_model().objects.create(
            email='ta@example.com',
            password='tapassword',
            first_name='Alice',
            last_name='Smith',
            phone='5555555555',
            is_instructor=False,
            is_assistant=True,
            is_admin=False
        )

        # Create a Lab
        self.lab = Lab.objects.create(
            assistant=self.ta,
            lab_name='Lab 1',
            course=self.course,
            start_time=timezone.now(),
            end_time=timezone.now(),
            days='Mon, Wed'
        )

    def test_ta_assignment_form_valid(self):
        form_data = {
            'ta': self.ta,
            'lab': self.lab
        }
        form = TaAssignment(self.course, data=form_data)
        self.assertTrue(form.is_valid())

    def test_ta_assignment_form_invalid_ta(self):
        form_data = {
            'ta': self.instructor,  # This is an instructor, not a TA
            'lab': self.lab
        }
        form = TaAssignment(self.course, data=form_data)
        self.assertFalse(form.is_valid())

    def test_ta_assignment_form_invalid_lab(self):
        form_data = {
            'ta': self.ta,
            'lab': None  # No lab selected
        }
        form = TaAssignment(self.course, data=form_data)
        self.assertFalse(form.is_valid())

class RegistrationFormTest(TestCase):
    def test_form_valid(self):
        form = RegistrationForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'role': 'TA',
            'password1': 'helloWorld12',
            'password2': 'helloWorld12',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_passwords_dont_match(self):
        form = RegistrationForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'role': 'TA',
            'password1': 'password123',
            'password2': 'password456',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors.keys())

    def test_form_invalid_email_exists(self):

        form = RegistrationForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doeexample.com',
            'phone': '1234567890',
            'role': 'TA',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

class EditProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='john.doe@example.com',
            password='helloWorld12',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            role='TA',
        )

    def test_form_valid(self):
        form = EditProfileForm(data={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'phone': '9876543210',
        }, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'jane.doe@example.com')
        self.assertEqual(self.user.phone, '9876543210')

    def test_form_invalid_email_not_unique(self):
        user = User.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe1@example.com',
            phone='9876543210',
            role='TA'
        )

        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '9876543210',
        }

        form = EditProfileForm(data=form_data, instance=user)

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())


    def test_form_invalid_phone_not_unique(self):
        user = User.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe1@example.com',
            phone='9876543210',
            role='TA'
        )
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe1@example.com',
            'phone': '1234567890',
        }

        form = EditProfileForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors.keys())