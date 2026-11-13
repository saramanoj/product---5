<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.
=======
from django.test import TestCase

# Create your tests here.
>>>>>>> d0b9c95965475f9b14f001bb4aef49392b2e69f7

# placement officer registration


from django.core.cache import cache
from rest_framework.test import APITestCase


class RegistrationOtpTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_email_otp_verifies_with_case_and_whitespace_variations(self):
        send_response = self.client.post(
            "/api/registration/send-otp/",
            {"type": "email", "value": " User@Example.com "},
            format="json",
        )

        self.assertEqual(send_response.status_code, 200)

        verify_response = self.client.post(
            "/api/registration/verify-otp/",
            {
                "type": "email",
                "value": "user@example.com",
                "otp": send_response.data["demo_otp"],
            },
            format="json",
        )

        self.assertEqual(verify_response.status_code, 200)
        self.assertTrue(verify_response.data["verified"])

    def test_incorrect_otp_returns_actionable_error(self):
        self.client.post(
            "/api/registration/send-otp/",
            {"type": "mobile", "value": "9876543210"},
            format="json",
        )

        verify_response = self.client.post(
            "/api/registration/verify-otp/",
            {"type": "mobile", "value": "9876543210", "otp": "000000"},
            format="json",
        )

        self.assertEqual(verify_response.status_code, 400)
        self.assertEqual(
            verify_response.data["message"],
            "Incorrect OTP. Please check the code and try again.",
        )



