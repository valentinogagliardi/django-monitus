from django.urls import path
from django.http import HttpResponse


async def secret(request):
    return HttpResponse("For testing.", status=403)


async def login(request):
    """
    Django has still no async ORM support.
    We don't want to interact with the real AuthenticationForm.
    This simulates an async login view with a fake AuthenticationForm.
    """
    response = HttpResponse(status=403)

    class FakeAuthenticationForm:
        pass

    errors = f"Please, enter a correct username and password"
    setattr(FakeAuthenticationForm, "errors", errors)
    setattr(response, "context_data", {"form": FakeAuthenticationForm})
    return response


urlpatterns = [path("secret-area/", secret), path("login/", login)]
