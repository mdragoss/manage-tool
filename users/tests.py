import unittest
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from users.models import User
from users.views import RegisterView, LogInView
import datetime
from rest_framework import status


class UserTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='user@mail.com',
            password='password',
            first_name='First',
            last_name='Last',
            date_joined=datetime.datetime(
                2023, 12, 26, 18, 23, 26, 139731, tzinfo=datetime.timezone.utc
            ),
        )

    def test_user(self):
        test_user = User.objects.get(email='user@mail.com')
        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.get_full_name(), 'First Last')

    def test_register(self):
        request = self.factory.post(
            path='auth/register/',
            data={
                'email': 'register@mail.com',
                'password': 'string',
                'first_name': 'New',
                'last_name': 'User',
            },
            format='json',
        )
        view = RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                'email': 'register@mail.com',
                'first_name': 'New',
                'last_name': 'User',
            },
        )

    @unittest.skip('Bad')
    def test_login_success(self):
        data = {'email': self.user.email, 'password': self.user.password}
        request = self.factory.post(
            path='auth/login/',
            data=data,
            format='json',
        )
        view = LogInView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        data = {'email': 'wronguser@mail.com', 'password': 'wrongpassword'}
        request = self.factory.post(
            path='auth/login/',
            data=data,
            format='json',
        )
        view = LogInView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
