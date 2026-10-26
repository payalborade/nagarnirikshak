# Nagar Nirikshan

Municipal infrastructure failure & root-cause intelligence for Pune Municipal Corporation ward areas.

> Student DBMS project styled after Indian government portals. **Not an official website.** Ward data comes from the provided `dataset.csv`.

**Live demo:** https://<username>.github.io/<repo>/

## What is in this version
- `docs/index.html`: standalone dashboard (no server, no database). Hero stats, city KPIs, poles by zone and ward, smart insights, Excel-style dataset viewer with CSV download, English/मराठी, themes, text size.

- Operations & risk (alert banner, risk score, charts, top-risk table) and the Repair → Replace roadmap slide, using sample records.
- `sql/`: Oracle `schema.sql` (tables, views, PL/SQL, triggers, seed), `generate_seed.py`, `build_demo.py`, `dataset.csv`.
  Run `python sql/generate_seed.py` then `python sql/build_demo.py` to regenerate.

## Run locally with Oracle
```
pip install -r requirements.txt
copy .env.example .env      # then edit DB_USER, DB_PASSWORD, DB_DSN
# run sql/schema.sql in SQL Developer or SQL*Plus
python app.py               # http://127.0.0.1:5000
```
`app.py` serves the same `docs/index.html` and adds the JSON API (`/api/bootstrap`, `/api/failures`, `/api/run-review`, `/dataset.csv`).

## Publish on GitHub Pages
1. Create an empty public repository.
2. Upload the contents of this folder (including `.gitignore`).
3. Settings → Pages → Deploy from branch `main`, folder `/docs`.

## License
MIT
