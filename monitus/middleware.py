from http import HTTPStatus
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import mail_admins


class Error403EmailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == HTTPStatus.FORBIDDEN and not settings.DEBUG:
            path = request.get_full_path()
            ip = request.META.get("REMOTE_ADDR", "<none>")
            if not request.user.is_authenticated:
                mail_admins(
                    "Got 403!",
                    f"Got error 403 on {path} from {ip}. User: Anonymous",
                    fail_silently=True,
                )
                return response
            user = request.user
            mail_admins(
                "Got 403!",
                f"Got error 403 on {path} from {ip}. User: {user.username} - {user.email}",
                fail_silently=True,
            )
        return response


class FailedLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            form = response.context_data.get("form")
            if isinstance(form, AuthenticationForm) and form.errors:
                path = request.get_full_path()
                ip = request.META.get("REMOTE_ADDR", "<none>")
                mail_admins(
                    "Failed login attempt",
                    f"Failed login attempt from {ip} on {path}.",
                    fail_silently=True,
                )
        except AttributeError:
            pass
        return response
