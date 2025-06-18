import os

from .base import *

Debug = False

# Cachalot
INSTALLED_APPS += [
    # Cache
    "cachalot",
]
CACHALOT_TABLE_KEYGEN = "cachalot.utils.get_table_cache_key"
CACHALOT_DATABASES = ("default",)  # 'supported_only')
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Prometheus
INSTALLED_APPS += [
    "django_prometheus",
]

# EMAIL_BACKEND
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "'smtp.mailgun.org'"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
