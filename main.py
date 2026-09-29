from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .db import init_db
from .schemas import IncidentCreate, IncidentUpdate, AIExplainRequest
from .workflow import create_incident, get_incident, list_incidents, update_incident, change_impact
from .rules import ui_state
from .ai import explain_with_gemini

settings=get_settings()
BASE=Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app=FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=BASE/"static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE/"templates"/"index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status":"ok","service":settings.app_name}

@app.get("/api/incidents")
def incidents():
    return list_incidents()

@app.post("/api/incidents")
def create(payload: IncidentCreate):
    try: return create_incident(payload.model_dump())
    except Exception as e: raise HTTPException(400, str(e))

@app.get("/api/incidents/{incident_id}")
def detail(incident_id:int):
    item=get_incident(incident_id)
    if not item: raise HTTPException(404,"Incident not found")
    item["ui_state"]=ui_state(item)
    return item

@app.patch("/api/incidents/{incident_id}")
def update(incident_id:int,payload:IncidentUpdate,source:str="form"):
    try: return update_incident(incident_id,payload.model_dump(),source)
    except ValueError as e: raise HTTPException(404,str(e))
    except PermissionError as e: raise HTTPException(422,str(e))

@app.post("/api/incidents/{incident_id}/impact")
def impact(incident_id:int, impact:str):
    try:
        updated,messages,ok,error=change_impact(incident_id,impact)
        return {"incident":updated,"messages":messages,"can_save":ok,"error":error,"ui_state":ui_state(updated)}
    except ValueError as e: raise HTTPException(404,str(e))

@app.post("/api/incidents/{incident_id}/list-state-edit")
def list_state_edit(incident_id:int,state:str):
    item=get_incident(incident_id)
    if not item: raise HTTPException(404,"Incident not found")
    if state != item["state"]:
        raise HTTPException(422,"State cannot be updated using list editing. Please open the Incident.")
    return item

@app.post("/api/ai/explain")
async def ai(payload:AIExplainRequest):
    item=get_incident(payload.incident_id)
    if not item: raise HTTPException(404,"Incident not found")
    text,provider=await explain_with_gemini(item,payload.question)
    return {"provider":provider,"explanation":text}
