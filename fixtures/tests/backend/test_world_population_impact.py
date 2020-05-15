from psycopg2.extras import DictCursor

from tests.backend import DatabaseTestCase


class TestWorldPopulationImpact(DatabaseTestCase):

    def test_population_summary(self):
        self.assertSQLResult(
            self.sql_path('world_pop_district_stats.sql'),
            self.json_path('world_pop_district_stats.json'),
        )

        self.assertSQLResult(
            self.sql_path('world_pop_sub_district_stats.sql'),
            self.json_path('world_pop_sub_district_stats.json'),
        )

        self.assertSQLResult(
            self.sql_path('world_pop_village_stats.sql'),
            self.json_path('world_pop_village_stats.json'),
        )

    def test_hazard_exposure_intersections(self):
        self.dbc.conn.autocommit = False
        with self.dbc.conn.cursor(cursor_factory=DictCursor) as c:

            # populate hazard map model
            hazard_map = self.sql_path('hazard_map.sql')
            self.execute_sql_file(hazard_map, cursor=c)

            # populate hazard event data
            hazard_insert = self.sql_path('hazard.sql')
            self.execute_sql_file(hazard_insert, cursor=c)

            # check summary

            def _test_summary_stats(self, results):
                self.assertTrue(results)
                for row in results:
                    # Sanity check
                    # total exposed count must be less or equal from
                    # total count (because there might be
                    # uncategorized) from the field
                    self.assertLessEqual(
                        row['hazarded_population_count'],
                        row['population_count'])

            mv_district_summary = self.sql_path(
                'mv_hazard_event_world_pop_district_summary.sql')
            self.execute_sql_file(mv_district_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            mv_sub_district_summary = self.sql_path(
                'mv_hazard_event_world_pop_sub_district_summary.sql')
            self.execute_sql_file(mv_sub_district_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            mv_village_summary = self.sql_path(
                'mv_hazard_event_world_pop_village_summary.sql')
            self.execute_sql_file(mv_village_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            self.dbc.conn.rollback()
