import asyncio
from asgiref.sync import sync_to_async
from http import HTTPStatus
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import mail_admins


class Error403EmailsMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(self, get_response):
        self.get_response = get_response
        if asyncio.iscoroutinefunction(self.get_response):
            self._is_coroutine = asyncio.coroutines._is_coroutine

    def __call__(self, request):
        if asyncio.iscoroutinefunction(self.get_response):
            return self.__acall__(request)

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

    async def __acall__(self, request):
        response = await self.get_response(request)
        if response.status_code == HTTPStatus.FORBIDDEN and not settings.DEBUG:
            path = request.get_full_path()
            ip = request.META.get("REMOTE_ADDR", "<none>")
            await mail_admins_task("Got 403!", ip, path, user=request.user)
        return response


class FailedLoginMiddleware:
    sync_capable = True
    # TODO: Works in testing but not with the
    #  real Django until Django gets async ORM support
    async_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if asyncio.iscoroutinefunction(self.get_response):
            self._is_coroutine = asyncio.coroutines._is_coroutine

    def __call__(self, request):
        if asyncio.iscoroutinefunction(self.get_response):
            return self.__acall__(request)

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

    async def __acall__(self, request):
        response = await self.get_response(request)
        try:
            form = response.context_data.get("form")
            # TODO: adapt username field and backport this logic to sync mode
            """
            TODO: Works properly in testing but not with the
            real Django until Django gets async ORM support
            """
            invalid_login = f"password"
            if invalid_login in form.errors:
                path = request.get_full_path()
                ip = request.META.get("REMOTE_ADDR", "<none>")
                await mail_admins_task("Failed login attempt", ip, path)
        except AttributeError:
            pass
        return response


"""
Async helpers
"""


async def mail_admins_task(subject, ip, path, **kwargs):
    if "Failed login attempt" in subject:
        message = f"Failed login attempt from {ip} on {path}."
        coro = sync_to_async(mail_admins)(subject, message, fail_silently=True)
        task = asyncio.create_task(coro)
        task.add_done_callback(lambda msg: print("\n", msg))
    if "Got 403" in subject:
        user = kwargs.get("user")
        message = f"Got error 403 on {path} from {ip}. User: {user.username}"
        coro = sync_to_async(mail_admins)(subject, message, fail_silently=True)
        task = asyncio.create_task(coro)
        task.add_done_callback(lambda msg: print("\n", msg))
