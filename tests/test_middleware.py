import pytest
from django.test import TestCase, override_settings
from django.core import mail
from model_bakery import baker

LOCMEM_BACKEND = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {"login.html": "<body><body>"},
                )
            ]
        },
    }
]


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

    def test_it_handles_anon_user(self):
        self.client.logout()
        self.client.get("/secret-area/")


@override_settings(TEMPLATES=LOCMEM_BACKEND)
class FailedLoginMiddlewareTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make("User", email="some.user@dev.io")

    def test_it_sends_email_to_admins_on_failed_login_attempts(self):
        self.client.post("/login/", {"username": "brute", "password": "force"})
        self.assertEqual(mail.outbox[0].subject, "[Django] Failed login attempt")
        self.assertIn("juliana.crain@dev.io", mail.outbox[0].to)
        body = mail.outbox[0].body
        self.assertIn("127.0.0.1", body)
        self.assertIn("/login/", body)

    def test_it_does_not_send_email_to_admins_on_valid_login(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.client.get("/login/")
        self.assertFalse(mail.outbox)

    def test_it_handles_only_authentication_form_errors(self):
        self.client.post("/tickets/", {"subject": "Website instable"})
        self.assertFalse(mail.outbox)

    def test_it_handles_functional_views_without_forms(self):
        self.client.get("/without-form/")

    def test_it_handles_functional_views_without_context_data(self):
        self.client.get("/without-context-data/")


@override_settings(TEMPLATES=LOCMEM_BACKEND)
@pytest.mark.django_db
@pytest.mark.parametrize(
    "method, expected", [("get", 0), ("head", 0), ("trace", 0), ("options", 0)]
)
def test_it_does_not_send_email_to_admins_non_post_methods(
    method, expected, client, mailoutbox
):
    request = getattr(client, method)
    request("/login/")
    assert len(mailoutbox) == expected
