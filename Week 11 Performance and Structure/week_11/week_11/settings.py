"""
Django settings for the Week 11 project.
"""

import os
from pathlib import Path

#-----------------------------------------------
# Base directory
#-----------------------------------------------

# Main project folder containing manage.py.
BASE_DIR = Path(__file__).resolve().parent.parent


#------------------------------------------------
# Environment variables
#------------------------------------------------

def load_env_file(path):
    """Load enviroment variables from .env file if the file exists."""
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # Ignore empty lines, comments, and invalid entries.
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip().strip('"').strip("'")

        # Keep existing system environment variables unchanged.
        os.environ.setdefault(key, value)


# Check for .env beside manage.py and one directory above it.
load_env_file(BASE_DIR / ".env")
load_env_file(BASE_DIR.parent / ".env")


#-------------------------------------------
# Core project settings
#-------------------------------------------

# Keep the production secret key private.
SECRET_KEY = (
    'django-insecure-6ce-r3ll2#4p!zgq^j3t^68**'
    'fv8$4p8mf8)wi*rqz=gitzjbk'
)

# Disable DEBUG before production deployment.
DEBUG = True

ALLOWED_HOSTS = []


#----------------------------------------
# Installed applications
#----------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages',
    'debug_toolbar',
]


#----------------------------------------
# Middleware
#----------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


#-----------------------------------------
# URLs and application configuration
#-----------------------------------------

ROOT_URLCONF = 'week_11.urls'

WSGI_APPLICATION = "week_11.wsgi.application"

#---------------------------------------------
# Templates
#---------------------------------------------

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

#----------------------------------------------
# Database
#----------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


#---------------------------------------------------
# Password validation
#---------------------------------------------------

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


#-----------------------------------------------------------------
# Internationalization
#-----------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#----------------------------------------------------------------
# Static files
#----------------------------------------------------------------

STATIC_URL = 'static/'


#----------------------------------------------------------------
# Authentication redirects
#----------------------------------------------------------------

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"


#-------------------------------------------------------------
# Uploaded media files
#-------------------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


#------------------------------------------------------------
# OpenAI API settings
#------------------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


#-----------------------------------
# Old Memo
#-----------------------------------
"""LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}"""
#------------------------------------------


#------------------------------------------------------------
# Django Debug Toolbar
#------------------------------------------------------------

INTERNAL_IPS = [
    "127.0.0.1",
]