"""
Django settings for mysite_MYSQL project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.conf import settings



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5qvi!cro^i20hf&x#f&_)b485qavho3%r8lq73=7g2n4u-je$m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_forms_bootstrap',
    'ZSIV',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite_MYSQL.urls'

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

WSGI_APPLICATION = 'mysite_MYSQL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ZSIV',
        'USER': 'christian',
        'PASSWORD': 'christian',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# settings file hat permission issues
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'init_command': 'SET storage_engine=INNODB',
#             'read_default_file': '/media/win-d/myfiles/2016/django/mysite_MYSQL/ChristianLocal.cnf',
# #             
#         },
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


"""
List of directories where "./manage.py collectstatic" 
will look for files, which it puts all together into STATIC_ROOT. 
Each app that you have can have it's own "static" files directory.
"""

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #'/var/www/static/',
]

REPOSITORY_ROOT = os.path.dirname(BASE_DIR)


""" URL that your STATIC files will be accessible through the browser."""
STATIC_URL = '/static/' 

"""  Physical system path where the static files are stored."""
STATIC_ROOT = os.path.join(REPOSITORY_ROOT, 'static/') 

"""  URL that your MEDIA files will be accessible through the browser."""
MEDIA_URL = '/mysite_MYSQL/ZSIV/uploads/'

"""Physical system path where the static files are stored. Files that are being uploaded by the user."""
MEDIA_ROOT = os.path.join(REPOSITORY_ROOT, 'mysite_MYSQL/ZSIV/uploads')



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/ZSIV-messages' # change this to a proper location


"""
http://stackoverflow.com/questions/6367014/how-to-send-email-via-django
Sichere Apps erlauben?
https://support.google.com/accounts/answer/6010255
security: http://stackoverflow.com/questions/12461484/is-it-secure-to-store-passwords-as-environment-variables-rather-than-as-plain-t
os.environ['CCGPWD'] 

"""

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'macKenzie4'
EMAIL_HOST_PASSWORD = 'billslater4'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'jedhoo@web.de'




