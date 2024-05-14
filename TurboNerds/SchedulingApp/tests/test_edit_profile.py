from django.test import TestCase, Client
from ..models import User, Course, Section, Lab
from django.urls import reverse
from datetime import date

class ProfileEditTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.ta = User.objects.create(email="janedoe@uwm.edu", first_name="Jane", last_name="Doe",
                                      phone="1234567890", role="TA", is_instructor=False, is_assistant=True,
                                      is_admin=False)
        self.ta.set_password('hellowrld12!')
        self.ta.save()

    def test_edit_profile(self):
        data ={'first_name': 'Jane',
               'last_name': 'Doe',
               'email': 'janedoey@uwm.edu',
               'phone': '1234567890'
               }
        login_response = self.client.post(reverse('login'), {'username': 'janedoe@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)

        response = self.client.post(reverse('edit_profile', args = ['janedoe@uwm.edu']), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='janedoey@uwm.edu').exists())

    def test_invalid_phone_digits(self):
        data ={'first_name': 'Jane',
               'last_name': 'Doe',
               'email': 'janedoey@uwm.edu',
               'phone': 'abc'
               }
        login_response = self.client.post(reverse('login'), {'username': 'janedoe@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)

        response = self.client.post(reverse('edit_profile', args = ['janedoe@uwm.edu']), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phone number must contain only digits.")

    def test_invalid_phone_digit_length(self):
        data ={'first_name': 'Jane',
               'last_name': 'Doe',
               'email': 'janedoey@uwm.edu',
               'phone': '123'
               }
        login_response = self.client.post(reverse('login'), {'username': 'janedoe@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)

        response = self.client.post(reverse('edit_profile', args = ['janedoe@uwm.edu']), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phone number must be 10 digits long.")

class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        # create a ta
        self.ta = User.objects.create(email="janedoe@uwm.edu", first_name="Jane", last_name="Doe",
                                      phone="1234567890", role="TA", is_instructor=False, is_assistant=True,
                                      is_admin=False)
        self.supervisor = User.objects.create(email="smith@uwm.edu", first_name="John", last_name="Smith",
                                              phone="4142342343", role="Supervisor", is_instructor=False,
                                              is_assistant=False, is_admin=True)
        self.supervisor.set_password('hellowrld12!')
        self.supervisor.save()


    def test_register(self):
        data = {'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'janedoey@uwm.edu',
                'phone': '1234567890', 'role':'TA',
                'password1' : 'hellowrld12!', 'password2' : 'hellowrld12!'
                }
        login_response = self.client.post(reverse('login'), {'username': 'smith@uwm.edu', 'password': 'hellowrld12!'})
        self.assertEqual(login_response.status_code, 302)
        response = self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code, 302)