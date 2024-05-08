from django.db.models import Model
from django.test import TestCase, Client
from ..models import User, Course, Section, Lab
from ..supervisor import Supervisor


class CourseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            department="CS",
            number=535,
            name="Algorithms",
            semester="Spring"
        )
        self.course1 = Course.objects.create(
            department="CS",
            number=422,
            name="Good",
            semester="Spring 2024",
        )
        self.course.save()
        self.course1.save()

    def test_addedCourse(self):
        course = Course.objects.filter(number=535).first()
        self.assertIsNotNone(course, "Course does not exist")

    def test_notAddedCourse(self):
        course = Course.objects.filter(number=337).first()
        self.assertIsNone(course, "Course exists for some reason")

    def test_deleteCourse(self):
        self.assertIsNotNone(Course.objects.filter(number=535).first, "Course should exist")
        Course.objects.filter(number=535).delete()
        course = Course.objects.filter(number=535).first()
        self.assertIsNone(course, "Course should not be in database")

    def test_deleteOne(self):
        course = Course.objects.filter(number=535).first()
        self.assertIsNotNone(course, "Course should be in database")
        Course.objects.filter(number=535).delete()
        self.assertIsNone(Course.objects.filter(number=535).first(), "Course")
        self.assertIsNotNone(Course.objects.filter(number=422).first, "record should still persist in database")


class SupervisorCourseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = Supervisor()

    def test_courseCreation(self):
        self.supervisor.create_course("CS", 422, "good", "Spring 2024")
        self.assertIsNotNone(Course.objects.filter(name="good").first(), "course should be retrievable")

    def test_courseCreationDeletion(self):
        self.supervisor.create_course("CS", 458, "Computer Architecture", "Spring 2024")
        self.assertIsNotNone(Course.objects.filter(name="Computer Architecture").first(),
                             "course should be retrievable")
        course = Course.objects.filter(number=458).first()
        self.supervisor.delete_course(course)
        self.assertIsNone(Course.objects.filter(number=458).first(), "Should no longer be in database")

    def test_courseDeletionByNumber(self):
        self.supervisor.create_course("CS", 458, "Computer Architecture", "Spring 2024")
        self.assertIsNotNone(Course.objects.filter(number=458).first, "Course should be in database")
        self.supervisor.delete_course(458)
        course = Course.objects.filter(number=458).first()
        self.assertIsNone(course, "Should be able to delete by course number")
