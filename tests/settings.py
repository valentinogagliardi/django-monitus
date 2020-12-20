DEBUG = False
SECRET_KEY = "NOT_SO_SECRET"
ROOT_URLCONF = "tests.urls"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "monitus",
]
MIDDLEWARE = [
    "monitus.middleware.Error403EmailsMiddleware",
    "monitus.middleware.FailedLoginMiddleware",
]
ADMINS = [("Juliana C.", "juliana.crain@dev.io")]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
