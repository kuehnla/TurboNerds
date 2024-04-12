from django.test import TestCase
from django.test import TestCase
from SchedulingApp.models import User


# Create your tests here.
class AdminTestCase(TestCase):

    def setUp(self):
        User.objects.create(name='Dean', email='<Dean@uwm.edu>', password='<Dean123>', phone_number='0123456789')

    def test_admin_creation(self):
        # Assert properties of admin user
        dean = User.objects.get(name='Dean')
        self.assertEqual(dean.email, '<Dean@uwm.edu>', msg=('Admin email incorrect: Expected: Dean@uwm.edu Was: ',
                                                            dean.email))
        self.assertEqual(dean.password, '<Dean123>', msg=('Admin password incorrect: Expected: Dean123 Was: ',
                                                          dean.password))
        self.assertEqual(dean.phone_number, '0123456789', msg=('Admin phone number incorrect: Expected:'
                                                               '0123456789 Was: ', dean.phone_number))


class InstructorTestCase(TestCase):

    def setUp(self):
        User.objects.create(name='Rock', email='<rock@uwm.edu>', password='<RockRules>', phone_number='4148675309')

    def test_instructor_creation(self):
        # Assert properties of instructor user using get request
        rock = User.objects.get(name='Rock')
        self.assertEqual(rock.email, '<rock@uwm.edu>', msg=('Instructor email incorrect: Expected:'
                                                            'rock@uwm.edu Was: ', rock.email))
        self.assertEqual(rock.password, '<RockRules>', msg=('Instructor password incorrect: Expected: RockRules Was: ',
                                                            rock.password))
        self.assertEqual(rock.phone_number, '4148675309', msg=('Instructor phone number incorrect: Expected: '
                                                               '4148675309 Was: ', rock.phone_number))


class TATestCase(TestCase):

    def setUp(self):
        User.objects.create(name='Tarun', email='<tarun@uwm.edu>', password='<TArun456>', phone_number='0987654321')

    def test_TA_creation(self):
        # Assert properties of TA user using get request
        tarun = User.objects.get(name='Tarun')
        self.assertEqual(tarun.email, '<tarun@uwm.edu>', msg=('TA email incorrect: Expected: tarun@uwm.edu Was: ',
                                                              tarun.email))
        self.assertEqual(tarun.password, '<TArun456>', msg=('TA password incorrect: Expected: TArun456 Was: ',
                                                            tarun.password))
        self.assertEqual(tarun.phone_number, '0987654321', msg=('TA phone number incorrect: Expected: 0987654321 Was: ',
                                                                tarun.phone_number))
