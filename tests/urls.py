from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm


def secret(request):
    return HttpResponse("For testing.", status=403)


def login(request):
    response = HttpResponse()
    if request.user.is_authenticated:
        return response
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        setattr(response, "context_data", {"form": form})
    return response


def ticket_create(request):
    response = HttpResponse()
    setattr(response, "context_data", {"form": None})
    return response


def without_form(request):
    response = HttpResponse()
    setattr(response, "context_data", {})
    return response


def without_context_data(request):
    return HttpResponse("For testing")


urlpatterns = [
    path("secret-area/", secret),
    path("login/", login),
    path("tickets/", ticket_create),
    path("without-form/", without_form),
    path("without-context-data/", without_context_data),
]
