from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    '13.245.109.191',
    'www.fundly.co.ke',
    'fundly.co.ke',
]

ADMINS = [
    ('Admin', 'o.jeff3.a@gmail.com'),
    ('Laurent', 'lawiomosh3@gmail.com'),
    ('Jeff', 'info@fundly.co.ke'),
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    'django_daraja',
    

    # Local apps
    'core.apps.CoreConfig',
    'project.apps.ProjectConfig',
    'users.apps.UsersConfig',
    'service.apps.ServiceConfig',
    'blog.apps.BlogConfig',
    'api.apps.ApiConfig',
    'mchango.apps.MchangoConfig',

    #add allauth configuration
    'allauth',
    'allauth.account',
    'allauth.usersessions',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',

    # The MFA app:
    'allauth.mfa',
]

SITE_ID = 1

CART_SESSION_ID = 'cart'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates/')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #All auth
    'allauth.account.middleware.AccountMiddleware',
    'allauth.usersessions.middleware.UserSessionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

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
                'core.context_processor.all',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


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
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': 5432,
            'OPTIONS': {
                'sslmode': 'require',
            }
        }
    }


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

# Make sure "webauthn" is included.
MFA_SUPPORTED_TYPES = ["totp", "webauthn", "recovery_codes"]

# Optional: enable support for logging in using a (WebAuthn) passkey.
MFA_PASSKEY_LOGIN_ENABLED = True

# Optional -- use for local development only: the WebAuthn uses the
#``fido2`` package, and versions up to including version 1.1.3 do not
# regard localhost as a secure origin, which is problematic during
# local development and testing.
MFA_WEBAUTHN_ALLOW_INSECURE_ORIGIN = True

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Make sure that the login methods includes "phone" as a method.
USERSESSIONS_TRACK_ACTIVITY = True
# Add a required phone field to the signup fields.
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ['first_name*', 'last_name*', 'email*', 'username*', 'password1*', 'password2*']

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_MAX_LENGTH = 200
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_SIGNUP_REDIRECT_URL = 'users:profile'
# ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'test', 'user', 'root', 'superuser', 'moderator', 'guest', 'support', 'service', '1234', '12345', 'banned', 'hacker', 'staff', 'owner', '123456', '12345678']
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Fundly - '

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'sw'

THEME_CHOICES = [
    ('light', 'light'),
    ('dark', 'dark'),
]

LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
]

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static/')
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    'https://fundly.co.ke/',
    'https://www.fundly.co.ke/',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# The Mpesa environment to use
# Possible values: sandbox, production

MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT')

# Credentials for the daraja app

MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')

#Shortcode to use for transactions. For sandbox  use the Shortcode 1 provided on test credentials page

MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')

# Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
# This is only used on sandbox, do not set this variable in production
# For sandbox use the Lipa na MPESA Online Shorcode provided on test credentials page

MPESA_EXPRESS_SHORTCODE = os.getenv('MPESA_EXPRESS_SHORTCODE')

# Type of shortcode
# Possible values:
# - paybill (For Paybill)
# - till_number (For Buy Goods Till Number)

MPESA_SHORTCODE_TYPE = os.getenv('MPESA_SHORTCODE_TYPE')

# Lipa na MPESA Online passkey
# Sandbox passkey is available on test credentials page
# Production passkey is sent via email once you go live

MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')

# Username for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

MPESA_INITIATOR_USERNAME = os.getenv('MPESA_INITIATOR_USERNAME')
# Plaintext password for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

MPESA_INITIATOR_SECURITY_CREDENTIAL = os.getenv('MPESA_INITIATOR_PASSWORD')