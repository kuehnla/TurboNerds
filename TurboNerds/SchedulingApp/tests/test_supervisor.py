from django.test import TestCase
from ..supervisor import Supervisor
from ..models import *


class TestSupervisor(TestCase):

    def setUp(self):
        self.supervisor = User.objects.create(email='JaneD@uwm.edu', first_name='Jane', last_name='Doe',
                                              password='JD456', phone='111-111-1111', role='Supervisor',
                                              is_instructor=False, is_assistant=False, is_admin=True)
        Supervisor.create_course(department='CS', number=361, name='Intro to Software Engineering', semester='Spring')
        cs361 = Course.objects.get(department='CS')
        rock = User.objects.create(last_name='Rock', email='rock@uwm.edu', phone='414-444-1234',
                                   is_assistant=False, is_admin=False, is_instructor=True)
        Supervisor.create_section(course=cs361, instructor=rock, section_name='101',
                                  start_date=2024 - 1 - 22,
                                  end_date=2024 - 5 - 18, start_time='09:30:00', end_time='10:20:00',
                                  days='Tu Th')
        Supervisor.create_lab(lab_name='803', course=cs361, start_time='2:30:00', end_time='04:20:00',
                              days='Tu')

    def test_basic_creation(self):
        c = Course.objects.filter(department='CS', number=361).first()
        self.assertEqual(c.__str__(), 'Intro to Software Engineering', msg="Course not correct")
        lab = Lab.objects.get(lab_name='803')
        self.assertEqual(lab.__str__(), '803', msg="Lab not correct")
        s = Section.objects.filter(days='Tu Th', section_name=101).first()
        self.assertEqual(s.__str__(), '101', msg="Section not correct")

    def test_creating_duplicate(self):
        str1 = Supervisor.create_course(department='CS', number=361, name='Intro to Software Engineering',
                                        semester='Spring')
        self.assertEqual(str1.__str__(), 'This course already exists')
        cs361 = Course.objects.get(department='CS')
        rock = User.objects.get(last_name='Rock')
        str2 = Supervisor.create_section(course=cs361, instructor=rock, section_name='101',
                                         start_date=2024 - 1 - 22,
                                         end_date=2024 - 5 - 18, start_time='09:30:00', end_time='10:20:00',
                                         days='Tu Th')
        self.assertEqual(str2.__str__(), 'This course already exists')
        str3 = Supervisor.create_lab(lab_name='803', course=cs361, start_time='2:30:00', end_time='04:20:00',
                                     days='Tu')
        self.assertEqual(str3.__str__(), 'This course already exists')

    def test_model_deletion(self):
        lab = Lab.objects.get(lab_name='803')
        self.supervisor.delete_lab(lab)
        self.assertRaises(Lab.objects.DoesNotExist, Lab.objects.get, lab_name='803', msg='Should have raised exception')
        sect = Section.objects.get(section_name='101')
        self.supervisor.delete_section(sect)
        self.assertRaises(Section.objects.DoesNotExist, Section.objects.get, section_name='101',
                          msg='Should have raised exception')
        c = Course.objects.get(course_name='Intro to Software Engineering')
        self.supervisor.delete_course(c)
        self.assertRaises(Course.objects.DoesNotExist, Course.objects.get, course_name='Intro to Software Engineering',
                          msg='Should have raised exception')

    def

