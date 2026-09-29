from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    caller: str = Field(min_length=2, max_length=120)
    category: str = "Software"
    subcategory: str = ""
    short_description: str = Field(min_length=2, max_length=200)
    description: str = ""
    impact: str = "3"
    urgency: str = "3"
    assigned_to: str = ""
    assignment_group: str = ""
    state: str = "1"

class IncidentUpdate(IncidentCreate):
    pass

class AIExplainRequest(BaseModel):
    incident_id: int
    question: str = "Explain the current incident validation state."
