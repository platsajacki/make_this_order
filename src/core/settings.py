from os import getenv, makedirs, path
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv('SECRET_KEY')

DEBUG = getenv('DEBUG') == 'True'

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', 'localhost, 127.0.0.1').split(', ')

CSRF_TRUSTED_ORIGINS = getenv(
    'CSRF_TRUSTED_ORIGINS',
    'https://127.0.0.1, https://localhost, https://www.127.0.0.1, https://www.localhost',
).split(', ')

SITE_DOMAIN = getenv('SITE_DOMAIN', '127.0.0.1')

# Application definition
django_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
third_party_apps = [
    'django_filters',
    'drf_yasg',
    'rest_framework',
    'rest_framework_api_key',
]
local_apps = [
    'apps.dishes',
    'apps.orders',
    'apps.tables',
]

INSTALLED_APPS = django_apps + third_party_apps + local_apps

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': getenv('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': getenv('POSTGRES_DB', 'django'),
        'USER': getenv('POSTGRES_USER', 'django'),
        'PASSWORD': getenv('POSTGRES_PASSWORD', 'django'),
        'HOST': getenv('SQL_HOST', 'localhost'),
        'PORT': getenv('SQL_PORT', '5432'),
    }
}


# Password validation
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

LOGIN_REDIRECT_URL = 'orders:list'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

WORKING_HOURS_START = '10:00'
WORKING_HOURS = 12

# Internationalization
LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_DIR = BASE_DIR / 'static'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [STATIC_DIR]

TEMPLATES_DIR = STATIC_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATETIME_FORMATTER = '%d/%b/%Y %H:%M:%S'
LOG_FORMATTER = '[%(asctime)s] logger: %(name)s\nLevel - %(levelname)s, func - %(funcName)s\n%(message)s'
LOG_DIR = BASE_DIR / 'logs'
if not path.exists(LOG_DIR):
    makedirs(LOG_DIR)
LOG_FILE = LOG_DIR / 'mto.log'
if not path.exists(LOG_FILE):
    open(LOG_FILE, 'w').close()

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'main': {
                'format': LOG_FORMATTER,
                'datefmt': DATETIME_FORMATTER,
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'main',
            },
            'timed_rotating_file': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': LOG_FILE,
                'formatter': 'main',
                'when': 'midnight',
                'interval': 1,
                'backupCount': 7,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'timed_rotating_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            }
        },
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {message}\n',
                'style': '{',
            },
        },
    }
