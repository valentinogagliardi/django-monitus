from django.test import TestCase, SimpleTestCase
from django.core import mail
from model_bakery import baker


class Error403EmailsMiddleware(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make("User", email="some.user@dev.io")

    def setUp(self):
        self.client.force_login(self.user)

    def test_it_sends_email_to_admins(self):
        self.client.get("/secret-area/")
        self.assertEqual(mail.outbox[0].subject, "[Django] Got 403!")
        self.assertIn("juliana.crain@dev.io", mail.outbox[0].to)
        body = mail.outbox[0].body
        self.assertIn("127.0.0.1", body)
        self.assertIn("/", body)
        self.assertIn(self.user.username, body)
        self.assertIn(self.user.email, body)


class FailedLoginMiddlewareTest(SimpleTestCase):
    def _test_it_sends_email_to_admins(self):
        self.client.post("/login/", {"username": "brute", "password": "force"})
        self.assertEqual(mail.outbox[0].subject, "[Django] Failed login attempt")
        self.assertIn("juliana.crain@dev.io", mail.outbox[0].to)
        body = mail.outbox[0].body
        self.assertIn("127.0.0.1", body)
        self.assertIn("/login/", body)
