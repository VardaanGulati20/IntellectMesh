
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
import requests
import json
import os

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

REGISTRY_URL = os.getenv("REGISTRY_URL", "http://localhost:9000")
SERVER_ID = "a2a-orchestrator"
SERVER_PORT = "8000"  

class QuestionRequest(BaseModel):
    question: str
    intent: str = "improve_answer"

def resolve_agent(tag: str):
    try:
        res = requests.get(f"{REGISTRY_URL}/resolve", params={"tag": tag}, timeout=5)
        return res.json().get("endpoints", {}).get("a2a")
    except Exception as e:
        print(f"❌ Failed to resolve agent for {tag}: {e}")
        return None

@app.post("/ask")
def ask_handler(req: QuestionRequest):
    question = req.question
    intent = req.intent

    scraper_url = resolve_agent("scraper")
    if not scraper_url:
        return {"error": "No scraper found in registry."}

    print(f"📡 Forwarding question to: {scraper_url}")

    try:
        response = requests.post(
            url=scraper_url,
            json={
                "input": question,
                "context": {},
                "pipeline_trace": [],
                "intent": intent
            },
            timeout=300
        )
        return response.json()
    except Exception as e:
        print(f"❌ Error forwarding to scraper: {e}")
        return {"error": f"Failed to contact scraper: {e}"}


AGENT_CARD = {
    "id": SERVER_ID,
    "name": "MCP Orchestrator",
    "version": "1.0.0",
    "description": "Entry point that sends user questions to the A2A pipeline",
    "tags": ["entry", "mcp"],
    "endpoints": {"ask": f"http://localhost:{SERVER_PORT}/ask"},
    "auth": {"type": "none"}
}

@app.on_event("startup")
def register():
    try:
        res = requests.post(f"{REGISTRY_URL}/register", json=AGENT_CARD)
        print("✅ Orchestrator registered with registry:", res.json())
    except Exception as e:
        print("❌ Failed to register orchestrator:", e)

@app.get("/")
def health():
    return {"status": "MCP A2A Server is running"}

