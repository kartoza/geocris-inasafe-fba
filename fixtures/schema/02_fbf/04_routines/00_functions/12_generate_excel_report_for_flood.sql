
--
-- Name: kartoza_fba_generate_excel_report_for_hazard(integer); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.kartoza_fba_generate_excel_report_for_hazard;
CREATE OR REPLACE FUNCTION public.kartoza_fba_generate_excel_report_for_hazard(hazard_event_id integer) RETURNS character varying
    LANGUAGE plpython3u
    AS $_$
    import io
    import sys
    import json
    plpy.execute("select * from satisfy_dependency('xlsxwriter')")
    plpy.execute("select * from satisfy_dependency('openpyxl')")
    result = plpy.execute("select value from config where key = 'WMS_BASE_URL'")
    wms_base_url = json.loads(result[0]['value'])

    from smartexcel.smart_excel import SmartExcel
    from smartexcel.fbf.data_model import FbfHazardData
    from smartexcel.fbf.definition import FBF_DEFINITION

    excel = SmartExcel(
        output=io.BytesIO(),
        definition=FBF_DEFINITION,
        data=FbfHazardData(
            wms_base_url=wms_base_url,
            hazard_event_id=hazard_event_id,
            pl_python_env=True
        )
    )

    excel.dump()

    # Rizky:
    # Optimization notes:
    # - Using plpy.prepare and let plpy convert bytestring to be sent is very slow
    # - We convert bytes into hex directly and put it in a query statement
    # - Explanation of the syntax. The column needs to be a bytea
    #   syntax uses E'\\x[each bytes as hex code]'. Since we are using python,
    #   We escape backslash twice. So, in python string, the format becomes:
    #   E'\\\\x[the bytes string as hex code]'. For example:
    #   E'\\\\x01ff77de
    query = "UPDATE spreadsheet_reports SET spreadsheet = (E'\\\\x{}') where hazard_event_id = ({})".format(excel.output.getvalue().hex(), hazard_event_id)
    plpy.execute(query)

    return "OK"
$_$;
