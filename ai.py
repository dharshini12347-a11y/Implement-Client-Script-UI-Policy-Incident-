import json, httpx
from .config import get_settings
from .rules import ui_state, validate_on_submit

def local_explanation(incident, question):
    state = ui_state(incident)
    ok, error = validate_on_submit(incident)
    text = [f"Incident {incident['number']} has Impact={incident['impact']} and Urgency={incident['urgency']}."]
    if state["high_impact"]:
        text.append("High Impact Control is active: Assignment Group is mandatory and Urgency is read-only.")
    else:
        text.append("High Impact Control is inactive, so its conditional restrictions are reversed.")
    text.append(f"Save validation: {'allowed' if ok else 'blocked — ' + error}.")
    text.append("Direct State changes from list editing are blocked, while form-based State changes are allowed.")
    return " ".join(text)

async def explain_with_gemini(incident, question):
    settings = get_settings()
    fallback = local_explanation(incident, question)
    if not settings.gemini_api_key:
        return fallback, "local-fallback"
    prompt = f"""
Explain this Incident validation demo using only the supplied data and rules.
Question: {question}
Incident: {json.dumps(incident, indent=2)}
Rules: Impact=1 activates High Impact Control; Assignment Group mandatory; Urgency read-only;
onChange Impact=1 sets Urgency=1; onSubmit blocks empty Assigned To; onCellEdit blocks direct State list edits.
Do not approve records or invent permissions. Keep the explanation concise.
"""
    url = f"{settings.gemini_api_base}/{settings.gemini_model}:generateContent"
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, params={"key":settings.gemini_api_key},
                                  json={"contents":[{"parts":[{"text":prompt}]}]})
            r.raise_for_status()
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip(), "gemini"
    except Exception:
        return fallback, "local-fallback"
