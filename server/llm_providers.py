"""
NyayBase — LLM Provider Abstraction
3-tier cascade: Google Gemini → Groq → Ollama (local)
"""

import json, os, re, time, requests
from dotenv import load_dotenv

load_dotenv()

# ─── Configuration ───
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma2:2b")


def _parse_json(raw: str) -> dict:
    """Extract and parse JSON from LLM response text."""
    raw = raw.strip()
    # Strip markdown code fences
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Provider 1: Google Gemini
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _call_gemini(system_prompt: str, user_msg: str) -> dict:
    """Call Google Gemini 2.0 Flash via REST API."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": user_msg}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json",
        },
    }
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # Extract text from Gemini response
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return _parse_json(text)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Provider 2: Groq
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]

def _call_groq(system_prompt: str, user_msg: str) -> dict:
    """Call Groq API with model cascade (70B → 8B)."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set")

    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)

    for i, model in enumerate(GROQ_MODELS):
        retries = 2 if i == 0 else 1
        for attempt in range(retries):
            try:
                if attempt > 0:
                    wait = 3 * (2 ** (attempt - 1))
                    print(f"[LLM] Groq retry {attempt} on {model}, waiting {wait}s...")
                    time.sleep(wait)

                print(f"[LLM] Calling Groq {model} (attempt {attempt+1}/{retries})")
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg},
                    ],
                    temperature=0.3,
                    max_tokens=4096,
                )
                raw = response.choices[0].message.content.strip()
                return _parse_json(raw)

            except Exception as e:
                print(f"[LLM] Groq {model} failed (attempt {attempt+1}): {e}")
                err_str = str(e).lower()
                if "rate_limit" not in err_str and "429" not in err_str:
                    break  # Non-rate-limit error, try next model

    raise RuntimeError("All Groq models exhausted")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Provider 3: Ollama (local)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _call_ollama(system_prompt: str, user_msg: str) -> dict:
    """Call local Ollama server."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 4096},
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    raw = resp.json()["message"]["content"]
    return _parse_json(raw)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Text-mode providers (for chatbot — returns plain text, not JSON)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _call_gemini_text(system_prompt: str, user_msg: str) -> str:
    """Call Google Gemini 2.0 Flash and return plain text."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": user_msg}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 1024,
        },
    }
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def _call_groq_text(system_prompt: str, user_msg: str) -> str:
    """Call Groq API and return plain text."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set")

    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)

    for i, model in enumerate(GROQ_MODELS):
        retries = 2 if i == 0 else 1
        for attempt in range(retries):
            try:
                if attempt > 0:
                    wait = 3 * (2 ** (attempt - 1))
                    print(f"[LLM] Groq text retry {attempt} on {model}, waiting {wait}s...")
                    time.sleep(wait)

                print(f"[LLM] Calling Groq {model} text mode (attempt {attempt+1}/{retries})")
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg},
                    ],
                    temperature=0.5,
                    max_tokens=1024,
                )
                return response.choices[0].message.content.strip()

            except Exception as e:
                print(f"[LLM] Groq {model} text failed (attempt {attempt+1}): {e}")
                err_str = str(e).lower()
                if "rate_limit" not in err_str and "429" not in err_str:
                    break

    raise RuntimeError("All Groq models exhausted (text mode)")


def _call_ollama_text(system_prompt: str, user_msg: str) -> str:
    """Call local Ollama server and return plain text."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        "stream": False,
        "options": {"temperature": 0.5, "num_predict": 1024},
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main cascade functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROVIDERS = [
    ("Gemini", _call_gemini),
    ("Groq", _call_groq),
    ("Ollama", _call_ollama),
]

TEXT_PROVIDERS = [
    ("Gemini", _call_gemini_text),
    ("Groq", _call_groq_text),
    ("Ollama", _call_ollama_text),
]


def call_llm(system_prompt: str, user_msg: str) -> dict:
    """
    Call LLM with automatic cascade: Gemini → Groq → Ollama.
    Returns parsed JSON dict from whichever provider succeeds first.
    Raises RuntimeError only if ALL providers fail.
    """
    errors = []

    for name, fn in PROVIDERS:
        try:
            print(f"[LLM] Trying {name}...")
            result = fn(system_prompt, user_msg)
            print(f"[LLM] ✓ Success via {name}")
            return result
        except Exception as e:
            err_msg = f"{name}: {e}"
            print(f"[LLM] ✗ {err_msg}")
            errors.append(err_msg)

    raise RuntimeError(f"All LLM providers failed: {'; '.join(errors)}")


def call_llm_text(system_prompt: str, user_msg: str) -> str:
    """
    Call LLM with automatic cascade: Gemini → Groq → Ollama.
    Returns plain text string from whichever provider succeeds first.
    Used by chatbot for conversational responses.
    Raises RuntimeError only if ALL providers fail.
    """
    errors = []

    for name, fn in TEXT_PROVIDERS:
        try:
            print(f"[LLM-Text] Trying {name}...")
            result = fn(system_prompt, user_msg)
            print(f"[LLM-Text] ✓ Success via {name}")
            return result
        except Exception as e:
            err_msg = f"{name}: {e}"
            print(f"[LLM-Text] ✗ {err_msg}")
            errors.append(err_msg)

    raise RuntimeError(f"All LLM providers failed (text mode): {'; '.join(errors)}")
