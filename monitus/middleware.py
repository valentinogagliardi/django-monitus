from http import HTTPStatus
from django.conf import settings
from django.core.mail import mail_managers


class Error403EmailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == HTTPStatus.FORBIDDEN and not settings.DEBUG:
            mail_managers("Got 403!", "Message: 403")
        return response
