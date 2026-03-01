"""
NyayBase - FastAPI Backend Server (Local RAG-based)
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from analysis_engine import analyze_case
from knowledge_base import CASE_TYPES, JURISDICTIONS
from courts_data import search_courts
from legal_news import fetch_legal_news
import threading
import time
import os
import requests as http_requests


def _build_index_background():
    """Build RAG index in a background thread to avoid blocking startup."""
    try:
        import rag_engine
        rag_engine.build_index()
    except Exception as e:
        print(f"[NyayBase] RAG index build error: {e}")


def _keep_alive():
    """Self-ping to keep the service alive (safety net)."""
    time.sleep(60)
    # Check for Railway or Render URL
    railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if railway_domain:
        health_url = f"https://{railway_domain}/api/health"
    elif render_url:
        health_url = f"{render_url}/api/health"
    else:
        print("[NyayBase] No public URL detected, skipping keep-alive self-ping")
        return
    print(f"[NyayBase] Keep-alive started, pinging {health_url} every 13 min")
    while True:
        try:
            resp = http_requests.get(health_url, timeout=10)
            print(f"[NyayBase] Keep-alive ping: {resp.status_code}")
        except Exception as e:
            print(f"[NyayBase] Keep-alive ping failed: {e}")
        time.sleep(13 * 60)


@asynccontextmanager
async def lifespan(app):
    # Startup: build RAG index in background thread
    print("[NyayBase] Starting RAG index build in background...")
    t = threading.Thread(target=_build_index_background, daemon=True)
    t.start()
    # Start keep-alive self-ping for Render
    ka = threading.Thread(target=_keep_alive, daemon=True)
    ka.start()
    yield
    # Shutdown: nothing to clean up

app = FastAPI(title="NyayBase API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaseInput(BaseModel):
    case_type: str
    facts: str
    jurisdiction: str
    sections: Optional[str] = ""
    custom_case_type: Optional[str] = ""
    adverse_party: Optional[str] = ""
    legal_representation: Optional[str] = ""

class ChatInput(BaseModel):
    message: str
    history: Optional[list] = []

@app.get("/")
def root():
    return {"service": "NyayBase API", "version": "2.0.0", "status": "running"}

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NyayBase API", "version": "2.0.0"}

@app.get("/api/case-types")
def get_case_types():
    types = []
    for key, val in CASE_TYPES.items():
        types.append({
            "id": key,
            "name": val["name"],
            "description": val["description"],
            "relevant_acts": val["relevant_acts"],
            "avg_win_rate": round(val["avg_win_rate"] * 100, 1),
            "avg_duration_months": val["avg_duration_months"]
        })
    return {"case_types": types}

@app.get("/api/jurisdictions")
def get_jurisdictions():
    jurisdictions = [
        {"id": key, "name": val["name"]}
        for key, val in JURISDICTIONS.items()
    ]
    return {"jurisdictions": jurisdictions}

@app.get("/api/courts/search")
def courts_search(q: str = ""):
    """Search courts by city name or pincode."""
    if not q.strip():
        return {"courts": [], "query": q}
    data = search_courts(q)
    return {"query": q, "count": len(data["courts"]), **data}

@app.get("/api/legal-news")
def get_legal_news():
    """Get latest Indian legal news from RSS feeds."""
    try:
        data = fetch_legal_news()
        return {"success": True, "count": len(data["articles"]), **data}
    except Exception as e:
        return {"success": False, "articles": [], "error": str(e)}

@app.post("/api/analyze")
def analyze(case_input: CaseInput):
    try:
        ct = case_input.case_type
        if ct == "custom" and case_input.custom_case_type:
            ct = "custom"
        result = analyze_case(
            case_type=ct,
            facts=case_input.facts,
            jurisdiction=case_input.jurisdiction,
            sections=case_input.sections or "",
            custom_case_type=case_input.custom_case_type or "",
            adverse_party=case_input.adverse_party or "",
            legal_representation=case_input.legal_representation or ""
        )
        if result.get("is_api_error"):
            return {"success": False, "error": result.get("error", "AI engine temporarily unavailable. Please try again.")}
        if "error" in result and not result.get("is_invalid_input"):
            return {"success": False, "error": result["error"]}
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/stats")
def get_stats():
    from analysis_engine import LEGAL_DB
    court_stats = LEGAL_DB.get("court_stats", [])
    case_profiles = LEGAL_DB.get("case_profiles", [])

    total_pending = sum(c.get("pending_total", 0) for c in court_stats)
    total_judges = sum(c.get("judges_working", 0) for c in court_stats)
    total_sanctioned = sum(c.get("judges_sanctioned", 0) for c in court_stats)
    total_disposal = sum(c.get("annual_disposal", 0) for c in court_stats)
    total_institution = sum(c.get("annual_institution", 0) for c in court_stats)

    return {
        "highlights": {
            "total_pending": total_pending,
            "total_pending_formatted": f"{total_pending:,}",
            "total_judges_working": total_judges,
            "total_judges_sanctioned": total_sanctioned,
            "judge_vacancy": total_sanctioned - total_judges,
            "annual_cases_filed": total_institution,
            "annual_cases_disposed": total_disposal,
            "dataset_items": sum(len(v) if isinstance(v, list) else 0 for v in LEGAL_DB.values()),
            "courts_covered": len(court_stats),
            "case_types_supported": len(CASE_TYPES),
        },
        "court_stats": [
            {
                "name": c.get("name", ""),
                "state": c.get("state", ""),
                "city": c.get("city", ""),
                "judges_working": c.get("judges_working", 0),
                "judges_sanctioned": c.get("judges_sanctioned", 0),
                "pending_total": c.get("pending_total", 0),
                "pending_civil": c.get("pending_civil", 0),
                "pending_criminal": c.get("pending_criminal", 0),
                "disposal_rate": round(c.get("disposal_rate", 0) * 100, 1),
                "avg_disposal_months": c.get("avg_disposal_months", 0),
                "annual_institution": c.get("annual_institution", 0),
                "annual_disposal": c.get("annual_disposal", 0),
            }
            for c in court_stats
        ],
        "case_profiles": [
            {
                "id": p.get("id", ""),
                "name": p.get("name", ""),
                "pending_nationally": p.get("pending_nationally", 0),
                "avg_duration_months": p.get("avg_duration_months", 0),
                "win_rate": round(p.get("win_rate", 0) * 100, 1),
                "settlement_rate": round(p.get("settlement_rate", 0) * 100, 1),
                "appeal_rate": round(p.get("appeal_rate", 0) * 100, 1),
                "limitation_years": p.get("limitation_years", 0),
            }
            for p in case_profiles
        ],
        "case_type_stats": [
            {
                "name": v["name"],
                "avg_win_rate": round(v["avg_win_rate"] * 100, 1),
                "avg_duration_months": v["avg_duration_months"],
                "landmark_cases_count": len(v["landmark_cases"]),
            }
            for k, v in CASE_TYPES.items()
        ],
    }

@app.post("/api/chat")
def chat_endpoint(chat_input: ChatInput):
    try:
        from chatbot import chat
        reply = chat(
            message=chat_input.message,
            history=chat_input.history or []
        )
        return {"success": True, "reply": reply}
    except Exception as e:
        return {"success": False, "reply": f"I'm having trouble connecting to the AI engine. Please try again. ({str(e)})"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
