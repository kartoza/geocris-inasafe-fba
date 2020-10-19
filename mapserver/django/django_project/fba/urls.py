from django.urls import path, include
from rest_framework import routers

from fba.api_views.hazard_event import HazardEventAPI, HazardEventExtentAPI
from fba.api_views.recent_hazard import RecentHazardList


router = routers.DefaultRouter()
router.register('hazard-event', HazardEventAPI)

urlpatterns = [
    path('hazard-event/recent/', RecentHazardList.as_view(),
         name='recent-hazard-list-api'),
    path('hazard-event/<id>/extent', HazardEventExtentAPI.as_view(),
         name='hazard-event-extent-api'),
    path('', include(router.urls))
]
