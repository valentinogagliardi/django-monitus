from http import HTTPStatus
from django.conf import settings
from django.core.mail import mail_admins


class Error403EmailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == HTTPStatus.FORBIDDEN and not settings.DEBUG:
            mail_admins("Got 403!", "Message: 403")
        return response


class FailedLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not hasattr(response, "context_data"):
            return response
        if "form" in response.context_data:
            if "invalid_login" in response.context_data["form"].error_messages:
                path = request.get_full_path()
                ip = request.META.get("REMOTE_ADDR", "<none>")
                mail_admins(
                    "Failed login attempt",
                    f"Failed login attempt from {ip} on {path}.",
                    fail_silently=True,
                )
        return response
