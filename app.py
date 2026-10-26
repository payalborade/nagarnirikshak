"""NagarNirikshan: Flask + Oracle (python-oracledb thin mode)."""
import csv
import io
import os
import pathlib
from datetime import date, datetime

import oracledb
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me")
SHELL = pathlib.Path(__file__).parent / "docs" / "index.html"  # same UI as the demo
HEADER = ["City Name", "Zone Name", "Ward Name", "Number of Poles", "No. of LED Bulbs",
          "No. of poles with conventional / non LED Lights", "Total length of roads (in km)",
          "Number of street lights / poles per km of road", "Total no. of streets",
          "No. of streets with adequate street lighting facilties"]
FTYPES = ["Bulb Burnout", "Power Surge", "Wiring Fault", "Driver Failure", "Pole Damage", "Other"]
_pool = None


def pool():
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                                     dsn=os.getenv("DB_DSN"), min=1, max=5, increment=1)
    return _pool


def rows(sql, **binds):
    with pool().acquire() as con, con.cursor() as cur:
        cur.execute(sql, binds)
        return cur.fetchall()


def num(v):
    return None if v is None else (int(v) if float(v) == int(v) else float(v))


def cell(v):
    return "NA" if v is None else str(num(v)) if not isinstance(v, str) else v


def ward_rows():
    return [[cell(x) for x in r] for r in rows(
        "SELECT city_name, zone_name, ward_name, number_of_poles, led_bulbs, conventional_poles, "
        "road_length_km, lights_per_km, total_streets, adequate_streets "
        "FROM WARD_INFRASTRUCTURE ORDER BY ward_id")]


def page(tab):
    html = SHELL.read_text(encoding="utf-8")
    html = html.replace("<body>", '<body data-tab="%s">' % tab, 1)
    return html.replace("<script>", '<script>window.NN_API="/api";</script>\n<script>', 1)


for _path, _tab in [("/", "dashboard"), ("/assets", "assets"), ("/failures", "failures"),
                    ("/contractors", "contractors"), ("/audit", "audit"), ("/solutions", "solutions"),
                    ("/review", "review"), ("/dataset", "dataset"), ("/roadmap", "roadmap")]:
    app.add_url_rule(_path, "page_" + _tab, (lambda t: lambda: page(t))(_tab))


@app.errorhandler(Exception)
def on_error(e):
    code = getattr(e, "code", 500) if isinstance(getattr(e, "code", None), int) else 500
    return jsonify(error=str(e)), code


@app.get("/api/bootstrap")
def bootstrap():
    return jsonify(
        dataset={"header": HEADER, "rows": ward_rows()},
        loc={r[0]: [r[1], r[2], r[3]] for r in rows(
            "SELECT location_id, ward_no, area_name, street_name FROM LOCATION ORDER BY location_id")},
        lights=[dict(id=r[0], loc=r[1], type=r[2], w=num(r[3]), inst=r[4], st=r[5]) for r in rows(
            "SELECT light_id, location_id, light_type, power_rating, "
            "TO_CHAR(installation_date,'YYYY-MM-DD'), current_status FROM STREET_LIGHT ORDER BY light_id")],
        fails=[dict(id=r[0], light=r[1], date=r[2], type=r[3], desc=r[4], res=r[5]) for r in rows(
            "SELECT failure_id, light_id, TO_CHAR(failure_date,'YYYY-MM-DD'), failure_type, "
            "failure_description, TO_CHAR(resolved_date,'YYYY-MM-DD') FROM FAILURE "
            "ORDER BY failure_date DESC, failure_id DESC")],
        cons=[dict(id=r[0], name=r[1], co=r[2]) for r in rows(
            "SELECT contractor_id, contractor_name, company_name FROM CONTRACTOR ORDER BY contractor_id")],
        maint=[dict(id=r[0], light=r[1], con=r[2], amt=num(r[3]), status=r[4]) for r in rows(
            "SELECT m.maintenance_id, m.light_id, m.contractor_id, SUM(e.amount), m.status "
            "FROM MAINTENANCE m LEFT JOIN EXPENDITURE e ON e.maintenance_id = m.maintenance_id "
            "GROUP BY m.maintenance_id, m.light_id, m.contractor_id, m.status ORDER BY m.maintenance_id")],
        insp=[dict(light=r[0], cond=r[1]) for r in rows(
            "SELECT light_id, condition_status FROM (SELECT light_id, condition_status, ROW_NUMBER() OVER "
            "(PARTITION BY light_id ORDER BY inspection_date DESC, inspection_id DESC) rn FROM INSPECTION) "
            "WHERE rn = 1")],
        audit=[list(r) for r in rows(
            "SELECT light_id, old_status, new_status, TO_CHAR(change_timestamp,'YYYY-MM-DD HH24:MI:SS') "
            "FROM LIGHT_AUDIT_LOG ORDER BY change_timestamp DESC, audit_id DESC FETCH FIRST 60 ROWS ONLY")],
    )


@app.post("/api/failures")
def add_failure():
    b = request.get_json(silent=True) or {}
    light, ftype, desc = b.get("light", ""), b.get("type", ""), (b.get("desc") or "").strip()
    try:
        fdate = datetime.strptime(b.get("date", ""), "%Y-%m-%d").date()
    except ValueError:
        return jsonify(error="Invalid date."), 400
    if fdate > date.today():
        return jsonify(error="Date cannot be in the future."), 400
    if ftype not in FTYPES:
        return jsonify(error="Invalid failure type."), 400
    if not desc or len(desc) > 255:
        return jsonify(error="Description is required (max 255 characters)."), 400
    if not rows("SELECT 1 FROM STREET_LIGHT WHERE light_id = :l", l=light):
        return jsonify(error="Unknown light."), 404
    with pool().acquire() as con, con.cursor() as cur:
        cur.execute("SELECT SEQ_FAILURE_ID.NEXTVAL FROM dual")
        fid = "FAIL_%02d" % cur.fetchone()[0]
        cur.execute("INSERT INTO FAILURE (failure_id, light_id, failure_date, failure_type, failure_description) "
                    "VALUES (:i, :l, TO_DATE(:d,'YYYY-MM-DD'), :t, :s)",
                    i=fid, l=light, d=fdate.isoformat(), t=ftype, s=desc)
        con.commit()  # trigger TRG_AUTO_LOG_FAILURE_STATUS sets the light to FAULTY
    return jsonify(id=fid), 201


@app.post("/api/failures/<fid>/resolve")
def resolve(fid):
    with pool().acquire() as con, con.cursor() as cur:
        cur.execute("UPDATE FAILURE SET resolved_date = TRUNC(SYSDATE) "
                    "WHERE failure_id = :i AND resolved_date IS NULL", i=fid)
        if cur.rowcount == 0:
            return jsonify(error="Failure not found or already resolved."), 404
        cur.execute("UPDATE STREET_LIGHT s SET current_status = 'ACTIVE' "
                    "WHERE s.light_id = (SELECT light_id FROM FAILURE WHERE failure_id = :i) "
                    "AND s.current_status = 'FAULTY' AND NOT EXISTS "
                    "(SELECT 1 FROM FAILURE f WHERE f.light_id = s.light_id AND f.resolved_date IS NULL)", i=fid)
        con.commit()
    return jsonify(ok=True)


@app.post("/api/run-review")
def run_review():
    with pool().acquire() as con, con.cursor() as cur:
        out = cur.var(int)
        cur.callproc("EVALUATE_REPLACEMENT_REVIEW", [3, 5000, out])
        return jsonify(flagged=int(out.getvalue() or 0))


@app.get("/dataset.csv")
def dataset_csv():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(HEADER)
    w.writerows(ward_rows())
    return Response("\ufeff" + buf.getvalue(), mimetype="text/csv; charset=utf-8",
                    headers={"Content-Disposition": "attachment; filename=dataset.csv"})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
