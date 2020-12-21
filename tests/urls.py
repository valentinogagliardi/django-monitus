from django.contrib.auth.views import LoginView
from django.urls import path
from django.http import HttpResponse


def secret(request):
    return HttpResponse("For testing.", status=403)


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = "login.html"


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
    path("login/", Login.as_view()),
    path("tickets/", ticket_create),
    path("without-form/", without_form),
    path("without-context-data/", without_context_data),
]
