from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from ..models import *
from ..views import LoginView


class LoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(first_name='nate', last_name='stock', phone='414-444-1234',
                                        email='nates@uwm.edu', is_instructor=False, is_assistant=True,
                                        is_admin=False)

    def test_LoginDetails(self):
        request = self.factory.get('/login')
        request.user = self.user
        response = LoginView.as_view()
        self.assertEqual(response.status_code, 200)
