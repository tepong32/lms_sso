"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0vk4l*&cp2o_o76!h&szpw$8+$yvba^9h*bvtc0_=8=079oj9v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    ### third-party packages ###
    'allauth',
    'jazzmin',
    'adminlte3',
    'adminlte3_theme',
    'crispy_forms',
    'crispy_bootstrap4',
    'rest_framework',

    ### defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ### admin-created apps ###
    'api.apps.ApiConfig',
    'home.apps.HomeConfig',
    'users.apps.UsersConfig',

    
]

### some defaults to make the project work ###
SITE_ID = 1
### this next line is needed for custom user models to work on django
### see https://www.youtube.com/watch?v=mndLkCEiflg 1:30 mark
AUTH_USER_MODEL='users.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = 'static/' # or '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")     # where we want django to save uploaded files
MEDIA_URL = 'media/' # or '/media/'

### meron na nitong login settings sa ibaba. Check them out
# LOGIN_REDIRECT_URL = 'home'     # needed for the login.html success instance
# LOGIN_URL = 'login'             # for the @login_required decorator on user.views.profile

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com' # or only your domain name if you have your own mail server
# EMAIL_PORT = 587 #587
# EMAIL_USE_TLS = True

### TO USE THESE VARIABLES BELOW, USE ENVIRONMENT VARIABLES TO HIDE SENSITIVE INFO
### CHECK CoreyMs' Django TUTORIAL # 12 -- 14:20
EMAIL_HOST_USER = os.environ.get('ADMIN_EMAIL_UN') # var for email username
EMAIL_HOST_PASSWORD = os.environ.get('ADMIN_EMAIL_PW') # var for email pw
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER # for email-sending pw-reset requests



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Affects to the "welcome" url (after successful authentication) when
# user logged in but don't have url to redirect. Optional.
# Compatible logic with Django.
LOGIN_REDIRECT_URL = '/' # set this as the go-to page after successful login
LOGIN_URL = '/login/' # this should explicitly be "/login/" as it is an absolute path

CRISPY_TEMPLATE_PACK = 'bootstrap4'     # for the css of crispy forms
PASSWORD_RESET_CONFIRM_TEMPLATE = '/password-reset/password-reset-confirm.html'



REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}