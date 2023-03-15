from custom_auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from .factories import UserFactory


class TestUserViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(role=User.Role.PROFESSOR)

    def test_register(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("user-register")
        data = {
            "email": "test@test.by",
            "document_number": "1234876532209",
            "password": "elf-j437-fpwk4n2",
            "confirmation_password": "elf-j437-fpwk4n2",
        }
        response = self.client.post(url, data, format="json")
        user = User.objects.filter(email=data["email"]).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, User.Role.GUEST)
        self.assertIsNotNone(user.password)

    def test_register_existed_in_db(self):
        """
        Ensure we added password and change is_active status
        in db for existed user.
        """

        url = reverse("user-register")
        data = {
            "email": self.user.email,
            "document_number": self.user.document_number,
            "password": "sel09-user0-pard",
            "confirmation_password": "sel09-user0-pard",
        }

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_active)
        self.assertIsNotNone(self.user.password)

    def test_register_short_password(self):
        """
        Ensure correct reaction for short password.
        """
        url = reverse("user-register")
        data = {
            "email": self.user.email,
            "document_number": self.user.document_number,
            "password": "dbiw4",
            "confirmation_password": "dbiw4",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_not_match_password(self):
        """
        Ensure correct reaction for password fields didn't match.
        """
        url = reverse("user-register")
        data = {
            "email": self.user.email,
            "document_number": self.user.document_number,
            "password": "bui-abbr45-pofbe",
            "confirmation_password": "dbiw4",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirmation_password", response.data)

    def test_register_common_password(self):
        """
        Ensure correct reaction for password too common.
        """
        url = reverse("user-register")
        data = {
            "email": self.user.email,
            "document_number": self.user.document_number,
            "password": "123456789",
            "confirmation_password": "123456789",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


    def test_activate_email(self):
        pass


    def test_reset_password(self):
        """
        Ensure that authorised user can change their password.
        """
        self.user.email_confirmed = True
        self.user.is_active = True
        self.user.set_password("eib31wf-je345owb-pon")
        old_password = self.user.password
        self.client.force_authenticate(user=self.user)

        url = reverse("user-reset-password")
      
        data = {
            "old_password": "eib31wf-je345owb-pon",
            "password": "12sdf-456gh-789",
            "confirmation_password": "12sdf-456gh-789",
        }

        response = self.client.post(url, data, format="json")
        user = User.objects.filter(email=self.user.email).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user.password, old_password)
        