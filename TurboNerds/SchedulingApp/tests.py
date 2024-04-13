from django.test import TestCase
from django.utils import timezone

from .models import *


# Create your tests here.
class AdminTestCase(TestCase):

  def setUp(self):
    UserProfile.objects.create(first_name='Dean', last_name='Griffin', phone='414-444-1234',
                               email='Dean@uwm.edu',
                               login='dean', password='Dean123', is_instructor=False, is_assistant=False,
                               is_admin=True,
                               created_at=timezone.now())

  def test_admin_creation(self):
    # Assert properties of admin user
    dean = UserProfile.objects.get(first_name='Dean')
    self.assertEqual(dean.email, 'Dean@uwm.edu', msg=('Admin email incorrect: Expected: Dean@uwm.edu Was: ',
                                                      dean.email))
    self.assertEqual(dean.password, 'Dean123', msg=('Admin password incorrect: Expected: Dean123 Was: ',
                                                    dean.password))
    self.assertEqual(dean.phone, '414-444-1234', msg=('Admin phone number incorrect: Expected:'
                                                      '0123456789 Was: ', dean.phone))
    self.assertEqual(dean.last_name, 'Griffin', msg=('Admin last name incorrect: Expected: Griffin Was: ',
                                                     dean.last_name))


class InstructorTestCase(TestCase):

  def setUp(self):
    UserProfile.objects.create(last_name='Rock', email='rock@uwm.edu', password='RockRules', phone='414-444-1234',
                               login='rock', is_assistant=False, is_admin=False, is_instructor=True,
                               created_at=timezone.now())

  def test_instructor_creation(self):
    # Assert properties of instructor user using get request
    rock = UserProfile.objects.get(last_name='Rock')
    self.assertEqual(rock.email, 'rock@uwm.edu', msg=('Instructor email incorrect: Expected:'
                                                      'rock@uwm.edu Was: ', rock.email))
    self.assertEqual(rock.password, 'RockRules', msg=('Instructor password incorrect: Expected: RockRules Was: ',
                                                      rock.password))
    self.assertEqual(rock.phone, '414-444-1234', msg=('Instructor phone number incorrect: Expected: '
                                                      '414-444-1234 Was: ', rock.phone))


class TATestCase(TestCase):

  def setUp(self):
    UserProfile.objects.create(first_name='Tarun', last_name='Eapen', email='tarun@uwm.edu', password='TArun456',
                               phone='414-000-1234', is_assistant=True, is_instructor=False, is_admin=False,
                               created_at=timezone.now())

  def test_TA_creation(self):
    # Assert properties of TA user using get request
    tarun = UserProfile.objects.get(first_name='Tarun')
    self.assertEqual(tarun.email, 'tarun@uwm.edu', msg=('TA email incorrect: Expected: tarun@uwm.edu Was: ',
                                                        tarun.email))
    self.assertEqual(tarun.password, 'TArun456', msg=('TA password incorrect: Expected: TArun456 Was: ',
                                                      tarun.password))
    self.assertEqual(tarun.phone, '414-000-1234', msg=('TA phone number incorrect: Expected: 0987654321 Was: ',
                                                       tarun.phone))
