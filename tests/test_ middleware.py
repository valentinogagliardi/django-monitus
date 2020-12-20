from django.test import SimpleTestCase
from django.core import mail


class Error403EmailsMiddleware(SimpleTestCase):
    def test_it_sends_email(self):
        self.client.get("")
        self.assertEqual(mail.outbox[0].subject, "[Django] Got 403!")
        self.assertIn("juliana.crain@dev.io", mail.outbox[0].to)
