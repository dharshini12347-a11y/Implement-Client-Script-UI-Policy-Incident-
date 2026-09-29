# ServiceNow Configuration Checklist

## UI Policy
1. Log in with administrative/configuration access.
2. System UI → UI Policies → New.
3. Name: High Impact Control.
4. Table: Incident.
5. Active: true.
6. Condition: Impact is 1 - High.
7. Create UI Policy Action for Assignment group: Mandatory.
8. Set Reverse if false to true.
9. Create UI Policy Action for Urgency: Read-only.
10. Leave Visible unchanged.
11. Submit.

## Client Scripts
Create these three Incident scripts:
- Auto set urgency for high impact — onChange — Impact.
- Prevent save if Assigned To missing — onSubmit.
- Prevent state change via list edit — onCellEdit — State.

Use the exact code in `02_client_scripts.md`.

## Testing
1. Incident → Create New.
2. Impact = High.
3. Urgency becomes High.
4. Urgency is read-only.
5. Leave Assigned To empty and Submit.
6. Save is blocked.
7. Fill Assigned To and Submit; save succeeds.
8. Change High to Medium; Assignment Group is no longer mandatory and Urgency becomes editable.
9. Incident → All; attempt direct State list editing; it is blocked.
10. Open the Incident form and change State; form-based update is allowed.
