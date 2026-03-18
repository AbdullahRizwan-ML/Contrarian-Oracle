# 🔮 The Contrarian Oracle

**An Autonomous Multi-Agent OSINT System for Financial Narrative Deconstruction**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple.svg)](https://www.crewai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)

---

## What Is This?

The Contrarian Oracle uses **4 collaborative AI agents** (built with CrewAI) to perform a **"Red Team" analysis** on any stock ticker. It identifies the dominant market narrative, actively searches for contradicting evidence, and produces a **Divergence Score (0-100)** that quantifies how much hidden risk the mainstream narrative is ignoring.

**⚠️ This is NOT a price prediction tool.** It is an **information arbitrage system.**

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    STREAMLIT UI (app.py)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Sidebar  │  │ Charts   │  │ Agent    │  │ Report │  │
│  │ Controls │  │ (Plotly) │  │ Stream   │  │ View   │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  CREW ORCHESTRATION                       │
│              (src/crew/oracle_crew.py)                    │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐                      │
│  │  Agent 1:    │  │  Agent 2:    │  (Independent)       │
│  │  Trend       │  │  Sentiment   │                      │
│  │  Scraper     │  │  Synthesizer │                      │
│  └──────┬───────┘  └──────┬───────┘                      │
│         │                 │                              │
│         └────────┬────────┘                              │
│                  ▼                                       │
│         ┌──────────────┐                                 │
│         │  Agent 3:    │  (Receives 1 + 2)               │
│         │  Contrarian  │                                 │
│         │  Skeptic     │                                 │
│         └──────┬───────┘                                 │
│                ▼                                         │
│         ┌──────────────┐                                 │
│         │  Agent 4:    │  (Receives 1 + 2 + 3)           │
│         │  Final       │                                 │
│         │  Arbitrator  │                                 │
│         └──────────────┘                                 │
└──────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                     TOOLS LAYER                          │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌────────┐  │
│  │ yfinance │  │ DuckDuck  │  │ SEC      │  │ FRED   │  │
│  │ Tool     │  │ Go News   │  │ EDGAR    │  │ Macro  │  │
│  └──────────┘  └───────────┘  └──────────┘  └────────┘  │
│  ┌──────────────────────────────────────────────────┐    │
│  │              RAG (ChromaDB + Sentence-Transformers)│    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  SCORING ENGINE                          │
│          (src/scoring/divergence_calculator.py)           │
│                                                          │
│  Score = 0.25×Technical + 0.20×Sentiment                 │
│        + 0.25×Insider   + 0.15×Fundamental               │
│        + 0.15×Macro                                      │
│                                                          │
│  0-20: Consensus Aligned  │  61-80: High Alert           │
│  21-40: Minor Cracks      │  81-100: Extreme Divergence  │
│  41-60: Significant Div.  │                              │
└──────────────────────────────────────────────────────────┘
```

---

## Screenshots

> *Screenshots will be added after first run.*

| Landing Page | Analysis Running | Final Report |
|:---:|:---:|:---:|
| ![Landing](docs/screenshots/landing.png) | ![Running](docs/screenshots/running.png) | ![Report](docs/screenshots/report.png) |

---

## Tech Stack

| Component | Technology |
|---|---|
| **Agent Framework** | CrewAI |
| **LLM Providers** | Google Gemini, Groq, Ollama |
| **Market Data** | yfinance |
| **News Search** | DuckDuckGo Search |
| **SEC Filings** | SEC EDGAR API |
| **Macro Data** | FRED API |
| **Vector Database** | ChromaDB |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) |
| **NLP** | TextBlob, NLTK |
| **Technical Analysis** | pandas-ta, custom indicators |
| **UI** | Streamlit |
| **Charts** | Plotly |
| **Validation** | Pydantic v2 |
| **Logging** | Loguru |
| **Testing** | pytest |

---

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/AbdullahRizwan-MLProject/contrarian-oracle.git
cd contrarian-oracle

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys:
# - GEMINI_API_KEY (free at https://aistudio.google.com/)
# - GROQ_API_KEY (free at https://console.groq.com/)
# - FRED_API_KEY (free at https://fred.stlouisfed.org/docs/api/api_key.html)
```

### 3. Run the App

```bash
streamlit run app.py
```

### 4. Run Tests

```bash
pytest tests/ -v
```

---

## The 4 Agents

### 🔍 Agent 1: Trend Scraper
*Senior Market Data Analyst* — 20-year veteran quant. Collects price data, calculates RSI, MACD, MAs, volume analysis, and insider transactions. Reports only facts, never opinions.

### 📰 Agent 2: Sentiment Synthesizer
*Media Narrative Analyst* — Former Bloomberg senior journalist. Analyzes news headlines, classifies sentiment, identifies the mainstream consensus. Knows that when every headline agrees, the trade is crowded.

### 🎯 Agent 3: Contrarian Skeptic
*Adversarial Research Analyst (Red Team)* — Legendary short-seller's head of research. Systematically finds evidence contradicting the mainstream narrative. Checks insider selling, technical divergences, SEC filings, and earnings transcripts.

### ⚖️ Agent 4: Final Arbitrator
*Chief Investment Strategist* — Nobel-caliber economist. Synthesizes bull and bear cases, calculates the Divergence Score, and produces the final verdict. Weighs quality of evidence over quantity.

---

## Divergence Score

The score ranges from **0 to 100**:

| Score | Label | Meaning |
|:---:|---|---|
| 0-20 | 🟢 Consensus Aligned | Market narrative matches reality |
| 21-40 | 🟡 Minor Cracks | Small inconsistencies detected |
| 41-60 | 🟠 Significant Divergence | Notable gaps between narrative and evidence |
| 61-80 | 🔴 High Alert | Major red flags found |
| 81-100 | 🚨 Extreme Divergence | Narrative severely disconnected from reality |

---

## Project Structure

```
contrarian-oracle/
├── app.py                     # Streamlit entry point
├── src/
│   ├── agents/                # 4 CrewAI agent definitions
│   ├── crew/                  # Crew orchestration & tasks
│   ├── tools/                 # Custom CrewAI tools
│   ├── data/                  # Data fetching, caching, processing
│   ├── rag/                   # ChromaDB vector store & retrieval
│   ├── models/                # Pydantic schemas
│   ├── scoring/               # Divergence scoring engine
│   └── config/                # Settings & prompt strings
├── ui/                        # Streamlit UI components
├── data/                      # Runtime data (cache, vectordb)
├── tests/                     # pytest test suite
├── notebooks/                 # Jupyter exploration notebooks
└── docs/                      # Documentation
```

---

## Configuration

All settings are managed via `.env` file and `src/config/settings.py`:

- **LLM Provider**: Switch between Gemini, Groq, or Ollama
- **Score Weights**: Adjust via UI sliders or `.env` defaults
- **Cache TTL**: Configure how long data is cached (default: 4 hours)
- **RAG Settings**: Chunk size, overlap, top-k retrieval

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Disclaimer

⚠️ **The Contrarian Oracle is NOT financial advice.** It is an educational tool for exploring information asymmetries in financial markets. Always do your own research before making investment decisions.

---

*Built by [AbdullahRizwan-MLProject](https://github.com/AbdullahRizwan-MLProject)*
