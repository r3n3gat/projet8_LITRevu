from pathlib import Path

# Chemin racine du projet (contenant manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------
# Sécurité
# ------------------------
SECRET_KEY = 'django-insecure-baa-ph-ut-cesh+s6u@(u%%8%x9!e3!45748)tpv&%&*r0(4#i'
DEBUG = True
ALLOWED_HOSTS = []

# ------------------------
# Applications
# ------------------------
INSTALLED_APPS = [
    # Apps Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Vos apps métier et UI
    'core',
    'reviews',
    'accounts',
]

# ------------------------
# Middleware
# ------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'litrevu.urls'

# ------------------------
# Templates
# ------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # dossier global templates/
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

WSGI_APPLICATION = 'litrevu.wsgi.application'

# ------------------------
# Base de données
# ------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------
# Authentification
# ------------------------
AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# URL pour @login_required
LOGIN_URL = 'accounts:login'

# Redirections après login / logout
# Après login, on renvoie vers le flux
LOGIN_REDIRECT_URL = '/reviews/'
# Après logout, on renvoie vers la page d’accueil (home)
LOGOUT_REDIRECT_URL = '/'

# ------------------------
# Internationalisation
# ------------------------
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ------------------------
# Static & Media
# ------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------
# Auto field par défaut
# ------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
