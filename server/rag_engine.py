"""
NyayBase — RAG Engine
TF-IDF based search over the legal dataset.
Lightweight: <10MB memory, <50ms per query.
"""

import json, os, re, time, threading
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

# ─── Global state ───
_index_ready = False

# Document stores (populated by build_index)
_docs = []           # list of {"text": str, "type": str, "data": dict}
_tfidf_matrix = None
_tfidf_vectorizer = None

DATASET_PATH = os.path.join(os.path.dirname(__file__), "legal_dataset.json")


def _flatten_dataset(db: dict) -> list:
    """Convert the nested legal_dataset.json into flat searchable documents."""
    docs = []

    def s(val):
        """Safe string coercion — handles int, float, bool, None."""
        if val is None:
            return ""
        if isinstance(val, list):
            return " ".join(str(v) for v in val)
        return str(val)

    # Constitution articles
    for item in db.get("constitution", []):
        text = f"Article {s(item.get('article'))} {s(item.get('title'))} {s(item.get('text'))} {s(item.get('usage'))} {s(item.get('category'))}"
        docs.append({"text": text.strip(), "type": "constitution", "data": item})

    # BNS Sections
    for item in db.get("bns_sections", []):
        text = f"BNS Section {s(item.get('bns'))} IPC {s(item.get('ipc'))} {s(item.get('offence'))} {s(item.get('description'))} {s(item.get('punishment'))}"
        docs.append({"text": text.strip(), "type": "bns", "data": item})

    # Civil sections
    for item in db.get("civil_sections", []):
        text = f"{s(item.get('act'))} Section {s(item.get('section'))} {s(item.get('title'))} {s(item.get('summary'))} {s(item.get('usage'))}"
        docs.append({"text": text.strip(), "type": "civil", "data": item})

    # All landmark cases
    for key in ["cases_const_criminal", "cases_civil_others", "cases_specialized", "landmark_cases_extra"]:
        for item in db.get(key, []):
            principles = " ".join(str(p) for p in item.get("principles", []))
            text = f"{s(item.get('name'))} {s(item.get('citation'))} {s(item.get('type'))} {s(item.get('facts'))} {s(item.get('held'))} {principles}"
            docs.append({"text": text.strip(), "type": "case", "data": item})

    # Legal procedures
    for item in db.get("legal_procedures", []):
        steps_text = " ".join(s(step.get("step")) for step in item.get("steps", []) if isinstance(step, dict))
        text = f"{s(item.get('name'))} {s(item.get('description'))} {steps_text}"
        docs.append({"text": text.strip(), "type": "procedure", "data": item})

    # Legal maxims
    for item in db.get("legal_maxims", []):
        text = f"{s(item.get('maxim'))} {s(item.get('meaning'))} {s(item.get('application'))}"
        docs.append({"text": text.strip(), "type": "maxim", "data": item})

    return docs


def build_index():
    """Pre-compute TF-IDF matrix for the full dataset. Call once at startup."""
    global _docs, _tfidf_matrix, _tfidf_vectorizer, _index_ready

    if _index_ready:
        return

    print("[RAG] Building search index...")
    t0 = time.time()

    # Load dataset
    try:
        with open(DATASET_PATH, "r") as f:
            db = json.load(f)
    except Exception as e:
        print(f"[RAG] Error loading dataset: {e}")
        return

    # Flatten
    _docs = _flatten_dataset(db)
    texts = [d["text"] for d in _docs]
    print(f"[RAG] Flattened {len(_docs)} documents from dataset")

    # TF-IDF index (fast, lightweight, <10MB memory)
    _tfidf_vectorizer = TfidfVectorizer(
        max_features=10000,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    _tfidf_matrix = _tfidf_vectorizer.fit_transform(texts)
    print(f"[RAG] TF-IDF index built ({_tfidf_matrix.shape})")

    _index_ready = True
    print(f"[RAG] Index ready in {time.time()-t0:.1f}s")


def search(query: str, top_k: int = 15, doc_types: list = None) -> list:
    """
    TF-IDF based search.
    Returns list of {"score": float, "type": str, "data": dict}.
    """
    if not _index_ready or not _docs:
        return []

    # TF-IDF similarity
    q_tfidf = _tfidf_vectorizer.transform([query])
    scores = sklearn_cosine(q_tfidf, _tfidf_matrix).flatten()

    # Filter by doc type if requested
    if doc_types:
        mask = np.array([d["type"] in doc_types for d in _docs], dtype=bool)
        scores = scores * mask

    # Top-K
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] < 0.05:
            continue
        results.append({
            "score": float(scores[idx]),
            "type": _docs[idx]["type"],
            "data": _docs[idx]["data"],
        })

    return results


def search_cases(query: str, top_k: int = 8) -> list:
    """Search specifically for landmark cases."""
    return search(query, top_k=top_k, doc_types=["case"])


def search_statutes(query: str, top_k: int = 8) -> list:
    """Search specifically for statutory provisions (constitution, BNS, civil)."""
    return search(query, top_k=top_k, doc_types=["constitution", "bns", "civil"])


def search_all(query: str, top_k: int = 20) -> dict:
    """
    Search across all document types and return categorized results.
    Each type gets its own dedicated search to ensure cases are never
    crowded out by the much larger statute pool.
    Returns {"statutes": [...], "cases": [...], "procedures": [...], "maxims": [...]}.
    """
    return {
        "statutes": search(query, top_k=8, doc_types=["constitution", "bns", "civil"]),
        "cases": search(query, top_k=8, doc_types=["case"]),
        "procedures": search(query, top_k=4, doc_types=["procedure"]),
        "maxims": search(query, top_k=4, doc_types=["maxim"]),
    }

