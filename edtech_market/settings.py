"""
Django settings for edtech_market project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from os import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b@e(89(q6%4oxmquv!^fh3j^p$zx@gygqp)&_1=ap%7hxiya*p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['edtech-review.herokuapp.com', 'localhost',  '127.0.0.1', 'www.edtech.reviews', 'edtech.reviews']


# Application definition

INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'listings.apps.ListingsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'star_ratings',
    'crispy_forms',
    'django_filters',
    'taggit', 
    'hitcount',





]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'edtech_market.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'edtech_market.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# DATABASE_URL: postgres://duesustgpjtsjg:6e2c3463f268d93739946f04277e7e3c08c04b31b45860ddd8c42cefedc9871b@ec2-54-228-250-82.eu-west-1.compute.amazonaws.com:5432/dtug35ea3clsm
# ?sslmode=require  - надо добавить
DATABASES = {
    'test': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edtech_marketplace',
        'USER': 'postgres',
        'PASSWORD': 'rimash456654',
        'HOST': 'localhost',
    
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dtug35ea3clsm',
        'USER': 'duesustgpjtsjg',
        'PASSWORD': '6e2c3463f268d93739946f04277e7e3c08c04b31b45860ddd8c42cefedc9871b',
        'HOST': 'ec2-54-228-250-82.eu-west-1.compute.amazonaws.com',
    }
}
default_database = environ.get('DJANGO_DATABASE', 'default')
DATABASES['default'] = DATABASES[default_database]


AUTHENTICATION_BACKENDS = {
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
}

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_USERNAME_REQUIRED = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  #убрать после релиза
# LOGIN_REDIRECT_URL = '/'

# LOCALE_PATHS = ['/locale']   

LANGUAGE_CODE = 'ru'  # язык сайта по умолчанию

# LANGUAGES = (
#     ('ru', 'Russian'),
#     # ('en', 'English'),
# )


TIME_ZONE = 'Europe/Moscow'
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT= os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'edtech_market/static')
    ]

# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Star rating
STAR_RATINGS_STAR_WIDTH = 13

# STAR_RATINGS_RATING_MODEL = 'pages.MyRating'
# STAR_RATINGS_OBJECT_ID_PATTERN = '[a-z0-9]{32}'


# Allauth

SITE_ID = 1

#crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'


