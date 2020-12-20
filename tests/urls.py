from django.urls import path
from django.http import HttpResponse


def index(request):
    return HttpResponse("For testing.", status=403)


urlpatterns = [path("", index)]
