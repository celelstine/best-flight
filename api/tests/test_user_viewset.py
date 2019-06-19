import os

from unittest.mock import patch

from django.urls import reverse
from django.test import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from faker import Faker

from bestflightUser.tests.factories import (
    UserFactory,
    ProfileFactory
)

fake = Faker()
User = get_user_model()


class UserTest(APITestCase):
    """test for the user viewset"""
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('api:user-list')
        self.login_url = reverse('api:user-login')
        self.user = UserFactory()
        self.detail_url = reverse('api:user-detail',
                                  kwargs={"pk": '1'})

    def test_create_user(self):
        """test for signup route"""
        # required fields must be present ['first_name', 'last_name' and 'email'] # noqa
        payload = {
            "user": {}
        }
        response = self.client.post(self.create_url, payload,
                                    content_type='application/json')
        self.assertEqual(len(response.data.get('user')), 4)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # profile photo should upload an actual file
        photo = SimpleUploadedFile("photo.jpeg", "nice photo".encode(),
                                   content_type="image/jpeg")
        photo.size = (1048576 * settings.MAX_PHOTO_UPLOAD_SIZE_MB) - 10
        payload = {
            "user": {},
            "photo":  photo
        }
        response = self.client.post(self.create_url, payload)
        photo_reponse = response.data.get('photo')[0]
        self.assertEqual(
            photo_reponse,
            "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")  # noqa
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # profile photo size should at most th value MAX_PHOTO_UPLOAD_SIZE_MB
        with self.settings(MAX_PHOTO_UPLOAD_SIZE_MB=0.1):
            mock_file_path = os.path.join(os.getcwd(),
                                          './api/tests/sample_photo.png')
            with open(mock_file_path, 'rb') as file:
                payload["photo"] = file
                response = self.client.post(self.create_url, payload)
                photo_reponse = response.data.get('photo')[0]
                expect_response = "The max file size that can be uploaded is \
{}MB. Set MAX_PHOTO_UPLOAD_SIZE_MB env var to modify limit".format(settings.MAX_PHOTO_UPLOAD_SIZE_MB) # noqa
                self.assertEqual(photo_reponse, expect_response)
                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)

        # should signup when we provide the right data
        mock_file_path = os.path.join(os.getcwd(),'./api/tests/sample_photo.png') # noqa
        with open(mock_file_path, 'rb') as file:
            name = fake.name().split()
            email = fake.email()
            payload = {
                'user.email': [email],
                'user.first_name': [name[0]],
                'user.last_name': [name[1]],
                'user.password': [name[1]],
                'photo': [file],
                # the file is now empty so we need to open it again
                'international_passport': [open(mock_file_path, 'rb')]
            }
            response = self.client.post(self.create_url, payload)
            data = response.data
            user_data = response.data.get('user')
            self.assertEqual(user_data.get('email'), email)
            self.assertEqual(user_data.get('first_name'), name[0])
            self.assertIn('token', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        with patch.object(User, 'check_password', return_value=True) as _:
            ProfileFactory(user=self.user)
            payload = {
                'email': self.user.email,
                'password': 'may_right'
            }
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

            self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
            response = self.client.get(self.create_url)
            self.assertEqual(response.data, 'You can not view a list of users')
            self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED) # noqa

    def test_retrieve(self):
        with patch.object(User, 'check_password', return_value=True) as _:
            ProfileFactory(user=self.user)
            payload = {
                'email': self.user.email,
                'password': 'may_right'
            }
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

            self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
            response = self.client.get(self.detail_url)
            self.assertEqual(response.data, 'Retrieve action not allowed.')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # noqa

    def test_partial_update(self):
        with patch.object(User, 'check_password', return_value=True):
            profile = ProfileFactory(user=self.user)
            payload = {
                'email': self.user.email,
                'password': 'may_right'
            }
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        email = fake.email()
        payload = {
            'user': {
                'email': email,
            }
        }
        url = reverse('api:user-detail', kwargs={"pk": profile.id})
        """
        DRF select the parse base off the contentType of the request
        so we set this to json as the default is octet-stream which expects
        a file in the request
        """
        response = self.client.patch(url, payload,
                                     content_type='application/json')
        user = response.data.get('user')
        self.assertEqual(user.get('email'), email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # always update the auth profile irrespective of the profile id passed
        another_profile = ProfileFactory()
        url = reverse('api:user-detail', kwargs={"pk": another_profile.id})
        self.assertNotEqual(response.data.get('id'), another_profile.id)
        self.assertEqual(response.data.get('id'), str(profile.id))

    def test_destroy(self):
        with patch.object(User, 'check_password', return_value=True) as _:
            ProfileFactory(user=self.user)
            payload = {
                'email': self.user.email,
                'password': 'may_right'
            }
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

            self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.data, 'coming up soon!!!')
            self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE) # noqa

    def test_login(self):
        # email and password are required
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.data, 'Please provide both email and password.') # noqa
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # # wrong email
        payload = {
            'email': "w{}".format(self.user.email),
            'password': 'may_right'
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.data, 'Wrong email or password.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # # right email and wrong pass
        payload['email'] = self.user.email
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.data, 'Wrong email or password.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # right credentials but without a profile
        with patch.object(User, 'check_password', return_value=True) as _:
            response = self.client.post(self.login_url, payload)
            self.assertIn('you don\'t have a profile', response.data)
            self.assertEqual(response.status_code, status.HTTP_424_FAILED_DEPENDENCY) # noqa

            # let create a profile for this user
            ProfileFactory(user=self.user)
            response = self.client.post(self.login_url, payload)
            data = response.data
            user_data = response.data.get('user')
            self.assertEqual(user_data.get('email'), self.user.email)
            self.assertIn('token', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # set token to use for authentication
            token = data.get('token')

        # can not login twice
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        response = self.client.post(self.login_url, payload)
        self.assertIn('you have an active session already.', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        url = reverse('api:user-logout')
        with patch.object(User, 'check_password', return_value=True) as _:
            ProfileFactory(user=self.user)
            payload = {
                'email': self.user.email,
                'password': 'may_right'
            }
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

            self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
            response = self.client.post(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # authenticated users can not logout
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
