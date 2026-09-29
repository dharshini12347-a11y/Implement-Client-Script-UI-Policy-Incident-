def high_impact(incident: dict) -> bool:
    return str(incident.get("impact", "")) == "1"

def apply_client_change(incident: dict, field: str, new_value: str):
    updated = dict(incident)
    messages = []
    updated[field] = new_value
    if field == "impact" and new_value == "1":
        updated["urgency"] = "1"
        messages.append("Urgency set to High for High impact incident.")
    return updated, messages

def ui_state(incident: dict):
    high = high_impact(incident)
    return {
        "assignment_group_mandatory": high,
        "urgency_read_only": high,
        "reverse_if_false": True,
        "high_impact": high,
    }

def validate_on_submit(incident: dict):
    if high_impact(incident) and not incident.get("assigned_to", "").strip():
        return False, "Assigned To is mandatory for High impact incidents."
    return True, None

def validate_list_edit(field: str):
    if field == "state":
        return False, "State cannot be updated using list editing. Please open the Incident."
    return True, None
