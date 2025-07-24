"""
Django settings for USSD Demo Project

This settings file configures the USSD application with:
- Africa's Talking API integration
- Development and production configurations
- Database settings
- Authentication and security settings
- Logging configuration

For more information on Django settings, see:
https://docs.djangoproject.com/en/5.2/topics/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This sets up the base directory for the project, used for relative file paths
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/



# Load environment variables from .env file
# This allows us to keep sensitive data out of version control
load_dotenv()

# Africa's Talking API Configuration
# These credentials are used to authenticate with the Africa's Talking USSD service
# In production, these should be set as environment variables
AT_USERNAME    = os.getenv("AT_USERNAME")    # Your Africa's Talking username
AT_API_KEY     = os.getenv("AT_API_KEY")     # Your Africa's Talking API key
AT_SHORTCODE   = os.getenv("AT_SHORTCODE")   # Your USSD shortcode

# Logging Configuration
# This sets up detailed logging for debugging and monitoring
# In production, you might want to log to files instead of console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Security Settings
# WARNING: These are development settings and must be changed in production!

# Secret key used for cryptographic signing. Must be kept secret in production!
# In production, set this using an environment variable
SECRET_KEY = 'django-insecure-9cz)q*av2j7su%4rzh5on02h(&vzak4t(bul^$7jqnab=)bok5'

# Debug mode gives detailed error pages but should be False in production
DEBUG = True  # Set to False in production

# Hosts/domain names that this Django site can serve
# Use ['your-domain.com'] in production instead of '*'
ALLOWED_HOSTS = ['*']  # '*' allows all hosts - restrict this in production!


# Application definition
# List of all Django apps used in this project

INSTALLED_APPS = [
    # Django's built-in apps
    'django.contrib.admin',          # Admin interface
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content type system
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file management

    # Third-party apps
    'rest_framework',               # Django REST framework for API

    # Local apps
    'ussd_app',                    # Our USSD application
]

# Middleware configuration
# Order is important! These are processed from top to bottom for requests
# and bottom to top for responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',     # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session support
    'django.middleware.common.CommonMiddleware',         # Common request processing
    'django.middleware.csrf.CsrfViewMiddleware',        # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',    # User messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

ROOT_URLCONF = 'ussd_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ussd_demo.wsgi.application'


# Database Configuration
# Using SQLite for development. For production, consider using PostgreSQL
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',    # Database engine
        'NAME': BASE_DIR / 'db.sqlite3',          # Database file path
        # Add these settings for production database:
        # 'USER': 'your_db_user',
        # 'PASSWORD': 'your_db_password',
        # 'HOST': 'localhost',
        # 'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization and Localization Settings
# These settings determine language and time zone handling
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'     # Default language code

TIME_ZONE = 'UTC'           # Default timezone (consider changing to your local timezone)

USE_I18N = True            # Enable internationalization

USE_TZ = True             # Enable timezone support


# Static Files Configuration (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'     # URL to use when referring to static files
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # Uncomment and set in production
# STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional static file directories

# Default Primary Key Field Type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
# Uses BigAutoField as default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Production Settings to add:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
