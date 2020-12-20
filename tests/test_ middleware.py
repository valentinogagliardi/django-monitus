from django.test import SimpleTestCase
from django.core import mail


class Error403EmailsMiddleware(SimpleTestCase):
    def test_it_sends_email(self):
        self.client.get("")
        self.assertEqual(mail.outbox[0].subject, "[Django] Got 403!")
        self.assertIn("juliana.crain@dev.io", mail.outbox[0].to)


class FailedLoginMiddlewareTest(SimpleTestCase):
    def test_it_sends_email_to_admins(self):
        self.client.post("/login/", {"username": "brute", "password": "force"})
        self.assertEqual(mail.outbox[0].subject, "[Django] Failed login attempt")
        self.assertIn("juliana.crain@dev.io", mail.outbox[0].to)
        body = mail.outbox[0].body
        self.assertIn("127.0.0.1", body)
        self.assertIn("/login/", body)
