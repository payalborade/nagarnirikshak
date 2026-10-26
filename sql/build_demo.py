"""Injects the sample operational data (same seed as schema.sql) into docs/index.html.
Run:  python sql/build_demo.py"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import generate_seed as g

def main():
    _, rows = g.read_dataset()
    seed = next(s for s in range(1, 2000) if len(g.build(s, rows)["flagged"]) == g.TARGET_FLAGGED)
    D = g.build(seed, rows)
    inprog = {m["light"] for m in D["maint"] if m["status"] == "IN PROGRESS"}
    openl = {f["light"] for f in D["fails"] if f["res"] is None}
    def status(i):  # same result as the seed script
        return ("REPLACEMENT REVIEW" if i in D["flagged"] else "MAINTENANCE" if i in inprog
                else "FAULTY" if i in openl else "ACTIVE")
    data = {
        "loc": {"LOC_%02d" % (i + 1): [r[1], r[2].strip(), g.STREETS[r[2].strip()][0]] for i, r in enumerate(rows)},
        "lights": [[l["id"], l["loc"], l["type"], l["w"], l["inst"].isoformat(), status(l["id"])] for l in D["lights"]],
        "fails": [[f["id"], f["light"], f["date"].isoformat(), f["type"], f["res"].isoformat() if f["res"] else None] for f in D["fails"]],
        "maint": [[m["id"], m["light"], m["status"], m["con"]] for m in D["maint"]],
        "exp": [[e["light"], e["amount"], e["maint"]] for e in D["exp"]],
        "cons": [[c[0], c[1], c[2]] for c in g.CONTRACTORS],
        "insp": {n["light"]: n["cond"] for n in D["insp"]},
    }
    p = pathlib.Path(__file__).parent.parent / "docs" / "index.html"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"/\*DATA\*/.*?/\*END\*/", lambda m: "/*DATA*/" + json.dumps(data, separators=(",", ":")) + "/*END*/", s, flags=re.S)
    p.write_text(s, encoding="utf-8")
    print("seed", seed, "flagged", D["flagged"])

main()
