"""
NyayBase — Analysis Engine (Local RAG-based)
Uses semantic search + smart response generation. No external API needed.
"""

import json, os, re
from knowledge_base import CASE_TYPES, JURISDICTIONS

# Load comprehensive legal dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "legal_dataset.json")
LEGAL_DB = {}
try:
    with open(DATASET_PATH, "r") as f:
        LEGAL_DB = json.load(f)
    print(f"[NyayBase] Loaded legal dataset: {sum(len(v) if isinstance(v,list) else 0 for v in LEGAL_DB.values())} items")
except Exception as e:
    print(f"[NyayBase] Warning: Could not load legal_dataset.json: {e}")


# ─── Gibberish / Invalid Input Detection ───
def is_gibberish(text):
    """Detect if input is gibberish, too short, or not a real legal scenario."""
    if not text or not text.strip():
        return True, "empty"
    clean = text.strip()
    if len(clean) < 15:
        return True, "too_short"
    alpha_chars = sum(1 for c in clean if c.isalpha())
    if alpha_chars < len(clean) * 0.4:
        return True, "random_chars"
    words = re.findall(r'[a-zA-Z]{3,}', clean)
    if len(words) < 3:
        return True, "no_real_words"
    if re.search(r'(.)\1{5,}', clean):
        return True, "repeated_chars"
    word_list = clean.lower().split()
    if len(word_list) > 3 and len(set(word_list)) <= 2:
        return True, "repeated_words"
    return False, "valid"


# ─── Semantic Input Quality Scoring ───
# Keywords that indicate real legal content
_LEGAL_KEYWORDS = {
    "dispute", "case", "complaint", "filed", "court", "judge", "lawyer", "advocate",
    "agreement", "contract", "property", "land", "rent", "tenant", "landlord",
    "cheque", "bounce", "loan", "debt", "payment", "money", "salary", "wages",
    "accident", "injury", "death", "hospital", "medical", "insurance",
    "divorce", "custody", "maintenance", "marriage", "husband", "wife", "domestic",
    "fir", "police", "arrest", "bail", "theft", "fraud", "assault", "murder",
    "termination", "employment", "fired", "resigned", "employer", "employee",
    "consumer", "defective", "product", "service", "refund", "warranty",
    "tax", "income", "gst", "assessment", "notice", "penalty",
    "copyright", "trademark", "patent", "infringement",
    "government", "authority", "municipal", "acquisition",
    "evidence", "witness", "document", "receipt", "proof", "certificate",
    "section", "act", "ipc", "crpc", "bns", "bnss", "cpc",
    "compensation", "damages", "injunction", "relief", "petition", "appeal",
    "violation", "rights", "fundamental", "constitutional",
}

_SPECIFICITY_KEYWORDS = {
    "date", "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "lakh", "crore", "rupee", "rs", "₹", "inr",
    "registered", "notarized", "stamped", "signed", "certified",
    "years", "months", "days", "since", "ago", "when",
}

_EVIDENCE_KEYWORDS = {
    "agreement", "contract", "receipt", "invoice", "fir", "witness", "cctv",
    "video", "recording", "notarized", "stamp paper", "affidavit",
    "bank statement", "photograph", "medical report", "forensic",
    "email", "whatsapp", "screenshot", "digital evidence", "certified copy",
    "sale deed", "title deed", "registration", "survey", "tax receipt",
    "appointment letter", "salary slip", "termination letter", "offer letter",
    "charge sheet", "postmortem", "disability certificate",
}


def compute_input_quality(text: str) -> dict:
    """
    Score input quality from 0-100 based on legal relevance and specificity.
    Returns: {"score": int, "label": str, "max_probability": int, "issues": list}
    """
    if not text or len(text.strip()) < 20:
        return {"score": 0, "label": "Insufficient", "max_probability": 10, "issues": ["Input too short"]}

    lower = text.lower()
    words = lower.split()
    word_count = len(words)
    score = 0
    issues = []

    # 1. Length score (max 20 pts) — more detail = better
    if word_count >= 80:
        score += 20
    elif word_count >= 50:
        score += 16
    elif word_count >= 30:
        score += 12
    elif word_count >= 15:
        score += 8
    else:
        score += 3
        issues.append("Very brief description — add more detail about what happened")

    # 2. Legal keyword hits (max 25 pts)
    legal_hits = sum(1 for kw in _LEGAL_KEYWORDS if kw in lower)
    if legal_hits >= 8:
        score += 25
    elif legal_hits >= 5:
        score += 20
    elif legal_hits >= 3:
        score += 14
    elif legal_hits >= 1:
        score += 7
    else:
        score += 0
        issues.append("No recognizable legal terms — describe your legal dispute clearly")

    # 3. Specificity — dates, amounts, names (max 20 pts)
    specificity_hits = sum(1 for kw in _SPECIFICITY_KEYWORDS if kw in lower)
    date_matches = len(re.findall(r'\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b', text))
    money_matches = len(re.findall(r'₹\s*[\d,]+|rs\.?\s*[\d,]+|lakh|crore|rupee', lower))
    specificity_score = min(20, specificity_hits * 3 + date_matches * 4 + money_matches * 4)
    score += specificity_score
    if specificity_score < 5:
        issues.append("Add specific dates, amounts, and names for better analysis")

    # 4. Evidence mentions (max 20 pts)
    evidence_hits = sum(1 for kw in _EVIDENCE_KEYWORDS if kw in lower)
    evidence_score = min(20, evidence_hits * 5)
    score += evidence_score
    if evidence_hits == 0:
        issues.append("Mention what evidence you have (documents, witnesses, receipts)")

    # 5. Coherence — has parties, dispute, outcome (max 15 pts)
    has_parties = any(w in lower for w in ["my", "i ", "me ", "we ", "our", "plaintiff", "defendant",
                                            "accused", "complainant", "petitioner", "respondent",
                                            "husband", "wife", "landlord", "tenant", "employer", "employee",
                                            "company", "neighbour", "neighbor", "bank", "police"])
    has_dispute = any(w in lower for w in ["dispute", "problem", "issue", "case", "complaint",
                                           "happened", "incident", "violated", "refused", "denied",
                                           "cheated", "fraud", "assault", "stolen", "damaged",
                                           "terminated", "evicted", "encroached", "harassed", "threatened"])
    has_relief = any(w in lower for w in ["want", "seek", "claim", "recover", "compensation",
                                          "damages", "refund", "injunction", "arrest", "bail",
                                          "custody", "maintenance", "divorce", "acquittal", "relief"])

    coherence = 0
    if has_parties:
        coherence += 5
    else:
        issues.append("Mention the parties involved (who is the dispute with)")
    if has_dispute:
        coherence += 5
    else:
        issues.append("Describe what happened or what the dispute is about")
    if has_relief:
        coherence += 5
    score += coherence

    # Final score capped at 100
    score = min(100, max(0, score))

    # Determine label and max probability cap
    if score >= 65:
        label = "Strong"
        max_prob = 95
    elif score >= 45:
        label = "Fair"
        max_prob = 70
    elif score >= 25:
        label = "Weak"
        max_prob = 40
    else:
        label = "Very Weak"
        max_prob = 20

    print(f"[NyayBase] Input quality: score={score}, label={label}, max_prob={max_prob}, "
          f"legal_hits={legal_hits}, evidence={evidence_hits}, words={word_count}")

    return {"score": score, "label": label, "max_probability": max_prob, "issues": issues}


def gibberish_response(reason, facts, case_type_name, jurisdiction_name):
    """Return a friendly, chatbot-like response for invalid inputs."""
    messages = {
        "empty": "It looks like you haven't entered any case details yet.",
        "too_short": "Your input is too brief for me to analyze. I need a proper description of the legal situation.",
        "random_chars": "I couldn't understand the input — it appears to contain random characters rather than a case description.",
        "no_real_words": "The input doesn't seem to contain a recognizable legal scenario.",
        "repeated_chars": "The input appears to contain repeated characters rather than a real case description.",
        "repeated_words": "The input appears to contain repeated words rather than a genuine legal scenario.",
    }
    friendly_msg = messages.get(reason, "I couldn't understand the input provided.")

    return {
        "case_type": case_type_name,
        "jurisdiction": jurisdiction_name,
        "relevant_acts": [],
        "is_invalid_input": True,
        "error_message": f"{friendly_msg} To get an accurate legal analysis, please describe your case with these details:",
        "suggestions": [
            "What happened? (the core dispute or incident)",
            "Who is involved? (parties — e.g., landlord vs tenant, employer vs employee)",
            "When did it happen? (dates, timeline)",
            "What evidence do you have? (documents, witnesses, FIR, agreements)",
            "What relief or outcome do you want? (compensation, injunction, acquittal)"
        ],
        "example_input": "Example: 'My landlord has not returned my security deposit of ₹2,00,000 after I vacated the flat in Mumbai on January 2025. I have the rent agreement and bank transfer receipts as proof. I want to recover the deposit amount plus interest.'",
        "win_probability": {
            "probability": 0, "lower_bound": 0, "upper_bound": 0, "confidence_margin": 0,
            "strength": "Insufficient Input", "strength_color": "#6b7280",
            "base_rate": 0, "adjustment": 0, "factors_detected": 0,
            "reasoning": f"{friendly_msg} Please provide a detailed description of your legal situation so I can analyze it properly."
        },
        "key_arguments": [],
        "timeline": {"estimated_months": 0, "min_months": 0, "max_months": 0, "stages": [], "recommendation": "Please provide valid case details to get timeline estimates."},
        "similar_cases": [],
        "mediation": {"recommendation": "N/A", "color": "#6b7280", "success_rate": 0, "avg_settlement_months": 0, "reasoning": "Cannot recommend mediation without understanding the dispute."},
        "risk_factors": [{"risk": "Insufficient Information", "severity": "High", "description": "No valid legal facts were provided for analysis.", "mitigation": "Please re-enter your case with specific facts, dates, parties, evidence, and the relief you seek."}]
    }


def weak_input_response(input_quality, case_type_name, jurisdiction_name, case_data):
    """Return a response for input that passes gibberish check but is too weak for real analysis."""
    issues = input_quality.get("issues", [])
    quality_label = input_quality.get("label", "Very Weak")
    score = input_quality.get("score", 0)

    return {
        "case_type": case_type_name,
        "jurisdiction": jurisdiction_name,
        "relevant_acts": case_data.get("relevant_acts", []),
        "is_weak_input": True,
        "input_quality": quality_label,
        "input_score": score,
        "win_probability": {
            "probability": 0,
            "lower_bound": 0,
            "upper_bound": 0,
            "confidence_margin": 0,
            "strength": "Insufficient Information",
            "strength_color": "#6b7280",
            "base_rate": 0,
            "adjustment": 0,
            "factors_detected": 0,
            "reasoning": "Your case description does not contain enough specific information for a meaningful analysis. Please provide detailed facts including what happened, who is involved, dates, evidence you have, and what outcome you seek."
        },
        "key_arguments": [],
        "similar_cases": [],
        "timeline": {
            "estimated_months": 0, "min_months": 0, "max_months": 0, "stages": [],
            "recommendation": "Please provide detailed case facts to get timeline estimates."
        },
        "mediation": {
            "recommendation": "N/A", "color": "#6b7280", "success_rate": 0,
            "avg_settlement_months": 0,
            "reasoning": "Cannot assess mediation suitability without understanding the dispute."
        },
        "risk_factors": [{
            "risk": "Insufficient Case Details",
            "severity": "High",
            "description": "No meaningful legal facts were provided. The analysis cannot proceed without specific details about the dispute.",
            "mitigation": "Please re-enter your case with: (1) What happened, (2) Who is involved, (3) Dates and timeline, (4) Evidence you have, (5) What relief you seek."
        }],
        "improvement_tips": issues,
    }


def analyze_case(case_type, facts, jurisdiction, sections, custom_case_type="", adverse_party="", legal_representation=""):
    """Main analysis function — uses local RAG + smart response generation."""
    ct = case_type if case_type in CASE_TYPES else "custom"
    case_data = CASE_TYPES[ct]
    jur_data = JURISDICTIONS.get(jurisdiction, JURISDICTIONS["Other"])
    display_name = custom_case_type if (ct == "custom" and custom_case_type) else case_data["name"]

    # ── Fast regex pre-check for obviously broken input ──
    is_bad, reason = is_gibberish(facts)
    if is_bad:
        print(f"[NyayBase] Input rejected (regex): reason={reason}, input='{facts[:50]}'")
        return gibberish_response(reason, facts, display_name, jur_data["name"])

    # ── Semantic input quality check ──
    input_quality = compute_input_quality(facts)

    # ── Short-circuit: Very weak input → don't waste LLM call ──
    if input_quality["score"] < 25:
        print(f"[NyayBase] Input too weak for LLM (score={input_quality['score']}), returning weak_input_response")
        return weak_input_response(input_quality, display_name, jur_data["name"], case_data)

    # ── RAG search for relevant legal context ──
    try:
        import rag_engine
        query = f"{display_name} {jurisdiction} {facts} {sections}".strip()
        rag_results = rag_engine.search_all(query, top_k=20)
        print(f"[NyayBase] RAG retrieved: {len(rag_results.get('statutes',[]))} statutes, "
              f"{len(rag_results.get('cases',[]))} cases, "
              f"{len(rag_results.get('procedures',[]))} procedures")
    except Exception as e:
        print(f"[NyayBase] RAG search error (using empty context): {e}")
        rag_results = {"statutes": [], "cases": [], "procedures": [], "maxims": []}

    # ── Generate structured analysis from RAG results ──
    try:
        from smart_responder import generate_analysis
        result = generate_analysis(
            case_type=ct,
            facts=facts,
            jurisdiction=jurisdiction,
            sections=sections,
            custom_case_type=custom_case_type,
            rag_results=rag_results,
            adverse_party=adverse_party,
            legal_representation=legal_representation,
            input_quality=input_quality,
        )
        print(f"[NyayBase] Analysis complete — win prob: {result['win_probability']['probability']}%, "
              f"args: {len(result['key_arguments'])}, cases: {len(result['similar_cases'])}")
        return result

    except Exception as e:
        print(f"[NyayBase] Smart responder error: {e}")
        return {
            "is_api_error": True,
            "error": f"Analysis engine encountered an error: {str(e)}. Please try again.",
        }
