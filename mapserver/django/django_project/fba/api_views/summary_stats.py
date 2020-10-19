from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from fba.models.hazard_event import HazardEvent
from fba.models.views import HazardEventExtent, \
    CensusPopulationSummarySubDistrictStats, BuildingSummaryDistrictStats, \
    BuildingSummarySubDistrictStats, CensusPopulationSummaryDistrictStats
from fba.serializers.common import SpatialExtentSerializer
from fba.serializers.hazard_event import HazardEventSerializer
from fba.serializers.views import BuildingSummaryDistrictSerializer, \
    BuildingSummarySubDistrictSerializer, \
    CensusPopulationSummaryDistrictSerializer, \
    CensusPopulationSummarySubDistrictSerializer


class SummaryStatsDistrictAPI(generics.ListAPIView):
    """API to return summary statistics of aggregate values:
    """

    def list(self, request, *args, **kwargs):
        # Attempt to fetch flood stats
        # Attempt to fetch roads stats
        # Attempt to fetch population stats
        id = kwargs.get('id')
        admin_level = kwargs.get('admin_level').replace('-', '_')
        building_models = {
            'district': BuildingSummaryDistrictStats,
            'sub_district': BuildingSummarySubDistrictStats
        }
        building_serializers = {
            'district': BuildingSummaryDistrictSerializer,
            'sub_district': BuildingSummarySubDistrictSerializer
        }
        population_models = {
            'district': CensusPopulationSummaryDistrictStats,
            'sub_district': CensusPopulationSummarySubDistrictStats
        }
        population_serializers = {
            'district': CensusPopulationSummaryDistrictSerializer,
            'sub_district': CensusPopulationSummarySubDistrictSerializer
        }
        building_stats = building_models[admin_level].objects.filter(
            flood_event__id=id
        )
        building_serializer = building_serializers[admin_level]
        population_stats = population_models[admin_level].objects.filter(
            flood_event__id=id
        )
        population_serializer = population_serializers[admin_level]


        # merge results:
        # stats = [
        #     {
        #         'country_id'
        #         'country_name'
        #         '<admin>_id'
        #         '<admin>_name'
        #         'building_stats': {
        #             counts... etc
        #         },
        #         'census_population_stats': {
        #             population_count...
        #         },
        #        'trigger_status'
        #     }
        # ]
        admin_id_field = f'{admin_level}_id'
        overall_stats = []
        population_admin_ids = [getattr(stat, admin_id_field) for stat in population_stats]
        building_admin_ids = [getattr(stat, admin_id_field) for stat in building_stats]
        unique_admin_ids = set(population_admin_ids).union(set(building_admin_ids))

        parent_level = {
            'district': {
                'parent_field': 'country_id',
                'parent_name_field': 'country_name',
                'parent_field_id': lambda _stat: _stat.district.country.country_code,
                'parent': lambda _stat: _stat.district.country
            },
            'sub_district': {
                'parent_field': 'district_id',
                'parent_name_field': 'district_name',
                'parent_field_id': lambda _stat: _stat.sub_district.district.dc_code,
                'parent': lambda _stat: _stat.sub_district.district
            }
        }

        parent_level_info = parent_level[admin_level]
        parent_field = parent_level_info['parent_field']
        parent_name_field = parent_level_info['parent_name_field']
        for admin_id in unique_admin_ids:
            result = {
                admin_id_field: admin_id
            }

            pop_stat = population_stats.filter(**{
                admin_id_field: admin_id
            }).first()
            building_stat = building_stats.filter(**{
                admin_id_field: admin_id
            }).first()

            default_stat = pop_stat or building_stat

            # Pull out basic metadata
            result['name'] = getattr(pop_stat, admin_level).name
            parent_administrative = parent_level_info['parent'](default_stat)
            parent_administrative_id = parent_level_info['parent_field_id'](default_stat)
            result[parent_field] = parent_administrative_id
            result[parent_name_field] = parent_administrative.name

            # merge statistics
            result['census_population_stats'] = population_serializer(
                pop_stat).data if pop_stat else {}
            result['building_stats'] = building_serializer(
                building_stat).data if building_stat else {}

            overall_stats.append(result)

        # Apply sort criteria.
        # Default sort by parent name, then current admin level name
        overall_stats.sort(key=lambda stat: (stat[parent_name_field], stat['name']))
        return Response(overall_stats)
