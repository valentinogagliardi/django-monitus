from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    return HttpResponse("For testing.", status=403)


def login(request):
    response = HttpResponse()
    form = AuthenticationForm(request.POST)
    form.error_messages = {
        "invalid_login": "Please enter a correct username and password. Note that both fields may be case-sensitive."
    }
    setattr(response, "context_data", {"form": form})
    return response


urlpatterns = [
    path("", index),
    path("login/", login),
]
