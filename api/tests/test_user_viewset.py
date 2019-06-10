import os

from django.urls import reverse
from django.test import Client
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from faker import Faker


fake = Faker()


class UserTest(APITestCase):
    """test for the user viewset"""
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('api:user-list')
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
        response = self.client.get(self.create_url)
        self.assertEqual(response.data, 'You can not view a list of users')
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data, 'coming up soon!!!')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE) # noqa

    def test_update(self):
        response = self.client.put(self.detail_url)
        self.assertEqual(response.data, 'coming up soon!!!')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE) # noqa

    def test_partial_update(self):
        response = self.client.patch(self.detail_url)
        self.assertEqual(response.data, 'coming up soon!!!')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE) # noqa

    def test_destroy(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.data, 'coming up soon!!!')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE) # noqa
