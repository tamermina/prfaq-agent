from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.llm import run_llm
from app.transform import prfaq_to_safefeatures

app = FastAPI(title="PRFAQ Agent")

class Notes(BaseModel):
    """Free‑form notes, requirements, user stories, etc."""
    text: str

class PRFAQ(BaseModel):
    prfaq: str

@app.post("/draft-prfaq")
def draft_prfaq(body: Notes):
    """
    Convert raw notes into a standardized PRFAQ.
    """
    system_prompt = open("app/prompts/prfaq_system.md").read()
    draft = run_llm(system_prompt, body.text)
    return {"prfaq": draft}

@app.post("/generate-safefeatures")
def generate_safefeatures(body: PRFAQ):
    """
    Turn the finished PRFAQ into a SAFe Epic and Feature list.
    """
    try:
        return prfaq_to_safefeatures(body.prfaq)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
