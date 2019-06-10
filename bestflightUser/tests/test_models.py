from django.test import TestCase # noqa
from django.contrib.auth import get_user_model

from faker import Faker
fake = Faker()


class TestUserManager(TestCase):

    def test_create_user(self):
        User = get_user_model()
        email = fake.email()
        user = User.objects.create_user(email=email,
                                        password='sohard')
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_staff_user(self):
        User = get_user_model()
        email = fake.email()
        staff_user = User.objects.create_staffuser(email, 'staff_pass')
        self.assertEqual(staff_user.email, email)
        self.assertTrue(staff_user.is_active)
        self.assertTrue(staff_user.is_staff)
        self.assertFalse(staff_user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        email = fake.email()
        admin_user = User.objects.create_superuser(email, 'admin_pass')
        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
