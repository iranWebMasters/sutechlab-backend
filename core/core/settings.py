
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY',)
DEBUG = os.getenv('DEBUG',)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'blog',
    'taggit',
    'accounts',
    'devices',
    'userpanel',
    'services',
    'orders',
    'gateway',
    
    'drf_yasg',
    'rest_framework',
    "azbankgateways",
    'decouple',
    'django.contrib.humanize',
    'django_jalali',
    'django.contrib.sites',

    'debug_toolbar',
    # 'django_celery_beat',

    
]

SITE_ID = 2

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
# DATABASES_________________________________________


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DATABASE_NAME',),
#         'USER': os.environ.get('DATABASE_USER',),
#         'PASSWORD': os.environ.get('DATABASE_PASSWORD',),
#         'HOST': os.environ.get('DATABASE_HOST',),
#         'PORT': os.environ.get('DATABASE_PORT',),
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# DATABASES_________________________________________
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Https settings
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = False
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CONTENT_TYPE_NOSNIFF = True

## Strict-Transport-Security
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

## that requests over HTTP are redirected to HTTPS. aslo can config in webserver
SECURE_SSL_REDIRECT = False

# for more security
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Strict'

    
    
# registration url redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = "accounts.User"


# Bank payment gateway
AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'ZARINPAL': {
           'MERCHANT_CODE': '0dbb3d9d-41f7-4776-b97d-545e81377eda',
           'SANDBOX': 1,  # 0 disable, 1 active
        },
        "IDPAY": {
            "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
            "METHOD": "GET",  # GET or POST
            "X_SANDBOX": 0
        },
        "PAYV1": {
            "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
            "X_SANDBOX": 1,  # 0 disable, 1 active
        },
   },
   'IS_SAMPLE_FORM_ENABLE': True, # اختیاری و پیش فرض غیر فعال است
   'DEFAULT': 'ZARINPAL',
   'CURRENCY': 'IRT', # اختیاری
   'TRACKING_CODE_QUERY_PARAM': 'tc', # اختیاری
   'TRACKING_CODE_LENGTH': 16, # اختیاری
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader', # اختیاری
   'BANK_PRIORITIES': [
       'ZARINPAL',
       'IDPAY',
       'PAYV1',
       # and so on ...
   ], # اختیاری
   'IS_SAFE_GET_GATEWAY_PAYMENT': False, #اختیاری، بهتر است True بزارید.
   'CUSTOM_APP': None, # اختیاری 
}





# SMTP 
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # یا هاست SMTP دیگری که استفاده می‌کنید
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'ansarialireza@mail.ir'  # ایمیل شما
# EMAIL_HOST_PASSWORD = 'Ansari1999'  # رمز عبور ایمیل شما
EMAIL_FILE_PATH = 'tmp/app-messages' 


# Internal IPs for debugging (especially useful with debug toolbar)
INTERNAL_IPS = [
    # For example, for localhost
    '127.0.0.1',
    # If you are using Docker, you might need to include the following:
    'localhost',
    '0.0.0.0',
]

# Caching configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
CACHE_TIMEOUT = 60*25