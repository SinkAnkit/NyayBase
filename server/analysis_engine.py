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
