# coding=utf-8
"""Project level url handler."""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('mapserver.urls')),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
