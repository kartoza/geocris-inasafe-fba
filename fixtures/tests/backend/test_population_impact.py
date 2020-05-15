from psycopg2.extras import DictCursor

from tests.backend import DatabaseTestCase


class TestPopulationImpact(DatabaseTestCase):

    def test_population_summary(self):
        self.assertSQLResult(
            self.sql_path('mv_population_summary.sql'),
            self.json_path('mv_population_summary.json'),
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
                keys_to_check = [
                    'males',
                    'females',
                    'elderly',
                    'unemployed',
                ]
                for row in results:
                    for key in keys_to_check:
                        # Do sanity count check
                        # exposed count must less than total count
                        exposed_count = row[
                            '{0}_hazarded_population_count'.format(key)]
                        total_count = row[
                            '{0}_population_count'.format(key)]
                        self.assertLessEqual(exposed_count, total_count)

                    # Sanity check
                    # total exposed count must be less or equal from
                    # total count (because there might be
                    # uncategorized) from the field
                    self.assertLessEqual(
                        row['hazarded_population_count'],
                        row['population_count'])

            mv_district_summary = self.sql_path(
                'mv_hazard_event_population_district_summary.sql')
            self.execute_sql_file(mv_district_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            mv_sub_district_summary = self.sql_path(
                'mv_hazard_event_population_sub_district_summary.sql')
            self.execute_sql_file(mv_sub_district_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            mv_village_summary = self.sql_path(
                'mv_hazard_event_population_village_summary.sql')
            self.execute_sql_file(mv_village_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            self.dbc.conn.rollback()
