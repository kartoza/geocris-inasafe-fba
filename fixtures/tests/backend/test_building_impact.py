from psycopg2.extras import DictCursor

from tests.backend import DatabaseTestCase


class TestBuildingImpact(DatabaseTestCase):

    def test_building_summary(self):
        self.assertSQLResult(
            self.sql_path('mv_building_summary.sql'),
            self.json_path('mv_building_summary.json'),
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

            # check building summary

            def _test_summary_stats(self, results):
                self.assertTrue(results)
                keys_to_check = [
                    'residential',
                    'clinic_dr',
                    'fire_station',
                    'school',
                    'university',
                    'government',
                    'hospital',
                    'police_station',
                    'supermarket',
                    'sports_facility',
                ]
                for row in results:
                    sum_exposed_count = 0
                    sum_total_count = 0
                    for key in keys_to_check:
                        # Do sanity count check
                        # exposed count must less than total count
                        exposed_count = row[
                            '{0}_hazarded_building_count'.format(key)]
                        total_count = row[
                            '{0}_building_count'.format(key)]
                        self.assertLessEqual(exposed_count, total_count)
                        sum_exposed_count += exposed_count
                        sum_total_count += total_count

                    # Sanity check
                    # total exposed count must be less or equal from
                    # total count (because there might be
                    # uncategorized building) from the field
                    self.assertLessEqual(
                        sum_exposed_count, row['hazarded_building_count'])
                    # Same reason with total count
                self.assertLessEqual(
                    sum_total_count, row['building_count'])

            mv_district_summary = self.sql_path(
                'mv_hazard_event_district_summary.sql')
            self.execute_sql_file(mv_district_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            mv_sub_district_summary = self.sql_path(
                'mv_hazard_event_sub_district_summary.sql')
            self.execute_sql_file(mv_sub_district_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            mv_village_summary = self.sql_path(
                'mv_hazard_event_village_summary.sql')
            self.execute_sql_file(mv_village_summary, cursor=c)
            results = c.fetchall()

            _test_summary_stats(self, results)

            self.dbc.conn.rollback()

    def test_generate_spreadsheets(self):
        # Spreadsheet generator relies on Geoserver to get the map,
        # So we can't use rollback because that means GeoServer won't have
        # the data to display the map
        def _cleanup(self, c):

            cleanup = self.sql_path('hazard_event_cleanup.sql')
            self.execute_sql_file(cleanup, cursor=c)

        self.dbc.conn.autocommit = True
        # Cleanup first in case of artifacts from previous tests
        with self.dbc.conn.cursor(cursor_factory=DictCursor) as c:
            _cleanup(self, c)

        with self.dbc.conn.cursor(cursor_factory=DictCursor) as c:

            try:
                # populate hazard map model
                hazard_map = self.sql_path('hazard_map.sql')
                self.execute_sql_file(hazard_map, cursor=c)

                # populate hazard event data
                hazard_insert = self.sql_path('hazard.sql')
                self.execute_sql_file(hazard_insert, cursor=c)

                # make sure materialized views are refreshed
                calculate_impact = self.sql_path('calculate_impact.sql')
                self.execute_sql_file(calculate_impact, cursor=c)

                # trigger spreadsheets calculations
                spreadsheet = self.sql_path('spreadsheet.sql')
                self.execute_sql_file(spreadsheet, cursor=c)
                results = c.fetchone()

                self.assertEqual(results[0], 'OK')

                spreadsheet_reports = self.sql_path('spreadsheet_content.sql')
                self.execute_sql_file(spreadsheet_reports, cursor=c)
                results = c.fetchone()

                self.assertTrue(results['spreadsheet'])
            finally:
                cleanup = self.sql_path('hazard_event_cleanup.sql')
                self.execute_sql_file(cleanup, cursor=c)

    def test_hazard_event_queue(self):
        # Test inserting hazard_event using hazard_event_queue table


        # Spreadsheet generator relies on Geoserver to get the map,
        # So we can't use rollback because that means GeoServer won't have
        # the data to display the map
        def _cleanup(self, c):

            cleanup = self.sql_path('hazard_event_cleanup.sql')
            self.execute_sql_file(cleanup, cursor=c)

        self.dbc.conn.autocommit = True
        # Cleanup first in case of artifacts from previous tests
        with self.dbc.conn.cursor(cursor_factory=DictCursor) as c:
            _cleanup(self, c)

        with self.dbc.conn.cursor(cursor_factory=DictCursor) as c:
            try:
                # populate hazard map model
                hazard_map = self.sql_path('hazard_map.sql')
                self.execute_sql_file(hazard_map, cursor=c)

                # populate hazard event queue data
                hazard_insert = self.sql_path('hazard_event_queue.sql')
                self.execute_sql_file(hazard_insert, cursor=c)

                # make sure queue exists
                self.execute_statement(
                    'select count(*) from hazard_event_queue', cursor=c)
                results = c.fetchone()
                self.assertTrue(results[0] > 0)

                # trigger event process
                process_hazard_event_queue = self.sql_path('process_hazard_event_queue.sql')
                self.execute_sql_file(process_hazard_event_queue, cursor=c)
                results = c.fetchone()
                # will return hazard_event_id
                hazard_event_id = results[0]
                self.assertTrue(hazard_event_id > 0)

                # trigger event analysis
                process_pending_analysis = self.sql_path(
                    'process_pending_analysis.sql')
                self.execute_sql_file(process_pending_analysis, cursor=c)
                results = c.fetchone()
                # will return OK
                self.assertEqual(results[0], 'OK')

                # should have spreadsheets
                self.execute_statement(
                    'select * from spreadsheet_reports where hazard_event_id = {}'.format(hazard_event_id),
                    cursor=c)
                results = c.fetchone()

                self.assertTrue(results['spreadsheet'])
            finally:
                cleanup = self.sql_path('hazard_event_cleanup.sql')
                self.execute_sql_file(cleanup, cursor=c)
