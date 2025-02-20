from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="device_control",
        default_version="v1",
    ),
    public=True,
    permission_classes=[
        AllowAny,
    ],
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path(
            "docs/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path("", include("apps.frontend.urls")),
        path("auth/", include("apps.my_auth.urls")),
        path("v1/page/", include("apps.for_page.urls")),
        path("v1/device_control/", include("apps.device.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + debug_toolbar_urls()
)
