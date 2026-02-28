"""
NyayBase — Smart Response Generator (Real-time LLM)
Constructs structured legal analysis by combining RAG-retrieved documents 
with real-time reasoning from LLM cascade (Gemini → Groq → Ollama).
"""

import json
import urllib.request
import re
from knowledge_base import CASE_TYPES, JURISDICTIONS
from llm_providers import call_llm


def generate_analysis(case_type: str, facts: str, jurisdiction: str,
                      sections: str = "", custom_case_type: str = "",
                      rag_results: dict = None, adverse_party: str = "",
                      legal_representation: str = "") -> dict:
    """
    Generate a complete legal analysis using RAG + Local Ollama LLM.
    """
    ct = case_type if case_type in CASE_TYPES else "custom"
    case_data = CASE_TYPES[ct]
    jur_data = JURISDICTIONS.get(jurisdiction, JURISDICTIONS["Other"])
    display_name = custom_case_type if (ct == "custom" and custom_case_type) else case_data["name"]

    # 1. Format RAG Context (Statutes & Landmark Cases)
    rag_statutes = (rag_results or {}).get("statutes", [])[:5]  # 5 statutes for more arguments
    rag_cases = (rag_results or {}).get("cases", [])[:5]  # 5 cases for more coverage
    
    context_str = "STATUTES:\n"
    for s in rag_statutes:
        data = s["data"]
        context_str += f"- {data.get('act', '')} S.{data.get('section', '')}: {data.get('title', '')}\n"
        
    context_str += "\nCASES:\n"
    for c in rag_cases:
        data = c["data"]
        context_str += f"- {data.get('name', '')} ({data.get('year', '')}): {data.get('held', '')[:120]}\n"

    # 2. Add Baseline Statistics
    sf = jur_data.get("speed_factor", 1.0)
    baseline_win_rate = case_data.get("avg_win_rate", 0.5) * 100
    est_months = int(case_data.get("avg_duration_months", 24) * sf)

    # ── Adverse Party Analysis ──
    adverse_context = ""
    adverse_adjustment = 0  # Win probability adjustment
    adverse_type = "unknown"
    adverse_risk = None

    if adverse_party and adverse_party.strip():
        ap = adverse_party.lower().strip()
        govt_keywords = ["government", "govt", "state", "ministry", "municipal", "corporation", "authority", "police", "army", "public sector", "psu", "sarkari", "nagar nigam", "collector", "commissioner"]
        corp_keywords = ["company", "corporate", "ltd", "limited", "pvt", "private limited", "llp", "firm", "multinational", "mnc", "conglomerate", "group of companies", "bank", "insurance", "builder", "developer", "hospital chain"]
        criminal_keywords = ["gang", "mafia", "criminal", "goonda", "illegal", "syndicate", "cartel", "nexus", "organized crime", "land mafia", "extortion"]
        influential_keywords = ["politician", "neta", "mla", "mp", "minister", "powerful", "influential", "connected", "wealthy", "rich businessman", "well-connected"]

        if any(kw in ap for kw in govt_keywords):
            adverse_type = "government"
            adverse_adjustment = -5
            adverse_context = f"\nADVERSE PARTY: Government/State entity — {adverse_party}."
            adverse_risk = {
                "risk": "Government as Opposing Party",
                "severity": "High",
                "description": "Your case is against a government entity with dedicated legal teams and procedural advantages.",
                "mitigation": "Ensure all evidence is documented. Consider filing under Article 226/32 for writ jurisdiction."
            }
        elif any(kw in ap for kw in criminal_keywords):
            adverse_type = "criminal_group"
            adverse_adjustment = -6
            adverse_context = f"\nADVERSE PARTY: Criminal/organized group — {adverse_party}."
            adverse_risk = {
                "risk": "Criminal/Organized Opposition",
                "severity": "High",
                "description": "Your case involves an adverse party with alleged criminal connections, posing witness intimidation and safety risks.",
                "mitigation": "Seek witness protection if needed. File applications for expedited hearing and keep digital copies of all evidence."
            }
        elif any(kw in ap for kw in influential_keywords):
            adverse_type = "influential"
            adverse_adjustment = -7
            adverse_context = f"\nADVERSE PARTY: Influential/powerful individual — {adverse_party}."
            adverse_risk = {
                "risk": "Influential Opposing Party",
                "severity": "High",
                "description": "Your opponent is influential and may retain top legal counsel with resources to prolong litigation.",
                "mitigation": "Build an airtight documentary case. Consider higher courts if local influence is a concern."
            }
        elif any(kw in ap for kw in corp_keywords):
            adverse_type = "corporation"
            adverse_adjustment = -3
            adverse_context = f"\nADVERSE PARTY: Corporation/company — {adverse_party}."
            adverse_risk = {
                "risk": "Corporate Opposition",
                "severity": "Medium",
                "description": "Your case is against a corporate entity with dedicated legal teams and resources.",
                "mitigation": "Focus on documentary evidence. Consumer forums often favor individuals against corporate negligence."
            }
        else:
            adverse_type = "individual"
            adverse_adjustment = 2
            adverse_context = f"\nADVERSE PARTY: Individual — {adverse_party}."
            adverse_risk = None

        print(f"[NyayBase] Adverse party: type={adverse_type}, adjustment={adverse_adjustment}")

    # ── Legal Representation Analysis ──
    rep_context = ""
    rep_adjustment = 0

    if legal_representation:
        rep_map = {
            "self": (-5, "Self-represented (no lawyer)"),
            "individual_lawyer": (0, "Represented by an individual/private lawyer"),
            "government_lawyer": (-2, "Represented by a government/legal aid lawyer"),
            "law_firm": (5, "Represented by a reputed law firm"),
            "organization": (4, "Backed by an organization/NGO/institution"),
        }
        rep_data = rep_map.get(legal_representation)
        if rep_data:
            rep_adjustment, rep_label = rep_data
            rep_context = f"\nYOUR REPRESENTATION: {rep_label}."
            print(f"[NyayBase] Legal representation: {legal_representation}, adjustment={rep_adjustment}")

    system_prompt = f"""You are NyayBase, an Indian legal advisor. Address the client directly as "you"/"your". Be professional.

Case: {display_name} | {jur_data['name']} | Base win rate: {baseline_win_rate}%
{context_str}{adverse_context}{rep_context}

Adjust win rate based on facts. Strong evidence=higher, weak evidence/admitted fault=lower.

Respond with ONLY valid JSON:
{{
    "win_probability": {{
        "probability": <int 0-100>,
        "strength": "<Strong|Moderate|Challenging|Difficult>",
        "reasoning": "<2-3 sentences to 'you' about why this probability, referencing case strengths/weaknesses>"
    }},
    "key_arguments": [
        {{"argument": "<legal argument>", "section": "<Act, Section>", "description": "<how it helps you>", "strength": <int 0-100>}}
    ],
    "risk_factors": [
        {{"risk": "<risk name>", "severity": "<High|Medium|Low>", "description": "<why risky for you>", "mitigation": "<what you can do>"}}
    ]
}}
Generate exactly 4-5 key_arguments and 3-4 risk_factors.
"""

    user_prompt = f"Case Facts provided by user:\n{facts}"

    # 3. Call LLM
    print("[NyayBase] Generating dynamic analysis via LLM cascade...")
    try:
        llm_response = call_llm(system_prompt, user_prompt)
    except Exception as e:
        print(f"[NyayBase] LLM failed: {e}. Falling back to default empty response.")
        llm_response = {}

    # ── Fallback: Build key_arguments from RAG statutes if LLM returned none ──
    if not llm_response.get("key_arguments"):
        fallback_args = []
        for s in rag_statutes[:5]:
            data = s["data"]
            act = data.get("act", "Relevant Act")
            sec = data.get("section", "")
            title = data.get("title", "Legal Provision")
            summary = data.get("summary", data.get("text", ""))[:200]
            fallback_args.append({
                "argument": title,
                "section": f"Section {sec}, {act}" if sec else act,
                "description": summary if summary else f"This provision under {act} is directly relevant to your case and strengthens your legal position.",
                "strength": max(40, min(85, 70 + len(fallback_args) * -5))
            })
        # Pad to at least 3 if we have fewer statutes
        while len(fallback_args) < 3:
            fallback_args.append({
                "argument": f"General Legal Standing under {display_name}",
                "section": ", ".join(case_data.get("relevant_acts", [])[:2]) or "Applicable Law",
                "description": f"Based on the facts of your case, you have a viable legal claim under the applicable statutes for {display_name}.",
                "strength": 55
            })
        llm_response["key_arguments"] = fallback_args[:5]

    # ── Always build similar_cases from RAG (more reliable than LLM) ──
    import urllib.parse
    rag_similar_cases = []
    for c in rag_cases:
        data = c["data"]
        case_name = data.get("name", "Landmark Case")
        citation = data.get("citation", "")
        year = data.get("year", "")
        court = data.get("court", "")
        held = data.get("held", data.get("summary", "Judgment pronounced"))[:200]
        principles = data.get("principles", [])
        # Construct Indian Kanoon search URL from case name
        search_query = urllib.parse.quote_plus(case_name)
        source_url = f"https://indiankanoon.org/search/?formInput={search_query}"
        rag_similar_cases.append({
            "case_name": case_name,
            "citation": citation,
            "year": year,
            "court": court,
            "outcome": held,
            "relevance_score": max(40, min(95, int(c.get("score", 0.6) * 100))),
            "summary": f"This case is relevant to your situation as it established: {'; '.join(principles[:2])}" if principles else f"This landmark case is relevant to your {display_name} case.",
            "source_url": source_url
        })
    # Use RAG cases (always more reliable), override any LLM-generated ones
    if rag_similar_cases:
        llm_response["similar_cases"] = rag_similar_cases

    # ── Fallback: Build risk_factors if LLM returned none ──
    if not llm_response.get("risk_factors"):
        llm_response["risk_factors"] = [
            {
                "risk": "Evidence Documentation",
                "severity": "Medium",
                "description": "Ensure all your documentary evidence is properly organized and authenticated. Courts rely heavily on documentary proof.",
                "mitigation": "Gather and notarize all relevant documents, obtain certified copies, and maintain a chronological evidence file."
            },
            {
                "risk": "Limitation Period",
                "severity": "High",
                "description": "Verify that your case is filed within the prescribed limitation period. Filing after the limitation expires can result in dismissal.",
                "mitigation": "Consult with a lawyer to confirm the applicable limitation period and file the case promptly."
            },
            {
                "risk": "Opposition Strategy",
                "severity": "Medium",
                "description": "The opposing party may challenge your claims with counter-evidence or procedural objections.",
                "mitigation": "Prepare for all possible defenses and counter-arguments. Consider engaging an experienced advocate."
            }
        ]


    # 4. Construct Final Response Payload (merging LLM dynamic vars with static metadata)
    win_prob = llm_response.get("win_probability", {})
    prob_val = win_prob.get("probability", int(baseline_win_rate))

    # Apply adverse party + legal representation adjustments
    total_adjustment = adverse_adjustment + rep_adjustment
    if total_adjustment != 0:
        prob_val = max(5, min(95, prob_val + total_adjustment))
    
    # Add adverse party risk factor if applicable
    risk_factors = llm_response.get("risk_factors", [])
    if adverse_risk:
        risk_factors.insert(0, adverse_risk)
    
    color = "#22c55e"
    if prob_val < 40: color = "#ef4444"
    elif prob_val < 60: color = "#f97316"
    elif prob_val < 75: color = "#f59e0b"

    fallback_reasoning = f"Based on the provided facts, the baseline chance is {int(baseline_win_rate)}%."
    
    timeline = {
        "estimated_months": est_months,
        "min_months": int(case_data.get("duration_range", [12, 36])[0] * sf),
        "max_months": int(case_data.get("duration_range", [12, 36])[1] * sf),
        "stages": [
            {
                "court": court,
                "avg_months": int(stats["avg_months"] * sf),
                "win_rate": round(stats["win_rate"] * 100, 1),
            }
            for court, stats in case_data.get("court_stats", {}).items()
        ],
        "recommendation": f"Estimated {est_months} months in {jur_data['name']}. Expect institutional delays if the opposition is a corporation or state entity."
    }
    
    med = case_data.get("mediation_factors", {})

    return {
        "case_type": display_name,
        "jurisdiction": jur_data["name"],
        "relevant_acts": case_data.get("relevant_acts", []),
        "win_probability": {
            "probability": prob_val,
            "lower_bound": max(5, prob_val - 12),
            "upper_bound": min(95, prob_val + 12),
            "confidence_margin": 12,
            "strength": win_prob.get("strength", "Unknown") if win_prob.get("strength") in ("Strong", "Moderate", "Challenging", "Difficult") else ("Strong" if prob_val >= 75 else "Moderate" if prob_val >= 50 else "Challenging" if prob_val >= 30 else "Difficult"),
            "strength_color": color,
            "base_rate": int(baseline_win_rate),
            "adjustment": prob_val - int(baseline_win_rate),
            "factors_detected": len(llm_response.get("key_arguments", [])),
            "reasoning": win_prob.get("reasoning", fallback_reasoning)
        },
        "key_arguments": llm_response.get("key_arguments", []),
        "similar_cases": llm_response.get("similar_cases", []),
        "timeline": timeline,
        "mediation": {
            "recommendation": "Recommended" if med.get("recommended") else "Worth Considering",
            "color": "#22c55e" if med.get("recommended") else "#f59e0b",
            "success_rate": round(med.get("success_rate", 0.4) * 100),
            "avg_settlement_months": med.get("avg_settlement_time_months", 4),
            "reasoning": med.get("reasoning", "Mediation is highly recommended to avoid the lengthy timelines of Indian courts.")
        },
        "risk_factors": risk_factors
    }
