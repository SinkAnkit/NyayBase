<div align="center">

# ⚖️ NyayBase

### AI-Powered Legal Intelligence Platform for India

Predict court case outcomes, discover winning arguments, and get AI-powered legal strategy advice — built on a curated dataset of **2,823 Indian legal statutes, landmark cases, and court data**.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge)](https://nyaybase.vercel.app)
[![Railway](https://img.shields.io/badge/Backend-Railway-blueviolet?style=for-the-badge)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](#license)

</div>

---

## ✨ Features

### 📊 Case Outcome Prediction
AI-powered win probability analysis with confidence intervals, strength rating, and personalized legal strategy. The system scores input quality to prevent misleading results from vague or gibberish inputs.

### 🔍 Similar Case Discovery
TF-IDF based search engine across Indian court judgments, statutes, constitutional articles, and legal maxims — returning relevant precedents categorized by type.

### 🤖 AI Legal Chatbot
Conversational AI assistant for legal queries. Uses a multi-provider LLM cascade (Gemini → Groq) with automatic fallback for high availability.

### ⚔️ Adverse Party Analysis
Counter-argument identification and risk assessment based on opponent type (individual, corporation, government).

### 🏛️ Court Locator
Find nearby courts across India with an interactive Leaflet.js map, directions, and contact info.

### 📰 Legal News Feed
100+ curated articles from LiveLaw, Bar & Bench, and Google News India — auto-refreshing daily at 12 AM IST.

### 📈 Statistics Dashboard
Visual analytics across case types, jurisdictions, and historical outcomes with animated charts.

### 🧠 Smart Input Validation
Multi-layered input quality scoring (0-100) that prevents gibberish or vague inputs from producing misleading win probabilities. Inputs below threshold are rejected with actionable improvement tips.

---

## 🏗️ Architecture

```
┌─────────────────────┐         ┌──────────────────────────┐
│   Frontend (Vercel)  │  HTTPS  │   Backend (Railway)       │
│   Next.js 16 + React│ ◄─────► │   FastAPI + Gunicorn      │
│   CSS Modules        │         │                          │
└─────────────────────┘         │  ┌────────────────────┐  │
                                │  │ Analysis Engine     │  │
                                │  │  • Input Quality    │  │
                                │  │  • Gibberish Check  │  │
                                │  │  • LLM Cascade      │  │
                                │  └────────────────────┘  │
                                │  ┌────────────────────┐  │
                                │  │ RAG Engine (TF-IDF) │  │
                                │  │  • 2,823 documents  │  │
                                │  │  • Bigram indexing  │  │
                                │  └────────────────────┘  │
                                │  ┌────────────────────┐  │
                                │  │ LLM Providers       │  │
                                │  │  Gemini → Groq      │  │
                                │  │  (auto-fallback)    │  │
                                │  └────────────────────┘  │
                                └──────────────────────────┘
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16, React 19, CSS Modules |
| **Backend** | FastAPI, Python 3.12, Gunicorn |
| **Search/RAG** | TF-IDF (scikit-learn) with bigram indexing |
| **LLM Cascade** | Google Gemini → Groq (Llama 3.3 70B) |
| **Maps** | Leaflet.js + OpenStreetMap |
| **News** | RSS feeds via feedparser |
| **Deployment** | Vercel (frontend) + Railway (backend, always-on) |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- At least one LLM API key (Gemini or Groq)

### 1. Clone & Setup

```bash
git clone https://github.com/SinkAnkit/NyayBase.git
cd NyayBase
```

### 2. Backend

```bash
cd server
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env — add your GEMINI_API_KEY and/or GROQ_API_KEY

python3 main.py
```

Backend starts at `http://localhost:8000`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend starts at `http://localhost:3000`

---

## 🔑 Environment Variables

Create `server/.env` from `server/.env.example`:

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key ([Get one](https://aistudio.google.com/apikey)) | Recommended |
| `GROQ_API_KEY` | Groq API key ([Get one](https://console.groq.com)) | Recommended |
| `OLLAMA_BASE_URL` | Local Ollama server URL | Optional (default: `localhost:11434`) |
| `OLLAMA_MODEL` | Local Ollama model name | Optional (default: `gemma2:2b`) |

> **LLM Cascade:** The system tries providers in order — **Gemini → Groq → Ollama**. At least one API key is needed for cloud deployment. Both Gemini and Groq have generous free tiers.

For deployment, also set on your hosting platform:

| Variable | Description | Platform |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL (e.g. `https://your-backend.up.railway.app/api`) | Vercel |
| `RAILWAY_PUBLIC_DOMAIN` | Auto-set by Railway | Railway |

---

## 📁 Project Structure

```
NyayBase/
├── frontend/                   # Next.js frontend (deployed on Vercel)
│   ├── app/
│   │   ├── page.js             # Main SPA — all views (landing, form, results)
│   │   ├── page.module.css     # Component styles
│   │   ├── globals.css         # Design tokens & global styles
│   │   └── layout.js           # Root layout with meta tags
│   ├── vercel.json
│   └── package.json
│
├── server/                     # FastAPI backend (deployed on Railway)
│   ├── main.py                 # API endpoints + keep-alive + CORS
│   ├── analysis_engine.py      # Case prediction — input quality + gibberish detection
│   ├── smart_responder.py      # LLM prompt engineering + response construction
│   ├── llm_providers.py        # Multi-provider LLM cascade (Gemini/Groq/Ollama)
│   ├── rag_engine.py           # TF-IDF search engine over legal dataset
│   ├── knowledge_base.py       # Case types, jurisdictions, legal statistics
│   ├── chatbot.py              # AI legal chatbot (uses LLM cascade)
│   ├── courts_data.py          # 50+ Indian courts with coordinates
│   ├── legal_news.py           # RSS news aggregator (LiveLaw, Bar & Bench)
│   ├── legal_dataset.json      # 2,823 curated legal documents
│   ├── Dockerfile              # Production container (dynamic PORT)
│   ├── requirements.txt
│   └── .env.example
│
├── render.yaml                 # Render deployment config (legacy)
└── .gitignore
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check — returns service status and version |
| `/api/case-types` | GET | List all supported case types with metadata |
| `/api/jurisdictions` | GET | List all supported jurisdictions (High Courts) |
| `/api/analyze` | POST | **Core endpoint** — predict case outcome with AI analysis |
| `/api/chat` | POST | AI legal chatbot conversation |
| `/api/stats` | GET | Aggregate case statistics for dashboard |
| `/api/legal-news` | GET | 100+ curated legal news articles |
| `/api/courts/search` | GET | Search courts by city/state with map coordinates |

### Example: Analyze a Case

```bash
curl -X POST https://nyaybase-api-production.up.railway.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "case_type": "cheque_bounce",
    "jurisdiction": "Delhi",
    "facts": "The accused issued a cheque for Rs 5,00,000 towards repayment of a loan. The cheque was dishonored due to insufficient funds. A legal notice was sent within 30 days but no payment was made within 15 days.",
    "sections": "Section 138 NI Act"
  }'
```

---

## 🧠 How the Analysis Works

1. **Input Validation** — Gibberish detection (regex) + semantic quality scoring (0-100)
2. **Short-Circuit** — If input quality < 25 ("Very Weak"), returns "Insufficient Information" immediately without calling the LLM
3. **RAG Search** — TF-IDF retrieves relevant statutes, landmark cases, procedures, and legal maxims from the 2,823-document dataset
4. **LLM Analysis** — Sends case facts + RAG context to the LLM with detailed prompts. Quality-aware instructions prevent inflated probabilities for weak input
5. **Probability Clamping** — Final win probability is capped by input quality score (e.g., weak input capped at 40%)
6. **Response Assembly** — Combines win probability, key arguments, risk factors, expected timeline, and mediation assessment

### Input Quality Tiers

| Score | Label | Max Probability | Behavior |
|-------|-------|----------------|----------|
| 0–24 | Very Weak | 0% | LLM skipped, "provide more details" screen |
| 25–44 | Weak | 40% | LLM called but probability capped |
| 45–64 | Fair | 70% | Normal analysis with moderate cap |
| 65–100 | Strong | 95% | Full analysis, minimal capping |

---

## 🌐 Deployment

### Current Production Setup

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend | **Vercel** (auto-deploy from `main`) | [nyaybase.vercel.app](https://nyaybase.vercel.app) |
| Backend | **Railway** (always-on, Docker) | `nyaybase-api-production.up.railway.app` |

### Deploy Your Own

**Backend (Railway):**
1. Fork this repo → Connect to [Railway](https://railway.app)
2. Set root directory to `server`
3. Add env vars: `GROQ_API_KEY`, `GEMINI_API_KEY`
4. Deploy — Railway auto-detects the Dockerfile

**Frontend (Vercel):**
1. Import repo on [Vercel](https://vercel.com)
2. Set root directory to `frontend`
3. Add env var: `NEXT_PUBLIC_API_URL = https://your-railway-url.up.railway.app/api`
4. Deploy

---

## 📊 Dataset

The legal dataset (`legal_dataset.json`) contains **2,823 curated documents**:

| Category | Count | Description |
|----------|-------|-------------|
| Constitutional Articles | 50+ | Fundamental rights, directive principles |
| BNS Sections | 200+ | Bharatiya Nyaya Sanhita (new criminal code) with IPC mapping |
| Civil Sections | 300+ | CPC, Transfer of Property, Indian Contract Act, etc. |
| Landmark Cases | 200+ | Supreme Court & High Court judgments with principles |
| Legal Procedures | 50+ | Step-by-step guides for filing, appeals, execution |
| Legal Maxims | 100+ | Latin maxims with meaning and application |

---

## 📄 License

MIT — free for personal and commercial use.

---

<div align="center">

Built with ❤️ for the Indian legal community

**[⭐ Star this repo](https://github.com/SinkAnkit/NyayBase)** if you find it useful!

</div>
