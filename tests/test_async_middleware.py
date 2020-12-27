import pytest
from unittest.mock import patch, ANY


@pytest.mark.skip(
    reason="""
            TODO: Works properly in testing but not with the
            real Django until Django gets async ORM support
            """
)
@pytest.mark.asyncio
async def test_it_sends_email_to_admin_on_failed_login_attempts(async_client, settings):
    settings.ROOT_URLCONF = "tests.async_urls"
    settings.MIDDLEWARE = [
        "monitus.middleware.FailedLoginMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]
    with patch("monitus.middleware.mail_admins_task") as mocked_mail_admins_task:
        response = await async_client.post(
            "/login/", {"username": "brute", "password": "force"}
        )
        assert response.status_code == 403
        mocked_mail_admins_task.assert_called_once_with(
            "Failed login attempt", "127.0.0.1", "/login/"
        )


# TODO: test authenticated user
@pytest.mark.skip
@pytest.mark.asyncio
async def test_it_sends_email_to_admin_on_403(async_client, settings):
    settings.ROOT_URLCONF = "tests.async_urls"
    settings.MIDDLEWARE = [
        "monitus.middleware.Error403EmailsMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]
    with patch("monitus.middleware.mail_admins_task") as mocked_mail_admins_task:
        response = await async_client.get("/secret-area/")
        assert response.status_code == 403
        mocked_mail_admins_task.assert_called_once_with(
            "Got 403!", "127.0.0.1", "/secret-area/"
        )


@pytest.mark.asyncio
async def test_it_sends_email_to_admin_on_403_it_handles_anon_user(
    async_client, settings
):
    settings.ROOT_URLCONF = "tests.async_urls"
    settings.MIDDLEWARE = [
        "monitus.middleware.Error403EmailsMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]
    with patch("monitus.middleware.mail_admins_task") as mocked_mail_admins_task:
        response = await async_client.get("/secret-area/")
        assert response.status_code == 403
        mocked_mail_admins_task.assert_called_once_with(
            "Got 403!", "127.0.0.1", "/secret-area/", user=ANY
        )


@pytest.mark.asyncio
async def test_middlewares_work_together_errormiddleware_before_failed(
    async_client, settings
):
    settings.ROOT_URLCONF = "tests.async_urls"
    settings.MIDDLEWARE = [
        "monitus.middleware.FailedLoginMiddleware",
        "monitus.middleware.Error403EmailsMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]
    with patch("monitus.middleware.mail_admins_task"):
        response = await async_client.get("/secret-area/")
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_middlewares_work_together_errormiddleware_after_failed(
    async_client, settings
):
    settings.ROOT_URLCONF = "tests.async_urls"
    settings.MIDDLEWARE = [
        "monitus.middleware.Error403EmailsMiddleware",
        "monitus.middleware.FailedLoginMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]
    with patch("monitus.middleware.mail_admins_task"):
        response = await async_client.get("/secret-area/")
        assert response.status_code == 403
