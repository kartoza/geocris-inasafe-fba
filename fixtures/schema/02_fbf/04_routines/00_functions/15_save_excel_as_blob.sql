
--
-- Name: save_excel_as_blob(); Type: FUNCTION; Schema: public; Owner: -
--
DROP FUNCTION IF EXISTS public.save_excel_as_blob;
CREATE FUNCTION public.save_excel_as_blob() RETURNS character varying
    LANGUAGE plpython3u
    AS $_$
  import sys
  sys.path.insert(0, '/usr/local/lib/python3.7/dist-packages')
  import xlsxwriter
  sys.path.insert(0, '/usr/local/lib/python3.7/dist-packages/SmartExcel/smartexcel')
  return sys.version_info
  # from smartexcel import smart_excel
  import io

  ouput = io.BytesIO()
  workbook = xlsxwriter.Workbook('hello.xlsx')
  worksheet = workbook.add_worksheet()
  worksheet.write('A1', 'Hello world')
  workbook.close()
  # plan = plpy.prepare("UPDATE hazard_event SET output = ($1)", ["bytea"])
  # plpy.execute(plan, [ouput])

  return ouput

$_$;

