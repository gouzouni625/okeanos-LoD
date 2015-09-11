"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-ay^f7=9e!@jr94v7!v&tl@4zm5=0g8&8d9(a*ffzqywg#@6iy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
    'rest_framework',
    'rest_framework.authtoken'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                'webapp/templates'
        ],
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

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lambda_db',
        'USER': 'lambda',
        'PASSWORD': 'change_me',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

##### Celery configuration #####
from kombu import Queue

CELERY_QUEUES = (
    Queue('events_queue', routing_key='event_key'),
    Queue('tasks_queue', routing_key='task_key'),
)

CELERY_ROUTES = {
    'backend.tasks.lambda_instance_start': {
        'queue': 'tasks_queue',
        'routing_key': 'task_key',
    },
    'backend.tasks.lambda_instance_stop': {
        'queue': 'tasks_queue',
        'routing_key': 'task_key',
    },
    'backend.tasks.lambda_instance_destroy': {
        'queue': 'tasks_queue',
        'routing_key': 'task_key',
    },
    'backend.events.set_lambda_instance_status': {
        'queue': 'events_queue',
        'routing_key': 'event_key',
    },
    'backend.tasks.create_lambda_instance': {
        'queue': 'tasks_queue',
        'routing_key': 'task_key',
    },
    'backend.events.create_new_lambda_instance': {
        'queue': 'events_queue',
        'routing_key': 'event_key',
    },
    'backend.events.insert_cluster_info': {
        'queue': 'events_queue',
        'routing_key': 'event_key',
    },

}

FILE_STORAGE = os.path.join(BASE_DIR,'uploaded_files')

REST_FRAMEWORK = {
  'DEFAULT_RENDERER_CLASSES': (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
    'rest_framework_xml.renderers.XMLRenderer',
  )
}

