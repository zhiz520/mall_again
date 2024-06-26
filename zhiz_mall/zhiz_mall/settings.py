"""
Django settings for zhiz_mall project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# https://gitee.com/itcastitheima/shunyi_git_42.git 远程仓库地址

import os
from datetime import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#ctl + K  来进行 git的 git add commit 的操作
# ctl + shift+k 来进行 git push

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+qiwhqle^zz4=zjq%q!buk81_5$t3nxk0+^%fm90iq22d=n3b('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.zhiz.mall','127.0.0.1','localhost', 'www.meiduo.site']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',
    'apps.verifications',
    'apps.oauth',
    'apps.areas',
    'apps.goods',
    'apps.contents',
    # 'apps.carts',
    # 'apps.orders',
    # 'apps.pay',
    # # CORS
    'corsheaders',
    # # haystack
    'haystack',
    # 'django_crontab',
]

MIDDLEWARE = [
    # CORS 的配置放在最上边
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zhiz_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'zhiz_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123',  # 数据库用户密码
        'NAME': 'zhizhi_mall',  # 数据库名字
        'OPTIONS':{
            'init_command': "SET sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 8306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123',  # 数据库用户密码
        'NAME': 'zhizhi_mall'  # 数据库名字
    }
}

# DATABASE_ROUTERS = ['utils.db_router.MasterSlaveDBRouter']

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#############django-redis###########################
CACHES = {
    "default": {        #省市区数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # 用于保存session数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "code": {  # 用于保存session数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 用于保存浏览记录数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 用于保存购物车数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 配置日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
        },
        'file': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'myapp.log',
            'maxBytes': 10240,  # 10MB
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # 通用logger
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {  # Django的默认logger
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'myapp': {  # 自定义的logger
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


##############################
# 通过提供一个值给AUTH_USER_MODEL设置，指向自定义的模型，Django允许你覆盖默认的User模型：
# 这个点式路径包含Django应用的名称（必须位于你的INSTALLED_APPS中），和要用作User模型的Django模型的名称。
AUTH_USER_MODEL = 'users.User'

#####CORS#######################

# CORS  白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.zhiz.mall:8080',
    'http://www.zhiz.mall:8000',
    'http://www.meiduo.site:8080',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# QQ登录参数
# 我们申请的 客户端id
QQ_CLIENT_ID = '101474184'
# 我们申请的 客户端秘钥
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
# 登录成功后回调的路径
QQ_REDIRECT_URI = 'http://www.zhiz.mall:8080/oauth_callback.html'


############邮件发送相关###########################
#  让django的哪个类来发送邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 邮件服务器的主机和端口号
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25

# 使用我的 163服务器 和 授权码
#发送邮件的邮箱
EMAIL_HOST_USER = 'qi_rui_hua@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '123456abc'


#收件人看到的发件人
EMAIL_FROM = '枝枝<qi_rui_hua@163.com>'


#########加载自定义文件存储类#######################
# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = 'utils.storage1.MyStorage'


#########ES的配置#################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
# 设置搜索 每页返回的记录条数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5


# #########定时任务##############

# """
# # 元素的第一个参数是 频次
# 分 时 日 月 周    命令

# M: 分钟（0-59）。每分钟用 * 或者 */1 表示
# H：小时（0-23）。（0表示0点）
# D：天（1-31）。
# m: 月（1-12）。
# d: 一星期内的天（0~6，0为星期天）。

# # 元素的第二个参数是 定时任务（函数）
# """
# CRONJOBS = [
#     ('*/1 * * * *','apps.contents.crons.generic_meiduo_index','>> ' + os.path.join(BASE_DIR, 'logs/crontab.log'))

# ]

# ######################支付宝支付相关##################################

# ALIPAY_APPID = '2016091600523030'
# ALIPAY_DEBUG = True
# ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
# ALIPAY_RETURN_URL = 'http://www.zhiz.mall:8080/pay_success.html'
# APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'apps/pay/key/app_private_key.pem')
# ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'apps/pay/key/alipay_public_key.pem')