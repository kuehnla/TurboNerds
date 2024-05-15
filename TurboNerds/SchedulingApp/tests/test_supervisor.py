from django.test import TestCase
from ..supervisor import Supervisor
from ..models import *


class TestSupervisor(TestCase):

    def setUp(self):
        self.supervisor = User.objects.create(email='JaneD@uwm.edu', first_name='Jane', last_name='Doe',
                                              password='JD456', phone='111-111-1111', role='Supervisor',
                                              is_instructor=False, is_assistant=False, is_admin=True)
        cs361 = Supervisor.create_course(department='CS', number=361, name='Intro to Software Engineering',
                                         semester='Spring')

        rock = User.objects.create(last_name='Rock', email='rock@uwm.edu', phone='414-444-1234',
                                   is_assistant=False, is_admin=False, is_instructor=True)
        Supervisor.create_section(course=cs361, instructor=rock, section_name='101', start_date="2024-1-22",
                                  end_date="2024-5-18", start_time='9:30:00', end_time='10:20:00',
                                  days='Tu Th')
        ta = User.objects.create(email='ta@uwm.edu', first_name='Josh', last_name='Guy', password='JoshGuy',
                                 phone='444-444-4444', role='TA', is_assistant=True, is_admin=False, is_superuser=False)
        Supervisor.create_lab(assistant=ta, lab_name='803', course=cs361, start_time='2:30:00', end_time='4:20:00',
                              days='Tu')

    def test_basic_creation(self):
        c = Course.objects.filter(department='CS', number=361).first()
        self.assertEqual(c.__str__(), 'Intro to Software Engineering', msg="Course not correct")
        lab = Lab.objects.get(lab_name='803')
        self.assertEqual(lab.__str__(), '803', msg="Lab not correct")
        s = Section.objects.get(section_name='101')
        self.assertEqual(s.__str__(), '101', msg="Section not correct")

    def test_creating_duplicate(self):
        str1 = Supervisor.create_course(department='CS', number=361, name='Intro to Software Engineering',
                                        semester='Spring')
        self.assertEqual(str1.__str__(), 'This course already exists')
        cs361 = Course.objects.get(department='CS')
        rock = User.objects.get(last_name='Rock')
        str2 = Supervisor.create_section(course=cs361, instructor=rock, section_name='101',
                                         start_date="2024 - 1 - 22",
                                         end_date="2024 - 5 - 18", start_time='09:30:00', end_time='10:20:00',
                                         days='Tu Th')
        self.assertEqual(str2.__str__(), 'This section already exists')
        ta = User.objects.get(last_name='Guy')
        str3 = Supervisor.create_lab(assistant=ta, lab_name='803', course=cs361, start_time='2:30:00',
                                     end_time='04:20:00',
                                     days='Tu')
        self.assertEqual(str3.__str__(), 'This lab already exists')

    def test_model_deletion(self):
        lab = Lab.objects.get(lab_name='803')
        Supervisor.delete_lab(self.supervisor, lab)
        self.assertEqual(Supervisor.delete_lab(self.supervisor, lab), "Cannot delete lab that does not exist")
        sect = Section.objects.get(section_name='101')
        Supervisor.delete_section(self.supervisor, sect)
        self.assertEqual(Supervisor.delete_section(self.supervisor, sect), "Cannot delete section that does not exist")
        c = Course.objects.get(name='Intro to Software Engineering')
        Supervisor.delete_course(self.supervisor, c)
        self.assertEqual(Supervisor.delete_course(self.supervisor, c), "Cannot delete course that does not exist")

    def test_multiple_sections(self):
        chris = User.objects.create(last_name='Chris', email='chris@uwm.edu', phone='926-527-8275',
                                    is_assistant=False, is_admin=False, is_instructor=True)
        cs361 = Course.objects.get(name='Intro to Software Engineering')
        x = Supervisor.create_section(course=cs361, instructor=chris, section_name='101', start_date="2024-1-22",
                                      end_date="2024-5-18", start_time='09:30:00', end_time='10:20:00',
                                      days='Tu Th')
        self.assertNotEqual(x.__str__(), 'This section already exists')

    def test_multiple_course(self):
        self.assertNotEqual(Supervisor.create_course(department='CS', number=361, name='Intro to Software Engineering',
                                                     semester='Fall'), "This course already exists")
        self.assertEqual(Supervisor.create_course(department='CS', number=361, name='Intro to Software Engineering',
                                                  semester='Spring'), "This course already exists")

    def test_userCreate(self):
        supervisor = Supervisor()
        supervisor.create_user(email="email@uwm.edu", first_name="Teaching", last_name="Assistant",
                               password="Turbo123", phone="2222222222", is_instructor=False,
                               is_assistant=False, is_admin=True, is_superuser=False)
        self.assertIsNotNone(User.objects.filter(last_name="Assistant").first(), "user should exist but doesn't")


class TestAssignments(TestCase):

    def setUp(self):
        self.supervisor = User.objects.create(email='Jane@uwm.edu', first_name='Jane', last_name='Doe',
                                              password='JD456', phone='111-111-1111', role='Supervisor',
                                              is_instructor=False, is_assistant=False, is_admin=True)
        cs361 = Supervisor.create_course(department='CS', number=361, name='Intro to Software Engineering',
                                         semester='Fall')
        User.objects.create(last_name='Rock', email='rock@uwm.edu', phone='414-444-1234',
                            is_assistant=False, is_admin=False, is_instructor=True)
        Supervisor.create_section(course=cs361, instructor=None, section_name='101', start_date="2024-1-22",
                                  end_date="2024-5-18", start_time='9:30:00', end_time='10:20:00',
                                  days='Tu Th')
        User.objects.create(email='ta@uwm.edu', first_name='Josh', last_name='Guy', password='JoshGuy',
                            phone='444-444-4444', role='TA', is_assistant=True, is_admin=False, is_superuser=False)
        Supervisor.create_lab(lab_name='803', course=cs361, assistant=None, start_time='2:30:00', end_time='4:20:00',
                              days='Tu')

    def test_permissions(self):
        rock = User.objects.get(last_name='Rock')
        lb = Lab.objects.get(lab_name='803')
        ta = User.objects.get(email='ta@uwm.edu')
        sect = Section.objects.get(section_name='101')
        self.assertEqual(Supervisor.assign_assistant(rock, lb, ta), "No permission to assign teaching assistant")
        self.assertEqual(Supervisor.assign_instructor(ta, sect, rock), "No permission to assign instructor")

    def test_basic_ta_assignment(self):
        lb = Lab.objects.get(lab_name='803')
        ta = User.objects.get(email='ta@uwm.edu')
        Supervisor.assign_assistant(self.supervisor, lab=lb, assistant=ta)
        new_lb = Lab.objects.get(lab_name='803')
        self.assertEqual(new_lb.assistant.__str__(), ta.__str__())

    def test_basic_instructor_assignment(self):
        rock = User.objects.get(last_name='Rock')
        sect = Section.objects.get(section_name='101')
        Supervisor.assign_instructor(self.supervisor, section=sect, instructor=rock)
        new_sect = Section.objects.get(section_name='101')
        self.assertEqual(new_sect.instructor.__str__(), rock.__str__())

    def test_reassign_assistant(self):
        lb = Lab.objects.get(lab_name='803')
        ta = User.objects.get(email='ta@uwm.edu')
        Supervisor.assign_assistant(self.supervisor, lab=lb, assistant=ta)
        new_ta = User.objects.create(email='joe@uwm.edu', first_name='Joe', last_name='Joe', password='JoeJoe',
                                     phone='111-111-1111', role='TA', is_assistant=True, is_admin=False,
                                     is_superuser=False)
        Supervisor.assign_assistant(self.supervisor, lab=lb, assistant=new_ta)
        new_lb = Lab.objects.get(lab_name='803')
        self.assertEqual(new_lb.assistant.__str__(), new_ta.__str__())

    def test_reassign_instructor(self):
        rock = User.objects.get(last_name='Rock')
        sect = Section.objects.get(section_name='101')
        Supervisor.assign_instructor(self.supervisor, section=sect, instructor=rock)
        new_rock = User.objects.create(last_name='new_Rock', email='newRock@uwm.edu', phone='867-787-9267',
                                       is_assistant=False, is_admin=False, is_instructor=True)
        Supervisor.assign_instructor(self.supervisor, section=sect, instructor=new_rock)
        new_sect = Section.objects.get(section_name='101')
        self.assertEqual(new_sect.instructor.__str__(), new_rock.__str__())
