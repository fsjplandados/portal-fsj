from pathlib import Path
import os
import dj_database_url  # Biblioteca para conectar ao Neon/Postgres

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
# Em produção, busca a chave do ambiente. No local, usa uma insegura de teste.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-chave-local-desenvolvimento')

# Em produção (Render), DEBUG será False (0). Localmente será True.
DEBUG = int(os.environ.get('DEBUG', 1))

# Domínios permitidos (Render + Localhost)
# O '*' libera para todos, útil para evitar erros de "DisallowedHost" iniciais
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(' ')


# --- APLICAÇÕES ---
INSTALLED_APPS = [
    # Mantenha os apps padrões do Django no topo
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # O 'staticfiles' deve vir ANTES do Cloudinary neste caso
    'django.contrib.staticfiles',
    
    # Apps de Terceiros (Cloudinary)
    'cloudinary_storage',
    'cloudinary',
    
    # Seus Apps
    'dashboards',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # WhiteNoise: Essencial para arquivos estáticos no Render
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # O Django busca automaticamente nas pastas 'templates' dos apps
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

WSGI_APPLICATION = 'core.wsgi.application'


# --- BANCO DE DADOS (Híbrido) ---
# Se houver a variável DATABASE_URL (Render/Neon), usa PostgreSQL.
# Se não (seu PC), usa o arquivo db.sqlite3 local.
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# --- VALIDAÇÃO DE SENHA ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS (CSS, JS, Imagens) ---
STATIC_URL = 'static/'

# Onde estão seus estáticos locais (ex: a logo)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Onde o Django vai juntar tudo no deploy (pasta staticfiles)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Engine do WhiteNoise para comprimir e servir arquivos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- ARQUIVOS DE MÍDIA (Uploads de capas dos dashboards) ---
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}


# --- LOGIN / LOGOUT ---
LOGIN_REDIRECT_URL = '/'          # Vai para a Home após logar
LOGOUT_REDIRECT_URL = '/accounts/login/'  # Volta para o Login após sair
LOGIN_URL = '/accounts/login/'    # URL da página de login

# Tipo de campo chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
