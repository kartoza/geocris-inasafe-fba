# coding=utf-8
"""Project level url handler."""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from core.views.template import HomeView, MapView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^map/', MapView.as_view(), name='map'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
