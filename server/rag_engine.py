"""
NyayBase — RAG Engine
Hybrid semantic search (sentence-transformers) + TF-IDF over the legal dataset.
Lightweight: ~80MB embedding model on CPU, <100ms per query after warm-up.
"""

import json, os, re, time, threading
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

# ─── Global state ───
_model = None
_model_lock = threading.Lock()
_index_ready = False

# Document stores (populated by build_index)
_docs = []           # list of {"text": str, "type": str, "data": dict}
_embeddings = None   # np.ndarray (N, dim)
_tfidf_matrix = None
_tfidf_vectorizer = None

DATASET_PATH = os.path.join(os.path.dirname(__file__), "legal_dataset.json")
MODEL_NAME = "all-MiniLM-L6-v2"  # 80MB, fast on CPU


def _get_model():
    """Lazy-load the sentence-transformers model (thread-safe)."""
    global _model
    if _model is not None:
        return _model
    with _model_lock:
        if _model is not None:
            return _model
        print(f"[RAG] Loading embedding model '{MODEL_NAME}'...")
        t0 = time.time()
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
        print(f"[RAG] Model loaded in {time.time()-t0:.1f}s")
        return _model


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
    """Pre-compute embeddings + TF-IDF matrix for the full dataset. Call once at startup."""
    global _docs, _embeddings, _tfidf_matrix, _tfidf_vectorizer, _index_ready

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

    # TF-IDF index (fast, lightweight)
    _tfidf_vectorizer = TfidfVectorizer(
        max_features=8000,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    _tfidf_matrix = _tfidf_vectorizer.fit_transform(texts)
    print(f"[RAG] TF-IDF index built ({_tfidf_matrix.shape})")

    # Semantic embeddings (heavier but more accurate)
    model = _get_model()
    _embeddings = model.encode(texts, batch_size=128, show_progress_bar=True, normalize_embeddings=True)
    _embeddings = np.array(_embeddings, dtype=np.float32)
    print(f"[RAG] Embeddings computed ({_embeddings.shape})")

    _index_ready = True
    print(f"[RAG] Index ready in {time.time()-t0:.1f}s")


def search(query: str, top_k: int = 15, doc_types: list = None) -> list:
    """
    Hybrid search: 70% semantic + 30% TF-IDF.
    Returns list of {"score": float, "type": str, "data": dict}.
    """
    if not _index_ready or not _docs:
        return []

    model = _get_model()

    # Semantic similarity
    q_emb = model.encode([query], normalize_embeddings=True)
    q_emb = np.array(q_emb, dtype=np.float32)
    sem_scores = np.dot(_embeddings, q_emb.T).flatten()

    # TF-IDF similarity
    q_tfidf = _tfidf_vectorizer.transform([query])
    tfidf_scores = sklearn_cosine(q_tfidf, _tfidf_matrix).flatten()

    # Hybrid score
    combined = 0.7 * sem_scores + 0.3 * tfidf_scores

    # Filter by doc type if requested
    if doc_types:
        mask = np.array([d["type"] in doc_types for d in _docs], dtype=bool)
        combined = combined * mask

    # Top-K
    top_indices = np.argsort(combined)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if combined[idx] < 0.05:
            continue
        results.append({
            "score": float(combined[idx]),
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
    Returns {"statutes": [...], "cases": [...], "procedures": [...], "maxims": [...]}.
    """
    results = search(query, top_k=top_k)

    categorized = {"statutes": [], "cases": [], "procedures": [], "maxims": []}
    for r in results:
        if r["type"] in ("constitution", "bns", "civil"):
            categorized["statutes"].append(r)
        elif r["type"] == "case":
            categorized["cases"].append(r)
        elif r["type"] == "procedure":
            categorized["procedures"].append(r)
        elif r["type"] == "maxim":
            categorized["maxims"].append(r)

    return categorized
