from django.urls import path, include
from rest_framework import routers

from fba.api_views.hazard_event import HazardEventAPI, HazardEventExtentAPI
from fba.api_views.recent_hazard import RecentHazardList
from fba.api_views.summary_stats import SummaryStatsAPI, SummaryStatsAllAPI

router = routers.DefaultRouter()
router.register('hazard-event', HazardEventAPI)

urlpatterns = [
    path('hazard-event/recent/', RecentHazardList.as_view(),
         name='recent-hazard-list-api'),
    path('hazard-event/<id>/extent', HazardEventExtentAPI.as_view(),
         name='hazard-event-extent-api'),
    path('hazard-event/<id>/summary-stats/all',
         SummaryStatsAllAPI.as_view(),
         name='hazard-event-summary-stats-all-api'),
    # This one is so that it will not match <admin_level> path
    # We could use re_path, but this one is easier to understand
    path('hazard-event/<id>/summary-stats/all/',
         SummaryStatsAllAPI.as_view()),
    path('hazard-event/<id>/summary-stats/<admin_level>/',
         SummaryStatsAPI.as_view(),
         name='hazard-event-summary-stats-api'),
    path('hazard-event/<id>/summary-stats/<admin_level>/<admin_id>',
         SummaryStatsAPI.as_view(),
         name='hazard-event-summary-stats-single-region-api'),
    path('hazard-event/<id>/summary-stats/'
         '<parent_admin_level>/<parent_admin_id>/<admin_level>/',
         SummaryStatsAPI.as_view(),
         name='hazard-event-summary-stats-drilldown-api'),
    path('', include(router.urls))
]
