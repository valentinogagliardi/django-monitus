DEBUG = False
SECRET_KEY = "NOT_SO_SECRET"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}
ROOT_URLCONF = "tests.urls"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "monitus",
]
MIDDLEWARE = [
    "monitus.middleware.Error403EmailsMiddleware",
    "monitus.middleware.FailedLoginMiddleware",
    # Session and auth middlewares needed for having request.user in Error403EmailsMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]
ADMINS = [("Juliana C.", "juliana.crain@dev.io")]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
