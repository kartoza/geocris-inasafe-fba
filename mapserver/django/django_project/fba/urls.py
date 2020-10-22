from django.urls import path, include
from rest_framework import routers

from fba.api_views.hazard_event import HazardEventAPI, HazardEventExtentAPI
from fba.api_views.recent_hazard import RecentHazardList
from fba.api_views.summary_stats import SummaryStatsAPI

router = routers.DefaultRouter()
router.register('hazard-event', HazardEventAPI)

urlpatterns = [
    path('hazard-event/recent/', RecentHazardList.as_view(),
         name='recent-hazard-list-api'),
    path('hazard-event/<id>/extent', HazardEventExtentAPI.as_view(),
         name='hazard-event-extent-api'),
    path('hazard-event/<id>/summary-stats/<admin_level>/',
         SummaryStatsAPI.as_view(),
         name='hazard-event-summary-stats-api'),
    path('hazard-event/<id>/summary-stats/'
         '<parent_admin_level>/<parent_admin_id>/<admin_level>/',
         SummaryStatsAPI.as_view(),
         name='hazard-event-summary-stats-drilldown-api'),
    path('', include(router.urls))
]
