DEBUG = False
SECRET_KEY = "NOT_SO_SECRET"
ROOT_URLCONF = "tests.urls"
INSTALLED_APPS = ["monitus"]
MIDDLEWARE = ["monitus.middleware.Error403EmailsMiddleware"]
MANAGERS = [("Juliana C.", "juliana.crain@dev.io")]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
