from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.llm import run_llm
from app.transform import prfaq_to_safefeatures

app = FastAPI(title="PRFAQ Agent")

class Idea(BaseModel):
    text: str

class PRFAQ(BaseModel):
    prfaq: str

@app.post("/draft-prfaq")
def draft_prfaq(body: Idea):
    """Generate a first‑pass PRFAQ from a one‑line idea."""
    system_prompt = open("app/prompts/prfaq_system.md").read()
    draft = run_llm(system_prompt, body.text)
    return {"prfaq": draft}

@app.post("/generate-safefeatures")
def generate_safefeatures(body: PRFAQ):
    """Turn a completed PRFAQ into a SAFe epic and feature list."""
    try:
        return prfaq_to_safefeatures(body.prfaq)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
