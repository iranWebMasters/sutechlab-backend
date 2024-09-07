
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY='django-insecure-95*u*w5%3ye=7fdga*u0*ur#2e^qnd^6^zlg0ptwj5gr+(02mb)'
DEBUG=True
ALLOWED_HOSTS = ['localhost', '127.0.0.1',]


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
    'requests',

    'decouple',
    'django.contrib.humanize',
    'django_jalali',
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.sites',
    
]

SITE_ID = 2

MIDDLEWARE = [
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

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':config('DB_ENGINE', default='django.db.backends.postgresql'),
            'NAME':config('DB_NAME', default='postgres'),
            'USER':config('DB_USER', default='postgres'),
            'PASSWORD':config('PASSWORD', default='1'),
            'HOST':config('HOST', default='127.0.0.1'),
            'PORT':config('PORT', default='5432')
        }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': 'mysite-database',
    #         'USER': 'root',
    #         'PASSWORD': 'JjO05MwXpcczY3nSCTnYfBvL',
    #         'HOST': 'mysite-database', 
    #         'PORT': '5432',        
    #     }
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

CKEDITOR_UPLOAD_PATH='uploads/'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Https settings
if config("USE_SSL_SETTINGS",default=False,cast=bool):
    SECURE_BROWSER_XSS_FILTER = True
    CSRF_COOKIE_SECURE =True
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_CONTENT_TYPE_NOSNIFF = True

    ## Strict-Transport-Security
    SECURE_HSTS_SECONDS = 15768000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    ## that requests over HTTP are redirected to HTTPS. aslo can config in webserver
    SECURE_SSL_REDIRECT = True 

    # for more security
    CSRF_COOKIE_SECURE = True
    CSRF_USE_SESSIONS = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    
    
# registration url redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = "accounts.User"
