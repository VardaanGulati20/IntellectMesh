# from fastapi import FastAPI
# from pydantic import BaseModel
# from server.tools.dynamic_scraper_tool import scrape_web
# import requests
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain_groq import ChatGroq
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()


# llm = ChatGroq(
#     temperature=0,
#     model_name="llama3-70b-8192",
#     groq_api_key=os.getenv("GROQ_API_KEY")
# )

# class QuestionInput(BaseModel):
#     input: str

# CRITIC_URL = "http://localhost:8002/evaluate"

# @app.post("/invoke")
# def invoke_tool(input: QuestionInput):
#     question = input.input

#     # === PHASE 1: SCRAPING ===
#     scraped_content = scrape_web(question)
#     initial_answer = scraped_content

#     # === PHASE 2: INITIAL CRITIC EVALUATION ===
#     critic_payload_1 = {"question": question, "answer": initial_answer}
#     try:
#         r1 = requests.post(CRITIC_URL, json=critic_payload_1).json()
#         score_1 = r1.get("score", 0)
#         critic_feedback_1 = r1.get("feedback", "")
#     except Exception as e:
#         score_1 = 0
#         critic_feedback_1 = f"Critic 1 failed: {e}"

#     # === PHASE 3: LLM IMPROVEMENT (only if score < 7) ===
#     if score_1 < 9:
#         improvement_prompt = PromptTemplate.from_template(
#             "The following content was scraped from the web for the question:\n{question}\n\nScraped Answer:\n{answer}\n\nCritic Feedback:\n{feedback}\n\nUsing this feedback, write a clearer, more complete, and accurate educational answer:"
#         )
#         chain = LLMChain(llm=llm, prompt=improvement_prompt)
#         final_answer = chain.run({
#             "question": question,
#             "answer": initial_answer,
#             "feedback": critic_feedback_1
#         })
#     else:
#         final_answer = initial_answer

#     # === PHASE 4: FINAL CRITIC EVALUATION ===
#     critic_payload_2 = {"question": question, "answer": final_answer}
#     try:
#         r2 = requests.post(CRITIC_URL, json=critic_payload_2).json()
#         score_2 = r2.get("score", 0)
#         critic_feedback_2 = r2.get("feedback", "")
#     except Exception as e:
#         score_2 = 0
#         critic_feedback_2 = f"Critic 2 failed: {e}"

#     return {
#         "question": question,
#         "initial_answer": initial_answer,
#         "critic_feedback_1": critic_feedback_1,
#         "score_1": score_1,
#         "final_answer": final_answer,
#         "critic_feedback_2": critic_feedback_2,
#         "score_2": score_2
#     }
# from fastapi import FastAPI, Request
# import requests
# from dynamic_scraper_tool import scrape_web

# app = FastAPI()

# CRITIC_URL = "http://localhost:8002/evaluate"
# LLM_REFINER_URL = "http://localhost:8003/refine"

# @app.post("/invoke")
# async def invoke(request: Request):
#     data = await request.json()
#     question = data.get("input", "")
#     context = data.get("context", "")

#     # Step 1: Scrape content
#     initial_answer = scrape_web(question)

#     # Step 2: First critic evaluation
#     critic_payload_1 = {"input": question, "answer": initial_answer}
#     try:
#         r1 = requests.post(CRITIC_URL, json=critic_payload_1)
#         critic_result_1 = r1.json()
#         score_1 =(int) critic_result_1.get("score", 0)
#         critic_feedback_1 = critic_result_1.get("feedback", "")
#     except Exception as e:
#         score_1 = 0
#         critic_feedback_1 = f"Critic evaluation failed: {e}"

#     # Step 3: If low score, refine with LLM
#     if score_1 < 9:
#         try:
#             refine_payload = {
#                 "question": question,
#                 "answer": initial_answer,
#                 "feedback": critic_feedback_1
#             }
#             r2 = requests.post(LLM_REFINER_URL, json=refine_payload)
#             final_answer = r2.json().get("refined_answer", initial_answer)
#         except Exception as e:
#             final_answer = initial_answer
#     else:
#         final_answer = initial_answer

#     # Step 4: Final critic evaluation
#     critic_payload_2 = {"input": question, "answer": final_answer}
#     try:
#         r3 = requests.post(CRITIC_URL, json=critic_payload_2)
#         critic_result_2 = r3.json()
#         score_2 = critic_result_2.get("score", 0)
#         critic_feedback_2 = critic_result_2.get("feedback", "")
#     except Exception as e:
#         score_2 = 0
#         critic_feedback_2 = f"Final critic evaluation failed: {e}"

#     return {
#         "question": question,
#         "initial_answer": initial_answer,
#         "critic_feedback_1": critic_feedback_1,
#         "refined_answer": final_answer,
#         "critic_feedback_2": critic_feedback_2,
#         "final_score": score_2
#     }
# from fastapi import FastAPI
# from pydantic import BaseModel
# from dynamic_scraper_tool import scrape_web
# import requests

# app = FastAPI()

# CRITIC_URL = "http://localhost:8002/evaluate"
# LLM_REFINER_URL = "http://localhost:8003/refine"

# class QuestionInput(BaseModel):
#     input: str

# @app.post("/invoke")
# def invoke_tool(input: QuestionInput):
#     question = input.input

#     # === PHASE 1: SCRAPING ===
#     scraped_content = scrape_web(question)
#     initial_answer = scraped_content

#     # === PHASE 2: INITIAL CRITIC EVALUATION ===
#     critic_payload_1 = {"question": question, "answer": initial_answer}
#     try:
#         r1 = requests.post(CRITIC_URL, json=critic_payload_1).json()
#         try:
#             score_1 = int(r1.get("score", 0))
#         except (ValueError, TypeError):
#             score_1 = 0
#         critic_feedback_1 = r1.get("feedback", "")
#     except Exception as e:
#         score_1 = 0
#         critic_feedback_1 = f"Critic 1 failed: {e}"

#     # === PHASE 3: LLM IMPROVEMENT (from external tool if score < 9) ===
#     if score_1 < 9:
#         try:
#             refine_payload = {
#                 "question": question,
#                 "answer": initial_answer,
#                 "feedback": critic_feedback_1
#             }
#             r2 = requests.post(LLM_REFINER_URL, json=refine_payload).json()
#             final_answer = r2.get("refined_answer", initial_answer)
#         except Exception as e:
#             final_answer = initial_answer
#     else:
#         final_answer = initial_answer

#     # === PHASE 4: FINAL CRITIC EVALUATION ===
#     critic_payload_2 = {"question": question, "answer": final_answer}
#     try:
#         r3 = requests.post(CRITIC_URL, json=critic_payload_2).json()
#         try:
#             score_2 = int(r3.get("score", 0))
#         except (ValueError, TypeError):
#             score_2 = 0
#         critic_feedback_2 = r3.get("feedback", "")
#     except Exception as e:
#         score_2 = 0
#         critic_feedback_2 = f"Critic 2 failed: {e}"

#     return {
#         "question": question,
#         "initial_answer": initial_answer,
#         "critic_feedback_1": critic_feedback_1,
#         "score_1": score_1,
#         "final_answer": final_answer,

#         "critic_feedback_2": critic_feedback_2,
#         "score_2": score_2
#     }

# orchestrator_agent.py
# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# import json
# import re

# app = FastAPI()

# # -------------------------
# # Tool Registry
# # -------------------------
# TOOL_REGISTRY = {
#     "scraper": "http://localhost:8001/a2a",
#     "critic": "http://localhost:8002/a2a",
#     "refiner": "http://localhost:8003/a2a"
# }

# # -------------------------
# # A2A Input Format
# # -------------------------
# class A2ARequest(BaseModel):
#     input: str
#     context: dict = {}

# # -------------------------
# # Helper: safe JSON parsing
# # -------------------------
# def safe_json_loads(s, fallback={}):
#     try:
#         clean = re.sub(r'[\x00-\x1f]+', '', s)  # remove control characters
#         return json.loads(clean)
#     except json.JSONDecodeError:
#         print("⚠️ JSON decode failed. Raw input:\n", s)
#         return fallback

# # -------------------------
# # A2A Orchestration Logic
# # -------------------------
# @app.post("/a2a")
# def orchestrate(req: A2ARequest):
#     question = req.input
#     context = req.context

#     print("\n🧠 Orchestrator received input:", question)

#     # -------------------------
#     # Step 1: Scraper
#     # -------------------------
#     try:
#         scraper_resp = requests.post(TOOL_REGISTRY["scraper"], json={
#             "input": question,
#             "context": {}
#         }).json()
#         scraped = scraper_resp.get("answer", "")
#         context["scraped_answer"] = scraped
#         print("🔍 Scraper complete")
#     except Exception as e:
#         return {"error": f"Scraper failed: {str(e)}"}

#     # -------------------------
#     # Step 2: First Critic Review
#     # -------------------------
#     try:
#         critic_resp = requests.post(TOOL_REGISTRY["critic"], json={
#             "input": question,
#             "context": {"answer": scraped}
#         }).json()
#         critic_data = safe_json_loads(critic_resp.get("answer", "{}"))
#         context["critic_score"] = critic_data.get("score", 0)
#         context["critic_feedback"] = critic_data.get("feedback", "No feedback provided.")
#         print(f"🧪 First critic review — Score: {context['critic_score']}")
#     except Exception as e:
#         return {"error": f"First critic failed: {str(e)}"}

#     # -------------------------
#     # Step 3: If score < 7, refine
#     # -------------------------
#     if context["critic_score"] < 9:
#         print("♻️ Score too low, sending to Refiner...")

#         try:
#             refine_resp = requests.post(TOOL_REGISTRY["refiner"], json={
#                 "input": question,
#                 "context": {
#                     "answer": scraped,
#                     "feedback": context["critic_feedback"]
#                 }
#             }).json()
#             context["refined_answer"] = refine_resp.get("answer", "")
#         except Exception as e:
#             return {"error": f"Refiner failed: {str(e)}"}

#         # -------------------------
#         # Step 4: Second Critic Review
#         # -------------------------
#         try:
#             critic2 = requests.post(TOOL_REGISTRY["critic"], json={
#                 "input": question,
#                 "context": {"answer": context["refined_answer"]}
#             }).json()
#             final_critique = safe_json_loads(critic2.get("answer", "{}"))
#             context["final_score"] = final_critique.get("score", 0)
#             context["final_feedback"] = final_critique.get("feedback", "No final feedback.")
#             print(f"✅ Final critic review — Score: {context['final_score']}")
#         except Exception as e:
#             return {"error": f"Final critic failed: {str(e)}"}
#     else:
#         # No refinement needed
#         context["refined_answer"] = scraped
#         context["final_score"] = context["critic_score"]
#         context["final_feedback"] = context["critic_feedback"]
#         print("✅ No refinement needed — Score acceptable")

#     # -------------------------
#     # Final A2A Output
#     # -------------------------
#     return {
#         "question": question,
#         "final_answer": context["refined_answer"],
#         "score": context["final_score"],
#         "feedback": context["final_feedback"]
#     }

# # -------------------------
# # Health Check
# # -------------------------
# @app.get("/")
# def root():
#     return {"status": "Orchestrator is running and A2A ready"}
# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# import json
# import os

# # ----------------------------
# # ⚙️ FastAPI Setup
# # ----------------------------
# app = FastAPI()

# # ----------------------------
# # 📦 Load Agent Registry
# # ----------------------------
# AGENT_REGISTRY_PATH = "agent_registry.json"

# def load_registry():
#     with open(AGENT_REGISTRY_PATH, "r") as f:
#         return json.load(f)

# def get_agent_url_by_tag(tag):
#     agents = load_registry()
#     for agent in agents:
#         if tag in agent["tags"]:
#             return agent["url"]
#     return None

# # ----------------------------
# # 📨 Client Request Model
# # ----------------------------
# class QuestionRequest(BaseModel):
#     question: str

# # ----------------------------
# # 📡 Main Endpoint
# # ----------------------------
# @app.post("/ask")
# def ask_student_question(payload: QuestionRequest):
#     question = payload.question
#     scraper_url = get_agent_url_by_tag("scraper")

#     if not scraper_url:
#         return {"error": "Scraper agent not found in registry."}

#     try:
#         response = requests.post(
#             f"{scraper_url}/a2a",
#             json={"input": question, "context": {}},
#             timeout=60
#         )
#         result = response.json()
#         return {
#             "final_answer": result.get("answer", "[No answer returned]"),
#             "pipeline": "scraper → critic → (maybe refiner) → critic → final"
#         }

#     except Exception as e:
#         return {"error": f"Failed to get answer from scraper: {e}"}

# # ----------------------------
# # ✅ Health Check
# # ----------------------------
# @app.get("/")
# def health_check():
#     return {"status": "MCP orchestrator is running"}

# mcp_server.py

# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# import json

# app = FastAPI()

# # Load agent registry
# def load_registry():
#     with open("agent_registry.json") as f:
#         return json.load(f)

# def get_agent_url_by_tag(tag):
#     agents = load_registry()
#     for agent in agents:
#         if tag in agent["tags"]:
#             return agent["url"]
#     return None

# class QuestionRequest(BaseModel):
#     question: str

# @app.post("/ask")
# def ask_handler(req: QuestionRequest):
#     scraper_url = get_agent_url_by_tag("scraper")
#     if not scraper_url:
#         return {"error": "Scraper not found in registry."}

#     try:
#         response = requests.post(
#             url=f"{scraper_url}/a2a",
#             json={"input": req.question, "context": {}, "pipeline_trace": []},
#             timeout=300
#         )
#         return response.json()
#     except Exception as e:
#         return {"error": f"Failed to contact scraper: {e}"}

# @app.get("/")
# def health():
#     return {"status": "MCP Server is running"}
# 📁 File: mcp_server.py (Updated for A2A Compliance)
# 

# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# import json
# import os

# app = FastAPI()

# # ----------------------------
# # 🔑 Config
# # ----------------------------
# REGISTRY_URL = os.getenv("REGISTRY_URL", "http://localhost:9000")
# SERVER_ID = "a2a-orchestrator"
# SERVER_PORT = "8000"  # default port for this service

# # ----------------------------
# # 📡 A2A Request Schema
# # ----------------------------
# class QuestionRequest(BaseModel):
#     question: str
#     intent: str = "improve_answer"

# # ----------------------------
# # 🔍 Resolve Agent by Tag
# # ----------------------------
# def resolve_agent(tag: str):
#     try:
#         res = requests.get(f"{REGISTRY_URL}/resolve", params={"tag": tag}, timeout=5)
#         return res.json().get("endpoints", {}).get("a2a")
#     except Exception as e:
#         print(f"❌ Failed to resolve agent for {tag}: {e}")
#         return None

# # ----------------------------
# # 🎯 Entry Point
# # ----------------------------
# @app.post("/ask")
# def ask_handler(req: QuestionRequest):
#     question = req.question
#     intent = req.intent

#     scraper_url = resolve_agent("scraper")
#     if not scraper_url:
#         return {"error": "No scraper found in registry."}

#     print(f"📡 Forwarding question to: {scraper_url}")

#     try:
#         response = requests.post(
#             url=scraper_url,
#             json={
#                 "input": question,
#                 "context": {},
#                 "pipeline_trace": [],
#                 "intent": intent
#             },
#             timeout=300
#         )
#         return response.json()
#     except Exception as e:
#         print(f"❌ Error forwarding to scraper: {e}")
#         return {"error": f"Failed to contact scraper: {e}"}

# # ----------------------------
# # 🔁 Register with MCP Registry
# # ----------------------------
# AGENT_CARD = {
#     "id": SERVER_ID,
#     "name": "MCP Orchestrator",
#     "version": "1.0.0",
#     "description": "Entry point that sends user questions to the A2A pipeline",
#     "tags": ["entry", "mcp"],
#     "endpoints": {"ask": f"http://localhost:{SERVER_PORT}/ask"},
#     "auth": {"type": "none"}
# }

# @app.on_event("startup")
# def register():
#     try:
#         res = requests.post(f"{REGISTRY_URL}/register", json=AGENT_CARD)
#         print("✅ Orchestrator registered with registry:", res.json())
#     except Exception as e:
#         print("❌ Failed to register orchestrator:", e)

# # ----------------------------
# # ✅ Health Check
# # ----------------------------
# @app.get("/")
# def health():
#     return {"status": "MCP A2A Server is running"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ Add CORS
from pydantic import BaseModel
import requests
import json
import os

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# 🔑 Config
# ----------------------------
REGISTRY_URL = os.getenv("REGISTRY_URL", "http://localhost:9000")
SERVER_ID = "a2a-orchestrator"
SERVER_PORT = "8000"  # default port for this service

# ----------------------------
# 📡 A2A Request Schema
# ----------------------------
class QuestionRequest(BaseModel):
    question: str
    intent: str = "improve_answer"

# ----------------------------
# 🔍 Resolve Agent by Tag
# ----------------------------
def resolve_agent(tag: str):
    try:
        res = requests.get(f"{REGISTRY_URL}/resolve", params={"tag": tag}, timeout=5)
        return res.json().get("endpoints", {}).get("a2a")
    except Exception as e:
        print(f"❌ Failed to resolve agent for {tag}: {e}")
        return None

# ----------------------------
# 🎯 Entry Point
# ----------------------------
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

# ----------------------------
# 🔁 Register with MCP Registry
# ----------------------------
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

# ----------------------------
# ✅ Health Check
# ----------------------------
@app.get("/")
def health():
    return {"status": "MCP A2A Server is running"}
