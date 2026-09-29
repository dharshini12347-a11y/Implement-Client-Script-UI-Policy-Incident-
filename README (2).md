# Incident Client Script & UI Policy — Complete Project

This project is a complete local simulator of the uploaded ServiceNow Incident micro-project.

## Implemented source rules

### UI Policy — High Impact Control
- Table: Incident
- Active: true
- Condition: Impact is 1 - High
- Assignment group: mandatory
- Reverse if false: true
- Urgency: read-only when condition is true

### onChange Client Script
Impact=1 sets Urgency=1 and shows:
`Urgency set to High for High impact incident.`

### onSubmit Client Script
If Impact=1 and Assigned To is empty, save is blocked with:
`Assigned To is mandatory for High impact incidents.`

### onCellEdit Client Script
Direct State list editing is blocked with:
`State cannot be updated using list editing. Please open the Incident.`

## Optional AI
Gemini is an explanation layer only. The deterministic rules decide whether a save is allowed.

## VS Code — Windows

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env`. The application works without a Gemini key.

Run:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```

Test:

```powershell
pytest -q
```

## Test scenarios

1. Create Incident.
2. Set Impact to High.
3. Confirm Urgency automatically becomes High.
4. Confirm Urgency becomes read-only.
5. Leave Assigned To empty.
6. Submit and confirm save is blocked.
7. Fill Assigned To and submit; save succeeds.
8. Change High to Medium; Assignment Group becomes optional and Urgency editable.
9. From Incident list, attempt State list editing; it is blocked.
10. Open the Incident form and change State; form-based update succeeds.

## ServiceNow files

The `servicenow/` folder contains:
- UI Policy configuration
- Exact Client Script code from the source
- Setup/testing checklist

The local application is a simulator; actual UI Policy and Client Script records must be created inside a ServiceNow instance.
