from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client=TestClient(app)
def setup_module(): init_db()

def make(**extra):
    d={"caller":"Test User","category":"Software","subcategory":"","short_description":"Test incident",
       "description":"Testing","impact":"3","urgency":"3","assigned_to":"","assignment_group":"","state":"1"}
    d.update(extra)
    r=client.post("/api/incidents",json=d)
    assert r.status_code==200, r.text
    return r.json()

def clean(i):
    return {k:i[k] for k in ["caller","category","subcategory","short_description","description","impact","urgency","assigned_to","assignment_group","state"]}

def test_health():
    r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"

def test_onchange_sets_urgency():
    i=make(); r=client.post(f"/api/incidents/{i['id']}/impact?impact=1")
    assert r.status_code==200; assert r.json()["incident"]["urgency"]=="1"
    assert r.json()["ui_state"]["urgency_read_only"] is True

def test_onsubmit_blocks_missing_assigned_to():
    i=make(); p=clean(i); p.update(impact="1",urgency="1")
    r=client.patch(f"/api/incidents/{i['id']}?source=form",json=p)
    assert r.status_code==422 and "Assigned To is mandatory" in r.json()["detail"]

def test_high_impact_save_succeeds_with_assigned_to():
    i=make(); p=clean(i); p.update(impact="1",urgency="1",assigned_to="Alex",assignment_group="Hardware")
    r=client.patch(f"/api/incidents/{i['id']}?source=form",json=p)
    assert r.status_code==200 and r.json()["assigned_to"]=="Alex"

def test_list_state_edit_blocked():
    i=make(); r=client.post(f"/api/incidents/{i['id']}/list-state-edit?state=2")
    assert r.status_code==422 and "State cannot be updated" in r.json()["detail"]

def test_form_state_update_allowed():
    i=make(); p=clean(i); p["state"]="2"
    r=client.patch(f"/api/incidents/{i['id']}?source=form",json=p)
    assert r.status_code==200 and r.json()["state"]=="2"

def test_reverse_condition():
    i=make(impact="1",urgency="1",assigned_to="Alex",assignment_group="Hardware")
    p=clean(i); p.update(impact="2",urgency="2",assigned_to="",assignment_group="")
    r=client.patch(f"/api/incidents/{i['id']}?source=form",json=p)
    assert r.status_code==200 and r.json()["impact"]=="2"

def test_ai():
    i=make(); r=client.post("/api/ai/explain",json={"incident_id":i["id"]})
    assert r.status_code==200 and "explanation" in r.json()
