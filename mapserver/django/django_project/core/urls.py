# coding=utf-8
"""Project level url handler."""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mapserver.urls')),
    path('api/', include('fba.urls')),
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
