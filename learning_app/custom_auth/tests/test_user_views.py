from datetime import datetime, timedelta

import time_machine
from custom_auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase

from ..tokens import account_activation_token
from .factories import UserFactory


class TestRegister(APITestCase):
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


class TestActivateEmail(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(role=User.Role.PROFESSOR, is_active=True)
        cls.user.set_password("eib31wf-je345owb-pon")
        cls.uid64 = urlsafe_base64_encode(force_bytes(cls.user.pk))
        cls.token = account_activation_token.make_token(cls.user)

    def test_activate_email(self):
        """
        Ensure that email was confirmed.
        """
        url = reverse("user-activate-email")
        data = {"uidb64": self.uid64, "token": self.token}
        response = self.client.get(url, data)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.email_confirmed)

    def test_activate_email_expire_token(self):
        """
        Ensure that email cannot be confirmed when token expired.
        """
        url = reverse("user-activate-email")
        data = {"uidb64": self.uid64, "token": self.token}
        exp_date = datetime.now() + timedelta(
            days=settings.PASSWORD_RESET_TIMEOUT + 1
        )
        with time_machine.travel(exp_date):
            response = self.client.get(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertFalse(self.user.email_confirmed)


class TestUserViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            role=User.Role.PROFESSOR, email_confirmed=True, is_active=True
        )
        cls.user.set_password("eib31wf-je345owb-pon")

    def test_reset_password(self):
        """
        Ensure that authorised user can change their password.
        """
        old_password = self.user.password
        self.client.force_authenticate(user=self.user)
        url = reverse("user-reset-password")
        data = {
            "old_password": "eib31wf-je345owb-pon",
            "password": "12sdf-456gh-789",
            "confirmation_password": "12sdf-456gh-789",
        }
        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.user.password, old_password)

    def test_reset_email(self):
        """
        Ensure that authorised user can change their email.
        """
        old_email = self.user.email
        self.client.force_authenticate(user=self.user)

        url = reverse("user-reset-email")

        data = {"email": "test_test@test.by"}

        response = self.client.post(url, data, format="json")
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.user.email, old_email)

    def test_update_profile(self):
        """
        Ensure that authorised user can change their first_name, last_name and document_number.
        """
        old_first_name = self.user.first_name
        old_last_name = self.user.last_name
        old_document_number = self.user.document_number
        self.client.force_authenticate(user=self.user)

        url = reverse("user-detail", args=(self.user.id,))
        data = {
            "first_name": "Test",
            "last_name": "Today",
            "document_number": "1235684390432",
        }

        response = self.client.patch(url, data, format="json")
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.user.first_name, old_first_name)
        self.assertNotEqual(self.user.last_name, old_last_name)
        self.assertNotEqual(self.user.document_number, old_document_number)
