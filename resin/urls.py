import re

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, re_path, include
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path("health/", lambda request: HttpResponse("OK")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.SERVE_STATIC:
    from django.views.static import serve

    static_url = r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/"))

    urlpatterns.append(re_path(static_url, serve, {'document_root': settings.STATIC_ROOT}))

