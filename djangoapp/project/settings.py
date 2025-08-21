from pathlib import Path
import os
from decouple import config  # type: ignore
from dotenv import load_dotenv  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent

# BASE_DIR.parent aponta para /app, que é a raiz do seu código no container
dotenv_path = BASE_DIR.parent / '.dotenv_files' / '.env'
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY')
# Converte '1' para True e '0'/'None' para False
DEBUG = str(os.getenv('DEBUG', '0')) == '1'

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',')
    if h.strip()
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Aplicativo do blog
    'site_setup',
    'django_summernote',  # Aplicativo para notas de rodapé
    'axes',  # Aplicativo para controle de acesso
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'site_setup.middleware.SiteSetupMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'project.urls'

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
                'site_setup.context_processors.site_setup',  # Context processor para SiteSetup
            ],
        },
    },
]


WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        # cast=int converte o número da porta
        'PORT': config('POSTGRES_PORT', cast=int),
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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # -> /app/staticfiles

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # -> /app/media

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # -> /app/static
]

MIGRATION_MODULES = {
    'django_summernote': 'migrations.django_summernote',
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGOUT AUTOMÁTICO POR INATIVIDADE

# Tempo de vida do cookie da sessão em segundos.
# Ex: 1800 segundos = 30 minutos de inatividade.
SESSION_COOKIE_AGE = 1800

# Salva a sessão a cada requisição. Isso "reseta" o contador de inatividade
# toda vez que o usuário clica em algo. O logout só ocorrerá se ele
# ficar o tempo acima sem fazer NADA.
SESSION_SAVE_EVERY_REQUEST = True


AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]


SUMMERNOTE_CONFIG = {
    'summernote': {
        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['style', ['style', ]],
            ['font', ['bold', 'italic', 'clear']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph', 'hr', ]],
            ['table', ['table']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen', 'codeview', 'undo', 'redo']],
        ],
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            'lineWrapping': 'true',
            'theme': 'dracula',
        },
    },
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/theme/dracula.min.css',
    ),
    'attachment_filesize_limit': 30 * 1024 * 1024,
    'attachment_model': 'blog.PostAttachment',
}

# djangoapp/project/settings.py

LOGIN_URL = 'blog:login'
LOGIN_REDIRECT_URL = 'blog:index'
LOGOUT_REDIRECT_URL = 'blog:login'


AXES_ENABLED = True
AXES_FAILURE_LIMIT = 6
AXES_COOLOFF_TIME = 1  # Tempo de bloqueio em horas
AXES_RESET_ON_SUCCESS = True
