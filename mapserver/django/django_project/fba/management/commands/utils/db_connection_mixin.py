import psycopg2 as driv
from postgis.psycopg import register


class BoundaryDBConnectionMixin:

    def create_connection(self):
        try:
            conn = driv.connect(database='geocris',
                                user='cdema',
                                password='cdema',
                                host='192.168.100.6',
                                port='35432')
            register(conn)
            return conn
        except driv.OperationalError as e:
            print(e)
        return None

    def get_table_header(self, conn, schema_name, table_name):
        try:
            with conn.cursor() as cur:
                sql = f'SELECT * FROM {schema_name}.{table_name} LIMIT 1'
                cur.execute(sql)
                return [d[0] for d in cur.description]
        except:
            return []

    def get_admin_data(self, conn, schema_name, table_name):
        try:
            with conn.cursor() as cur:
                sql = f'SELECT * FROM {schema_name}.{table_name}'
                cur.execute(sql)
                return cur.fetchall()
        except:
            return []

    def get_all_tables(self, conn, schema):
        query = f"""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = '{schema}' AND table_type = 'BASE TABLE'
            """
        with conn.cursor() as cur:
            cur.execute(query)
            return [r[0] for r in cur.fetchall()]

    def get_all_schemas(self, conn):
        try:
            with conn.cursor() as cur:
                query = (
                    'SELECT schema_name FROM information_schema.schemata '
                    'WHERE length(schema_name) = 3'
                )
                cur.execute(query)
                schemas_list = cur.fetchall()
                return [r[0] for r in schemas_list]
        except:
            return []
