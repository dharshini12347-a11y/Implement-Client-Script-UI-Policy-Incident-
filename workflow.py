from datetime import datetime, timezone
from .db import get_db
from .rules import apply_client_change, validate_on_submit, validate_list_edit

def now():
    return datetime.now(timezone.utc).isoformat()

def row_dict(row):
    return dict(row) if row else None

def create_incident(payload):
    with get_db() as con:
        ts = now()
        next_id = con.execute("SELECT COALESCE(MAX(id),0)+1 FROM incidents").fetchone()[0]
        number = f"INC{int(next_id):07d}"
        cur = con.execute("""
            INSERT INTO incidents
            (number,caller,category,subcategory,short_description,description,impact,urgency,
             assigned_to,assignment_group,state,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            number,payload["caller"],payload["category"],payload["subcategory"],
            payload["short_description"],payload["description"],payload["impact"],
            payload["urgency"],payload["assigned_to"],payload["assignment_group"],
            payload["state"],ts,ts
        ))
        return row_dict(con.execute("SELECT * FROM incidents WHERE id=?", (cur.lastrowid,)).fetchone())

def get_incident(incident_id):
    with get_db() as con:
        return row_dict(con.execute("SELECT * FROM incidents WHERE id=?", (incident_id,)).fetchone())

def list_incidents():
    with get_db() as con:
        return [row_dict(r) for r in con.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()]

def update_incident(incident_id, payload, source="form"):
    current = get_incident(incident_id)
    if not current:
        raise ValueError("Incident not found")

    if source == "list" and payload.get("state") != current["state"]:
        ok, error = validate_list_edit("state")
        if not ok:
            raise PermissionError(error)

    if payload.get("impact") != current["impact"]:
        changed, _ = apply_client_change(current, "impact", payload["impact"])
        payload = {**payload, "urgency": changed["urgency"]}

    candidate = {**current, **payload}
    ok, error = validate_on_submit(candidate)
    if not ok:
        raise PermissionError(error)

    with get_db() as con:
        ts = now()
        con.execute("""
        UPDATE incidents SET caller=?,category=?,subcategory=?,short_description=?,description=?,
        impact=?,urgency=?,assigned_to=?,assignment_group=?,state=?,updated_at=? WHERE id=?
        """, (
            candidate["caller"],candidate["category"],candidate["subcategory"],
            candidate["short_description"],candidate["description"],candidate["impact"],
            candidate["urgency"],candidate["assigned_to"],candidate["assignment_group"],
            candidate["state"],ts,incident_id
        ))
    return get_incident(incident_id)

def change_impact(incident_id, impact):
    current = get_incident(incident_id)
    if not current:
        raise ValueError("Incident not found")
    updated, messages = apply_client_change(current, "impact", impact)
    ok, error = validate_on_submit(updated)
    return updated, messages, ok, error
