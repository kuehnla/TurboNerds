from django.test import TestCase

from TurboNerds.SchedulingApp.models import Course


class CourseAddCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            department="CS",
            number=351,
            name="Algorithms",
            semester="Spring"
        )

    def addValidCourse(self):
        self.setUp()