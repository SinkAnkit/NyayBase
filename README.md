# NyayBase ⚖️

**AI-Powered Legal Intelligence Platform for India**

NyayBase predicts court case outcomes, discovers winning arguments, and provides AI-powered legal strategy advice — built on analysis of **2,823 Indian legal statutes, landmark cases, and court data**.

### 🔗 [Try NyayBase Live →](https://nyaybase.vercel.app)

---

## Features

- **Case Outcome Prediction** — AI-powered win probability analysis using historical case data
- **Similar Case Discovery** — RAG-based semantic search across Indian court judgments
- **Legal Strategy Advice** — AI-generated arguments, precedents, and winning strategies
- **Adverse Party Analysis** — Counter-argument and risk assessment
- **Court Locator** — Find nearby courts with interactive Leaflet map and directions
- **Legal News Feed** — 100+ curated articles from LiveLaw, Bar & Bench, and Google News India (refreshes daily at 12 AM IST)
- **AI Legal Chatbot** — Conversational AI assistant for legal queries
- **Statistics Dashboard** — Visual analytics across case types, jurisdictions, and outcomes
- **URL Routing** — Browser back/forward and page refresh work correctly

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16, React 19, CSS Modules |
| **Backend** | FastAPI, Python 3.12 |
| **AI/ML** | Sentence Transformers (RAG), scikit-learn |
| **LLM Cascade** | Google Gemini → Groq (Llama 3.3) → Ollama (local) |
| **News** | RSS feeds via feedparser |
| **Deployment** | Vercel (frontend) + Render (backend) |

## Quick Start (Local Development)

### 1. Clone & Install

```bash
git clone https://github.com/SinkAnkit/NyayBase.git
cd NyayBase
```

### 2. Backend Setup

```bash
cd server
pip install -r requirements.txt

# Copy and configure API keys
cp .env.example .env
# Edit .env with your GEMINI_API_KEY and GROQ_API_KEY

python3 main.py
```

Backend runs at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`

## Environment Variables

Create `server/.env` from `server/.env.example`:

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Optional (cascade) |
| `GROQ_API_KEY` | Groq API key | Optional (cascade) |
| `OLLAMA_BASE_URL` | Local Ollama server URL | Optional (default: localhost:11434) |
| `OLLAMA_MODEL` | Ollama model name | Optional (default: gemma2:2b) |

The LLM system uses a **3-tier cascade**: Gemini → Groq → Ollama. It tries each provider in order and uses whichever responds first.

## Project Structure

```
NyayBase/
├── frontend/           # Next.js 16 frontend
│   ├── app/
│   │   ├── page.js     # Main application
│   │   ├── page.module.css
│   │   ├── globals.css
│   │   └── layout.js
│   └── package.json
├── server/             # FastAPI backend
│   ├── main.py         # API endpoints
│   ├── analysis_engine.py  # Case prediction engine
│   ├── knowledge_base.py   # Legal dataset
│   ├── rag_engine.py       # Semantic search (RAG)
│   ├── llm_providers.py    # LLM cascade (Gemini/Groq/Ollama)
│   ├── chatbot.py          # AI chatbot
│   ├── courts_data.py      # Court locator database
│   ├── legal_news.py       # RSS news aggregator
│   ├── Dockerfile          # For cloud deployment
│   ├── requirements.txt
│   ├── .env.example
│   └── legal_dataset.json
└── .gitignore
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Predict case outcome |
| `/api/legal-news` | GET | Get 102 curated legal news articles |
| `/api/courts/search` | GET | Search courts by location |
| `/api/stats` | GET | Case statistics |
| `/api/case-types` | GET | Available case types |
| `/api/jurisdictions` | GET | Available jurisdictions |
| `/api/chat` | POST | AI chatbot conversation |
| `/api/health` | GET | Health check |

## Deployment

- **Live Site:** [nyaybase.vercel.app](https://nyaybase.vercel.app)
- Frontend hosted on **Vercel**, Backend hosted on **Render**

## License

MIT

---

Built with ❤️ for the Indian legal community.
