from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "(v)uhf&0!)cebh%pw_nii*_j+r)3!t_6+(0k%&72r*sr#9(h)8"

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = ['https://8000-icy-term-29576850.eu-ws2.runcode.io','https://8080-icy-term-29576850.eu-ws2.runcode.io']



INSTALLED_APPS += [  # noqa
    "django_sass",
]

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass
