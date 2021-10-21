"""
Django settings for Sanctuary project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
from pathlib import Path
from kombu import Queue, Exchange

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+jkg%^an3e7!i=luhk5nx@(8o+3#+#s&80h8$)65y=jf3im!=&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'rbac',  # 权限管理模块
    'users',  # 用户管理模块
    'sjxf',  # 数据下发模块
    'dataexp',  # 数据提取模块
    'infomg',  # 信息管理模块
    'metrics',  # 指标管理模块
]
AUTH_USER_MODEL = 'users.UserInfo'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middleware.rbac.RbacMiddleware',  # 注册RBAC权限管理中间件
]

ROOT_URLCONF = 'Sanctuary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Sanctuary.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Sanctuary',
        'USER': 'Athena',
        'PASSWORD': 'Passw0rd',
        'HOST': '192.168.57.130',
        'PORT': '3309',
        'CONN_MAX_AGE': 60,
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"}
    }
}

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'static'
else:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]

# 最重要的配置，设置消息broker,格式为：db://user:password@host:port/dbname
# 如果redis安装在本机，使用localhost
# 如果docker部署的redis，使用redis://redis:6379
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

# celery时区设置，建议与Django settings中TIME_ZONE同样时区，防止时差
# Django设置时区需同时设置USE_TZ=True和TIME_ZONE = 'Asia/Shanghai'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False
# 为django_celery_results存储Celery任务执行结果设置后台
# 格式为：db+scheme://user:password@host:port/dbname
# 支持数据库django-db和缓存django-cache存储任务状态及结果
CELERY_RESULT_BACKEND = "django-db"
# celery内容等消息的格式设置，默认json
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
CELERY_TASK_TIME_LIMIT = 30 * 60

# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除。
# 设为0，存储结果永不过期
CELERY_RESULT_EXPIRES = 90

# 任务限流
CELERY_TASK_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

# Worker并发数量，一般默认CPU核数，可以不设置
CELERY_WORKER_CONCURRENCY = 2

# 每个worker执行了多少任务就会死掉，默认是无限的
CELERY_WORKER_MAX_TASKS_PER_CHILD = 200

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('sjxf', Exchange('sjxf'), routing_key="sjxf")
)

CELERY_ROUTES = {
    "sjxf.data_push": "sjxf"  # 将数据下发作业路由到单独的队列
}

CELERY_BEAT_SCHEDULE = {
    'sync_sjxf_task_status': {
        'task': 'sjxf.tasks.check_task_result',
        'schedule': datetime.timedelta(minutes=5)
    }
}

# 保存权限菜单
PERMISSION_URL_KEY = 'url_key'
PERMISSION_MENU_KEY = 'menu_key'

# 配置URL权限白名单
SAFE_URL = [
    '/users/login/',
    '/users/logout/',
    '/admin/.*',
    '/tailf/'
]
# 配置登录页面
LOGIN_URL = '/users/login/'

# 指定ASGI的路由地址
# ASGI_APPLICATION = 'Sanctuary.routing.application'

# test
TAILF = {
    1: '/var/log/messages',
}
