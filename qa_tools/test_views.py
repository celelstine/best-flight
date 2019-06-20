from unittest.mock import patch

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from bestflightUser.tests.factories import ProfileFactory

User = get_user_model()


class ViewsTest(APITestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.user = self.profile.user
        self.login_url = reverse('api:user-login')
        self.logout_url = reverse('api:user-logout')

        with patch.object(User, 'check_password', return_value=True) as _:
            payload = {
                'email': self.user.email,
                'password': 'may_right'
            }
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

            self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token

    def logout(self):
        self.client.post(self.logout_url)

    def test_create_test_user(self):
        url = reverse('qa:create_test_user')

        # this view should be access by admin only
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # make user an admin, logout and retry again
        self.user.is_superuser = True
        self.user.save()
        self.logout()

        with patch.object(User, 'check_password', return_value=True) as _:
            payload = {
                'email': self.user.email,
                'password': 'may_right'
            }
            self.client.defaults['HTTP_AUTHORIZATION'] = ''
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

            self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
            response = self.client.post(url)
            self.assertEqual(response.status_code,
                             status.HTTP_201_CREATED)
            email = response.data.get('email')
            password = response.data.get('password')
            test_user_exist = User.objects.filter(
                email=email).exists()
            self.assertTrue(test_user_exist)
            self.assertIsNotNone(password)
