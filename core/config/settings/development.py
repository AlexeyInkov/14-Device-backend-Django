from .base import *


if IS_RUNNING_TESTS:
    DEBUG = False
else:
    DEBUG = "True" == os.environ.get("DJANGO_DEBUG", True)

print(f"{DEBUG=}")


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Development options
def show_toolbar(request: HttpRequest) -> bool:
    if DEBUG and not IS_RUNNING_TESTS:
        if request.META.get("REMOTE_ADDR") not in INTERNAL_IPS:
            logger.error(
                "Local address is not in INTERNAL_IPs",
                {
                    "error": {
                        "remote_addr": request.META.get("REMOTE_ADDR"),
                        "INTERNAL_IPs": INTERNAL_IPS,
                    }
                },
            )
        return True


if not IS_RUNNING_TESTS:
    # Swagger
    INSTALLED_APPS += [
        "rest_framework_swagger",
        "drf_yasg",
    ]
    # Debug toolbar
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    DEBUG_TOOLBAR_PANELS = (
        # "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.alerts.AlertsPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        # "debug_toolbar.panels.redirects.RedirectsPanel",
        # "debug_toolbar.panels.profiling.ProfilingPanel",
        "cachalot.panels.CachalotPanel",  # Cachalot
    )

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        # 'INSERT_BEFORE': '<head>',
        "UPDATE_ON_FETCH": True,
        "SQL_WARNING_THRESHOLD": 20,
        "ROOT_TAG_EXTRA_ATTRS": "hx-preserve",
        # 'EXCLUDE_URLS': ('/admin',),  # не работает, но в разработке есть...
        "INTERCEPT_REDIRECTS": False,
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django": {
            "format": "{name} {levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        # "file": {
        #     "class": "logging.FileHandler",
        #     "level": "WARNING",
        #     "filename": f"{BASE_DIR.parent}/log/django_warning.log",
        #     "formatter": "django.server",
        # },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "django",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "formatter": "django",
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "django.template": {
            "formatter": "django.template",
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "formatter": "django.request",
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        # "django.db": {
        #     "formatter": "django.db",
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": True,
        # },
        "django.server": {
            "formatter": "django.server",
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
