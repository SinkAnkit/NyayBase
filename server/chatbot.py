"""
NyayBase — Legal Chatbot Module
Handles general legal queries using RAG + LLM cascade (Gemini → Groq → Ollama).
"""

import re
import random
from llm_providers import call_llm_text

# ── Greeting Detection (instant response, no LLM call) ──
GREETING_PATTERNS = {
    # Exact matches and common typos
    "hello", "helo", "helllo", "hllo", "hellow", "hullo",
    "hi", "hii", "hiii", "hey", "heyy", "heyyy", "hye", "hyi",
    "yo", "yoo", "sup", "ssup", "whatsup", "wassup",
    "good morning", "good afternoon", "good evening", "good night",
    "gm", "gn", "namaste", "namaskar", "namastey",
    "howdy", "greetings", "ola", "hola",
    "thanks", "thank you", "thankyou", "thnx", "thx", "ty",
    "ok", "okay", "okk", "oky", "k", "kk",
    "bye", "byee", "goodbye", "good bye", "see you", "tata",
    "what's up", "whats up", "how are you", "how r u", "how ru",
    "who are you", "what are you", "who r u", "what r u",
}

GREETING_RESPONSES = [
    "Hello! I'm NyayBase Legal Assistant. How can I help you with legal matters today? You can ask me about any area of Indian law — criminal, civil, family, property, consumer rights, and more.",
    "Hi there! I'm your AI legal assistant. Ask me anything about Indian law — from filing an FIR to property disputes, tenant rights, consumer complaints, and more. How can I help?",
    "Hey! Welcome to NyayBase. I'm here to help with any legal questions you have about Indian law. What would you like to know?",
]

THANKS_RESPONSES = [
    "You're welcome! Feel free to ask me anything else about Indian law.",
    "Happy to help! Let me know if you have any more legal questions.",
    "Glad I could help! Don't hesitate to ask if you need more guidance.",
]

BYE_RESPONSES = [
    "Goodbye! Remember, for a detailed case analysis, try our Analyze Case feature. Stay safe!",
    "Take care! If you need legal help later, I'll be right here.",
]

IDENTITY_RESPONSES = [
    "I'm NyayBase Legal Assistant — an AI-powered legal advisor specializing in Indian law. I can help you with questions about criminal law, civil disputes, family law, property matters, consumer rights, labor law, and much more. For detailed case analysis with win probability, use our 'Analyze Case' feature!",
]

def _is_greeting(msg: str) -> str | None:
    """Detect greetings, thanks, byes — return category or None."""
    clean = msg.lower().strip().rstrip("!?.,:;")
    clean = re.sub(r'\s+', ' ', clean)

    if clean in GREETING_PATTERNS:
        if any(w in clean for w in ["thank", "thnx", "thx", "ty"]):
            return "thanks"
        if any(w in clean for w in ["bye", "goodbye", "tata", "see you"]):
            return "bye"
        if any(w in clean for w in ["who are", "what are", "who r", "what r"]):
            return "identity"
        return "greeting"

    # Fuzzy: very short message (1-2 words, <12 chars) that's close to a greeting
    if len(clean) <= 12 and len(clean.split()) <= 2:
        # Check edit distance for common greetings
        for pattern in ["hello", "hey", "hi", "thanks", "bye"]:
            if _similar(clean, pattern):
                if pattern in ["thanks"]:
                    return "thanks"
                if pattern in ["bye"]:
                    return "bye"
                return "greeting"
    return None

def _similar(a: str, b: str) -> bool:
    """Simple similarity check — True if strings differ by <=2 chars."""
    if a == b:
        return True
    if abs(len(a) - len(b)) > 2:
        return False
    # Levenshtein distance <= 2
    d = _edit_distance(a, b)
    return d <= 2

def _edit_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance."""
    if len(s1) < len(s2):
        return _edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[len(s2)]

def _is_simple_query(msg: str) -> bool:
    """Check if message is too short or casual to need RAG search."""
    clean = msg.strip()
    if len(clean) < 8:
        return True
    # Very short questions
    words = clean.split()
    if len(words) <= 3 and not any(legal in clean.lower() for legal in
        ["law", "act", "section", "fir", "court", "bail", "rti", "ipc", "crpc", "bns", "bnss",
         "complaint", "divorce", "custody", "property", "tenant", "rent", "cheque",
         "arrest", "police", "lawyer", "advocate", "judge", "rights", "legal"]):
        return True
    return False


SYSTEM_PROMPT = """You are NyayBase Legal Assistant, a helpful, friendly, and professional Indian legal advisor chatbot.

RULES:
- Address the user directly as "you"/"your"
- Be concise (1-3 paragraphs). For simple questions, give SHORT answers. Don't over-explain.
- Always reference specific Indian laws, acts, and sections when relevant
- If the query is about a procedure (e.g., filing FIR, RTI), give step-by-step instructions
- If the query is too vague, ask ONE clarifying question — don't lecture
- NEVER say "I cannot provide legal advice" — you ARE a legal assistant
- Handle typos gracefully. If the user writes something unclear, interpret the most likely meaning and respond helpfully. Never say "I don't understand what you mean by X" for obvious typos.
- If the user has a specific case to analyze, suggest: "For a detailed case analysis with win probability, timeline, and strategy, use our 'Analyze Case' section."
- End with a SHORT disclaimer: "Note: This is general guidance. Consult a qualified advocate for case-specific advice."
- Be warm and empathetic but professional
- You can answer about ANY area of Indian law: criminal, civil, family, consumer, property, labor, tax, cyber, constitutional rights, etc.
- Keep responses UNDER 200 words unless the question genuinely requires more detail
"""


def chat(message: str, history: list = None) -> str:
    """
    Process a chat message and return a response.
    Smart greeting detection + RAG + LLM cascade (Gemini → Groq → Ollama).
    """
    if not message or not message.strip():
        return "Please ask me a legal question and I'll do my best to help you."

    # ── 1. Instant greeting/casual response (no LLM needed) ──
    greeting_type = _is_greeting(message)
    if greeting_type:
        if greeting_type == "thanks":
            return random.choice(THANKS_RESPONSES)
        elif greeting_type == "bye":
            return random.choice(BYE_RESPONSES)
        elif greeting_type == "identity":
            return random.choice(IDENTITY_RESPONSES)
        else:
            return random.choice(GREETING_RESPONSES)

    # ── 2. Build RAG context (skip for very simple queries) ──
    rag_context = ""
    if not _is_simple_query(message):
        try:
            import rag_engine
            query = message.strip()
            results = rag_engine.search_all(query, top_k=5)

            statutes = results.get("statutes", [])[:3]
            cases = results.get("cases", [])[:2]
            procedures = results.get("procedures", [])[:2]

            if statutes or cases or procedures:
                rag_context = "\n\nRELEVANT LEGAL CONTEXT:\n"
                for s in statutes:
                    d = s["data"]
                    rag_context += f"- {d.get('act', '')} S.{d.get('section', '')}: {d.get('title', '')} — {d.get('summary', d.get('text', ''))[:150]}\n"
                for c in cases:
                    d = c["data"]
                    rag_context += f"- Case: {d.get('name', '')} ({d.get('year', '')}): {d.get('held', '')[:150]}\n"
                for p in procedures:
                    d = p["data"]
                    rag_context += f"- Procedure: {d.get('title', d.get('name', ''))}: {d.get('summary', d.get('text', ''))[:150]}\n"

        except Exception as e:
            print(f"[Chatbot] RAG search error: {e}")

    # ── 3. Build conversation context from history ──
    history_str = ""
    if history and len(history) > 0:
        recent = history[-4:]  # Last 4 exchanges for context
        for h in recent:
            role = h.get("role", "user")
            content = h.get("content", "")[:200]
            history_str += f"\n{'User' if role == 'user' else 'Assistant'}: {content}"

    # ── 4. Compose and send to LLM cascade ──
    full_system = SYSTEM_PROMPT + rag_context
    full_user = ""
    if history_str:
        full_user += f"Previous conversation:{history_str}\n\n"
    full_user += f"Current question: {message}"

    try:
        response = call_llm_text(full_system, full_user)
        if not response:
            return "I apologize, but I'm having trouble generating a response right now. Please try again in a moment."
        return response
    except Exception as e:
        print(f"[Chatbot] Error: {e}")
        return "I'm experiencing technical difficulties. Please try again in a moment."

