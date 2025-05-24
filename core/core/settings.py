from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key and Debug Settings
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

# Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website",
    "blog",
    "taggit",
    "accounts",
    "devices",
    "userpanel",
    "services",
    "orders",
    "gateway",
    "notifications",
    "drf_yasg",
    "rest_framework",
    "azbankgateways",
    "decouple",
    "django.contrib.humanize",
    "django_jalali",
    "django.contrib.sites",
    # 'sslserver',
    # 'django_celery_beat',
]

SITE_ID = 2

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notifications.context_processors.notification_context_processor",
                "accounts.context_processors.user_profile_context_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Use PostgreSQL
        "NAME": config("DATABASE_NAME"),  # Read DATABASE_NAME from environment
        "USER": config("DATABASE_USER"),  # Read DATABASE_USER from environment
        "PASSWORD": config(
            "DATABASE_PASSWORD"
        ),  # Read DATABASE_PASSWORD from environment
        "HOST": config(
            "DATABASE_HOST", default="localhost"
        ),  # Read DATABASE_HOST from environment
        "PORT": config(
            "DATABASE_PORT", default="5432"
        ),  # Read DATABASE_PORT from environment
    }
}

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# Static and Media Files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security Settings
SECURE_REFERRER_POLICY = config(
    "SECURE_REFERRER_POLICY", default="strict-origin-when-cross-origin"
)
SECURE_BROWSER_XSS_FILTER = config("SECURE_BROWSER_XSS_FILTER", default=True, cast=bool)
X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default="SAMEORIGIN")
SECURE_CONTENT_TYPE_NOSNIFF = config(
    "SECURE_CONTENT_TYPE_NOSNIFF", default=True, cast=bool
)

# HSTS Settings
SECURE_HSTS_SECONDS = config(
    "SECURE_HSTS_SECONDS", default=0, cast=int
)  # Disable HSTS by default
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)
SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT", default=False, cast=bool
)  # Force HTTPS redirection

# CSRF settings
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
CSRF_USE_SESSIONS = config("CSRF_USE_SESSIONS", default=True, cast=bool)
CSRF_COOKIE_HTTPONLY = config("CSRF_COOKIE_HTTPONLY", default=True, cast=bool)

# Session settings
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
SESSION_COOKIE_SAMESITE = config("SESSION_COOKIE_SAMESITE", default="Lax")
SESSION_EXPIRE_AT_BROWSER_CLOSE = config(
    "SESSION_EXPIRE_AT_BROWSER_CLOSE", default=False, cast=bool
)
SESSION_COOKIE_AGE = config(
    "SESSION_COOKIE_AGE", default=1209600, cast=int
)  # 2 weeks in seconds
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='').split(',')

# Add SECURE_PROXY_SSL_HEADER setting
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Registration URL Redirects
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTH_USER_MODEL = "accounts.User"

# Bank Payment Gateway Configuration
AZ_IRANIAN_BANK_GATEWAYS = {
    "GATEWAYS": {
        # "BMI": {
        #     "MERCHANT_CODE": config("BMI_MERCHANT_CODE"),
        #     "TERMINAL_CODE": config("BMI_TERMINAL_CODE"),
        #     "SECRET_KEY": config("BMI_SECRET_KEY"),
        # },
        'ZARINPAL': {
           'MERCHANT_CODE': '0dbb3d9d-41f7-4776-b97d-545e81377eda',
           'SANDBOX': 0,  # 0 disable, 1 active
       }
    },
    "IS_SAMPLE_FORM_ENABLE": True,
    "DEFAULT": "ZARINPAL",
    "CURRENCY": "IRT",
    "TRACKING_CODE_QUERY_PARAM": "tc",
    "TRACKING_CODE_LENGTH": 16,
    "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",
    "BANK_PRIORITIES": [
        "ZARINPAL",
    ],
    "IS_SAFE_GET_GATEWAY_PAYMENT": False,
    "CUSTOM_APP": None,
}

# Email Settings
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="your_email@example.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="your_email_password")
EMAIL_FILE_PATH = "tmp/app-messages"

# Swagger Settings
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "DOC_EXPANSION": "none",
    "DEFAULT_MODEL_RENDERING": "example",
}

# SMS API Configuration
SMS_API_KEY = config("SMS_API_KEY", default="your_api_key_here")
SMS_API_URL = "https://api.kavenegar.com/v1/{api_key}/sms/send.json"
