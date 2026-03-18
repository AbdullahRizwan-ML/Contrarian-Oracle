# THE CONTRARIAN ORACLE — Complete Build Instructions

## PROJECT IDENTITY

- **Name**: The Contrarian Oracle
- **Subtitle**: An Autonomous Multi-Agent OSINT System for Financial Narrative Deconstruction
- **Author**: AbdullahRizwan-MLProject
- **Python Version**: 3.11+
- **License**: MIT

---

## WHAT THIS PROJECT DOES

This system uses 4 collaborative AI agents (built with CrewAI) to perform a "Red Team" analysis on any stock ticker. It identifies the dominant market narrative, actively searches for contradicting evidence, and produces a **Divergence Score (0-100)** that quantifies how much hidden risk the mainstream narrative is ignoring.

**This is NOT a price prediction tool.** It is an information arbitrage system.

---

## COMPLETE DIRECTORY STRUCTURE

Create this EXACT directory structure. Every file listed below must be created.

```
contrarian-oracle/
│
├── .env.example
├── .env
├── .gitignore
├── .python-version
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── Makefile
│
├── app.py                              # Streamlit entry point
│
├── src/
│   ├── __init__.py                     # empty init
│   │
│   ├── agents/
│   │   ├── __init__.py                 # empty init
│   │   ├── trend_scraper.py            # Agent 1: Market data collector
│   │   ├── sentiment_synthesizer.py    # Agent 2: Narrative analyst
│   │   ├── contrarian_skeptic.py       # Agent 3: Red team adversarial
│   │   └── final_arbitrator.py         # Agent 4: Quant judge
│   │
│   ├── crew/
│   │   ├── __init__.py                 # empty init
│   │   ├── oracle_crew.py              # Crew assembly and kickoff
│   │   └── tasks.py                    # Task definitions for all 4 agents
│   │
│   ├── tools/
│   │   ├── __init__.py                 # empty init
│   │   ├── yfinance_tool.py            # Custom CrewAI tool: stock data
│   │   ├── technical_indicators.py     # RSI, MACD, MA helper functions
│   │   ├── news_search_tool.py         # Custom CrewAI tool: DuckDuckGo news
│   │   ├── sec_edgar_tool.py           # Custom CrewAI tool: SEC filings
│   │   ├── rag_query_tool.py           # Custom CrewAI tool: ChromaDB RAG query
│   │   └── macro_data_tool.py          # Custom CrewAI tool: FRED macro data
│   │
│   ├── data/
│   │   ├── __init__.py                 # empty init
│   │   ├── fetcher.py                  # Unified data fetcher orchestrator
│   │   ├── processor.py                # Data cleaning and transformation
│   │   ├── embedder.py                 # Document embedding pipeline
│   │   └── cache.py                    # SQLite caching layer
│   │
│   ├── rag/
│   │   ├── __init__.py                 # empty init
│   │   ├── vector_store.py             # ChromaDB management
│   │   ├── document_loader.py          # Load and chunk documents
│   │   └── retriever.py                # Semantic search interface
│   │
│   ├── models/
│   │   ├── __init__.py                 # empty init
│   │   ├── market_data.py              # Pydantic schemas for technical data
│   │   ├── sentiment.py                # Pydantic schemas for sentiment
│   │   ├── contrarian.py               # Pydantic schemas for contrarian evidence
│   │   └── report.py                   # Pydantic schemas for final report
│   │
│   ├── scoring/
│   │   ├── __init__.py                 # empty init
│   │   ├── divergence_calculator.py    # Core divergence scoring algorithm
│   │   └── weights.py                  # Configurable score weight profiles
│   │
│   └── config/
│       ├── __init__.py                 # empty init
│       ├── settings.py                 # Pydantic app settings from .env
│       └── prompts.py                  # Centralized agent prompt strings
│
├── ui/
│   ├── __init__.py                     # empty init
│   ├── sidebar.py                      # Streamlit sidebar components
│   ├── agent_stream.py                 # Real-time agent thought display
│   ├── report_view.py                  # Final report renderer with tabs
│   ├── charts.py                       # Plotly chart components
│   └── styles.py                       # Custom CSS strings
│
├── data/
│   ├── cache/                          # SQLite cache files (gitignored)
│   │   └── .gitkeep
│   ├── vectordb/                       # ChromaDB persistence (gitignored)
│   │   └── .gitkeep
│   └── sample_transcripts/             # Sample earnings call transcripts
│       └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # Shared pytest fixtures
│   ├── test_tools/
│   │   ├── __init__.py
│   │   ├── test_yfinance_tool.py
│   │   ├── test_news_search.py
│   │   └── test_sec_edgar.py
│   ├── test_agents/
│   │   ├── __init__.py
│   │   └── test_agent_outputs.py
│   └── test_scoring/
│       ├── __init__.py
│       └── test_divergence.py
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_sentiment_analysis.ipynb
│   └── 03_agent_prototyping.ipynb
│
└── docs/
    ├── architecture.md
    ├── agent_prompts.md
    └── api_setup_guide.md
```

---

## VIRTUAL ENVIRONMENT SETUP

Use this EXACT sequence to set up the project environment:

```bash
# 1. Create project directory
mkdir contrarian-oracle
cd contrarian-oracle

# 2. Create virtual environment with Python 3.11+
python3.11 -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Upgrade pip
pip install --upgrade pip setuptools wheel

# 5. Install all dependencies
pip install -r requirements.txt

# 6. Verify installation
python -c "import crewai; print(f'CrewAI version: {crewai.__version__}')"
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
python -c "import chromadb; print(f'ChromaDB version: {chromadb.__version__}')"
```

---

## REQUIREMENTS.TXT — EXACT CONTENTS

```
# === Core Agent Framework ===
crewai[tools]>=0.80.0
crewai-tools>=0.14.0

# === LLM Providers ===
google-generativeai>=0.8.0
groq>=0.11.0
ollama>=0.3.0
litellm>=1.50.0

# === Data Collection ===
yfinance>=0.2.40
duckduckgo-search>=6.3.0
requests>=2.32.0
beautifulsoup4>=4.12.0
feedparser>=6.0.0

# === Technical Analysis ===
pandas>=2.2.0
numpy>=1.26.0
ta>=0.11.0
pandas-ta>=0.3.14b

# === NLP & Embeddings ===
sentence-transformers>=3.0.0
textblob>=0.18.0
nltk>=3.9.0

# === Vector Database (RAG) ===
chromadb>=0.5.0

# === UI ===
streamlit>=1.38.0
plotly>=5.24.0

# === Settings & Validation ===
pydantic>=2.9.0
pydantic-settings>=2.5.0
python-dotenv>=1.0.0

# === Utilities ===
loguru>=0.7.0
tenacity>=9.0.0
ratelimit>=2.2.1

# === Development ===
pytest>=8.3.0
black>=24.0.0
ruff>=0.6.0
```

---

## .env.example — EXACT CONTENTS

```
# === LLM Provider: gemini, groq, or ollama ===
LLM_PROVIDER=gemini

# === Google Gemini (free at https://aistudio.google.com/) ===
GEMINI_API_KEY=your_gemini_api_key_here

# === Groq (free at https://console.groq.com/) ===
GROQ_API_KEY=your_groq_api_key_here

# === FRED Federal Reserve (free at https://fred.stlouisfed.org/docs/api/api_key.html) ===
FRED_API_KEY=your_fred_api_key_here

# === Ollama local (only if using ollama provider) ===
OLLAMA_BASE_URL=http://localhost:11434

# === SEC EDGAR (no key needed, just identification) ===
SEC_USER_AGENT=ContrariOracle research@example.com
```

---

## .gitignore — EXACT CONTENTS

```
# Virtual environment
venv/
.venv/
env/

# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/
.eggs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data (generated at runtime)
data/cache/*.db
data/cache/*.sqlite
data/vectordb/*
!data/vectordb/.gitkeep
!data/cache/.gitkeep

# Jupyter
.ipynb_checkpoints/
notebooks/.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

---

## pyproject.toml — EXACT CONTENTS

```toml
[project]
name = "contrarian-oracle"
version = "1.0.0"
description = "An Autonomous Multi-Agent OSINT System for Financial Narrative Deconstruction"
requires-python = ">=3.11"

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

---

## Makefile — EXACT CONTENTS

```makefile
.PHONY: setup run test lint clean

setup:
	python3.11 -m venv venv
	. venv/bin/activate && pip install --upgrade pip setuptools wheel
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && streamlit run app.py

test:
	. venv/bin/activate && pytest tests/ -v

lint:
	. venv/bin/activate && ruff check src/ tests/
	. venv/bin/activate && black --check src/ tests/ app.py

format:
	. venv/bin/activate && black src/ tests/ app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf data/cache/*.db data/vectordb/*
```

---

## FILE-BY-FILE IMPLEMENTATION SPECIFICATIONS

### src/config/settings.py

This file loads all configuration from the `.env` file using Pydantic Settings.

- Define an enum `LLMProvider` with values: `gemini`, `groq`, `ollama`
- Define a `Settings` class inheriting from `pydantic_settings.BaseSettings`
- Fields:
  - `llm_provider: LLMProvider` default `gemini`
  - `gemini_api_key: str` default `""`
  - `groq_api_key: str` default `""`
  - `ollama_base_url: str` default `"http://localhost:11434"`
  - `gemini_model: str` default `"gemini/gemini-2.0-flash"`
  - `groq_model: str` default `"groq/llama-3.3-70b-versatile"`
  - `ollama_model: str` default `"ollama/llama3.1:8b"`
  - `news_lookback_hours: int` default `48`
  - `max_news_results: int` default `15`
  - `yfinance_period: str` default `"6mo"`
  - `cache_ttl_hours: int` default `4`
  - `chroma_persist_dir: str` default `"data/vectordb"`
  - `embedding_model: str` default `"all-MiniLM-L6-v2"`
  - `chunk_size: int` default `512`
  - `chunk_overlap: int` default `50`
  - `top_k_retrieval: int` default `5`
  - `weight_technical_divergence: float` default `0.25`
  - `weight_sentiment_uniformity: float` default `0.20`
  - `weight_insider_activity: float` default `0.25`
  - `weight_fundamental_risk: float` default `0.15`
  - `weight_macro_headwinds: float` default `0.15`
  - `sec_user_agent: str` default `"ContrariOracle research@example.com"`
  - `fred_api_key: str` default `""`
- Config inner class: `env_file = ".env"`, `env_file_encoding = "utf-8"`
- Create a module-level singleton: `settings = Settings()`
- Create a helper function `get_llm_model_name() -> str` that returns the correct model string based on `settings.llm_provider`

### src/config/prompts.py

Centralized store for all agent prompt strings. Define these as module-level constants:

- `TREND_SCRAPER_ROLE = "Senior Market Data Analyst"`
- `TREND_SCRAPER_GOAL` — Collect comprehensive technical and fundamental data for a given ticker. Calculate RSI, MACD, MAs, volume analysis. Report only facts, never opinions.
- `TREND_SCRAPER_BACKSTORY` — 20-year veteran quant at Goldman Sachs. Methodical, precise, emotionless. Known for catching subtle technical signals like volume divergences and MA compression. Numbers tell the story.
- `SENTIMENT_SYNTH_ROLE = "Media Narrative Analyst"`
- `SENTIMENT_SYNTH_GOAL` — Analyze last 48 hours of financial news. Identify and articulate the "Mainstream Consensus." Measure sentiment uniformity (high uniformity = contrarian signal).
- `SENTIMENT_SYNTH_BACKSTORY` — Former Bloomberg senior journalist, 15 years covering Wall Street. Understands how narratives are constructed and amplified. Knows that when every headline agrees, the trade is crowded. Sharp eye for early sentiment shifts.
- `CONTRARIAN_ROLE = "Adversarial Research Analyst (Red Team)"`
- `CONTRARIAN_GOAL` — Systematically find evidence CONTRADICTING the mainstream narrative. Search for: insider selling, technical divergences, risks in earnings transcripts, competitive threats, macro headwinds. Cite real evidence. Admit when bull case is genuinely strong.
- `CONTRARIAN_BACKSTORY` — Legendary short-seller's head of research (modeled after Jim Chanos and Carson Block). Career built on finding what everyone misses. Skeptical of consensus, allergic to hype. Follows the money, not headlines. Never fabricates bearish arguments.
- `ARBITRATOR_ROLE = "Chief Investment Strategist & Final Arbitrator"`
- `ARBITRATOR_GOAL` — Synthesize bull and bear cases. Calculate Divergence Score (0-100). Weigh QUALITY of evidence, not just quantity. A single critical insider-selling pattern can outweigh ten bullish headlines.
- `ARBITRATOR_BACKSTORY` — Nobel-caliber economist, former Chief Strategist at Bridgewater. Seen every cycle since 1987. Never takes sides. Assesses arguments like a Supreme Court Justice: evidence strength, internal consistency, historical precedent. Divergence Score has flagged 7 of last 9 corrections.

### src/models/market_data.py

Pydantic models for Agent 1 output:

- `TechnicalSnapshot(BaseModel)`:
  - `ticker: str`
  - `current_price: float`
  - `fifty_two_week_high: float`
  - `fifty_two_week_low: float`
  - `market_cap: str`
  - `sector: str`
  - `industry: str`
  - `pe_ratio: float | str` (can be "N/A")
  - `forward_pe: float | str`
  - `ma_50: float`
  - `ma_200: float | None`
  - `ma_crossover: Literal["Golden Cross", "Death Cross", "Neutral", "Insufficient Data"]`
  - `rsi_14: float`
  - `rsi_signal: Literal["Overbought", "Oversold", "Neutral"]`
  - `macd_value: float`
  - `macd_signal_line: float`
  - `macd_crossover: Literal["Bullish", "Bearish"]`
  - `volume_current: int`
  - `volume_20d_avg: int`
  - `volume_ratio: float`
  - `volume_trend: Literal["Increasing", "Decreasing", "Stable"]`
  - `support_level: float`
  - `resistance_level: float`
  - `insider_sells_90d: int`
  - `insider_buys_90d: int`
  - `overall_technical_bias: Literal["Bullish", "Bearish", "Neutral"]`

### src/models/sentiment.py

Pydantic models for Agent 2 output:

- `HeadlineSentiment(BaseModel)`:
  - `title: str`
  - `source: str`
  - `timestamp: str`
  - `url: str`
  - `sentiment: Literal["Bullish", "Bearish", "Neutral"]`
  - `confidence: float` (0.0 to 1.0)

- `NarrativeAnalysis(BaseModel)`:
  - `ticker: str`
  - `headlines: list[HeadlineSentiment]`
  - `overall_sentiment_score: float` (-1.0 to +1.0)
  - `sentiment_uniformity: float` (0.0 to 1.0, where 1.0 = total consensus)
  - `mainstream_narrative: str` (2-3 sentence summary)
  - `narrative_confidence: Literal["Low", "Medium", "High"]`
  - `num_bullish: int`
  - `num_bearish: int`
  - `num_neutral: int`

### src/models/contrarian.py

Pydantic models for Agent 3 output:

- `ContrarianEvidence(BaseModel)`:
  - `category: str` (e.g., "Insider Selling", "Technical Divergence", "Regulatory Risk")
  - `description: str`
  - `severity: Literal["Low", "Medium", "High", "Critical"]`
  - `source: str`

- `ContrarianAnalysis(BaseModel)`:
  - `ticker: str`
  - `evidence: list[ContrarianEvidence]`
  - `contrarian_narrative: str` (2-3 sentence bear case)
  - `evidence_strength_score: int` (0-100)
  - `key_risks: list[str]` (top 3-5 risks)

### src/models/report.py

Final report model for Agent 4 output:

- `FinalReport(BaseModel)`:
  - `ticker: str`
  - `analysis_timestamp: datetime`
  - `divergence_score: int` (0-100)
  - `divergence_label: Literal["Consensus Aligned", "Minor Cracks", "Significant Divergence", "High Alert", "Extreme Divergence"]`
  - `score_breakdown: dict` with keys: `technical_divergence`, `sentiment_uniformity`, `insider_activity`, `fundamental_risk`, `macro_headwinds` — each a float 0-100
  - `bull_case_summary: str`
  - `bear_case_summary: str`
  - `key_risk_factors: list[str]`
  - `verdict: str` (full paragraph)
  - `confidence_level: Literal["Low", "Medium", "High"]`
  - `technical: TechnicalSnapshot`
  - `narrative: NarrativeAnalysis`
  - `contrarian: ContrarianAnalysis`

### src/tools/yfinance_tool.py

Custom CrewAI tool that wraps yfinance:

- Class `YFinanceTool(BaseTool)` with `name = "Stock Data Fetcher"`
- `args_schema` using Pydantic: takes `ticker: str` and optional `period: str`
- `_run()` method:
  1. Creates `yf.Ticker(ticker)`
  2. Fetches history with `stock.history(period=period)`
  3. Gets `stock.info` for fundamentals
  4. Calculates 50-day MA: `hist['Close'].rolling(window=50).mean().iloc[-1]`
  5. Calculates 200-day MA: same with `window=200`, handle case when < 200 days of data
  6. Determines MA crossover: Golden Cross if MA50 > MA200, Death Cross if MA50 < MA200
  7. Calculates RSI (14-day):
     - `delta = hist['Close'].diff()`
     - `gain = delta.where(delta > 0, 0).rolling(14).mean()`
     - `loss = (-delta.where(delta < 0, 0)).rolling(14).mean()`
     - `rs = gain / loss`
     - `rsi = 100 - (100 / (1 + rs))`
  8. Calculates MACD:
     - `ema_12 = hist['Close'].ewm(span=12, adjust=False).mean()`
     - `ema_26 = hist['Close'].ewm(span=26, adjust=False).mean()`
     - `macd_line = ema_12 - ema_26`
     - `signal_line = macd_line.ewm(span=9, adjust=False).mean()`
  9. Volume analysis: current volume vs 20-day average, compute ratio
  10. Support/Resistance: 20-day rolling low/high
  11. Insider transactions: `stock.insider_transactions` — count buys vs sells
  12. Returns all data as a formatted string (dict converted to str)
  13. Wraps everything in try/except, returns error string on failure

### src/tools/news_search_tool.py

Custom CrewAI tool using `duckduckgo-search` library:

- Class `FinancialNewsSearchTool(BaseTool)` with `name = "Financial News Search"`
- `_run(query: str, max_results: int = 15) -> str`:
  1. Creates `DDGS()` context manager
  2. Calls `ddgs.news(keywords=query, max_results=max_results, timelimit="w")`
  3. Extracts: title, body (snippet), source, date, url from each result
  4. Formats output as numbered article list with clear labels
  5. Handles empty results gracefully
  6. Wraps in try/except

### src/tools/sec_edgar_tool.py

Custom CrewAI tool for SEC EDGAR:

- Class `SECEdgarTool(BaseTool)` with `name = "SEC EDGAR Filing Fetcher"`
- Helper method `_get_cik(ticker: str) -> str | None`:
  1. Fetches `https://www.sec.gov/files/company_tickers.json`
  2. Must include `User-Agent` header from settings
  3. Searches for matching ticker, returns CIK padded to 10 digits
- `_run(ticker: str, filing_type: str = "10-K", count: int = 3) -> str`:
  1. Gets CIK via `_get_cik()`
  2. Fetches `https://data.sec.gov/submissions/CIK{cik}.json`
  3. Parses `filings.recent` for form type, date, accession number
  4. Constructs filing URLs
  5. Returns formatted list of filings

### src/tools/rag_query_tool.py

Custom CrewAI tool for querying ChromaDB:

- Class `RAGQueryTool(BaseTool)` with `name = "Earnings Transcript Search"`
- `_run(ticker: str, query: str) -> str`:
  1. Instantiates `VectorStore()`
  2. Calls `store.query(ticker, query, n_results=5)`
  3. If no results, returns message saying RAG store not populated yet
  4. Formats results with relevance percentage (1 - distance), source, date, content
  5. Wraps in try/except

### src/tools/macro_data_tool.py

Custom CrewAI tool for FRED API:

- Class `MacroDataTool(BaseTool)` with `name = "Macro Economic Data"`
- `_run(indicator: str = "all") -> str`:
  1. Fetches these FRED series (use requests + FRED API):
     - `DFF` — Federal Funds Rate
     - `T10Y2Y` — 10Y-2Y Treasury Spread (yield curve)
     - `UNRATE` — Unemployment Rate
     - `CPIAUCSL` — CPI (inflation)
     - `VIXCLS` — VIX Volatility Index
  2. For each: get latest value and 3-month-ago value, compute change
  3. Flag: rates rising/falling, yield curve inverted, VIX elevated (>20)
  4. Returns formatted summary

### src/tools/technical_indicators.py

Pure helper functions (not a CrewAI tool):

- `calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series`
- `calculate_macd(prices: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series]` — returns macd_line, signal_line, histogram
- `calculate_bollinger_bands(prices: pd.Series, period: int = 20, std: int = 2) -> tuple`
- `detect_divergence(prices: pd.Series, indicator: pd.Series, lookback: int = 14) -> str` — returns "Bullish Divergence", "Bearish Divergence", or "No Divergence"
- `identify_support_resistance(hist: pd.DataFrame, window: int = 20) -> dict`

### src/rag/vector_store.py

ChromaDB vector store management:

- Class `VectorStore`:
  - `__init__()`: Creates `chromadb.PersistentClient(path=settings.chroma_persist_dir)` and `SentenceTransformerEmbeddingFunction(model_name=settings.embedding_model)`
  - `get_or_create_collection(ticker: str) -> Collection`: collection name = `oracle_{ticker_lowercase}`
  - `add_documents(ticker, documents, metadatas, ids)`: upserts to collection
  - `query(ticker, query_text, n_results=5) -> dict`: queries collection, returns documents/metadatas/distances
  - `ingest_transcript(ticker, transcript_text, metadata) -> int`: chunks text, adds to store, returns chunk count
  - `_chunk_text(text, chunk_size=512, overlap=50) -> list[str]`: splits on words with overlapping windows

### src/rag/document_loader.py

Document loading and preprocessing:

- `load_text_file(filepath: str) -> str`
- `load_earnings_transcript(filepath: str) -> dict` with keys: text, date, company, quarter
- `clean_text(text: str) -> str` — remove extra whitespace, special chars
- `chunk_documents(text: str, chunk_size: int, overlap: int) -> list[str]`

### src/rag/retriever.py

High-level RAG retrieval interface:

- Class `TranscriptRetriever`:
  - `__init__(vector_store: VectorStore)`
  - `search(ticker: str, query: str, top_k: int = 5) -> list[dict]` — returns list of {content, source, date, relevance_score}
  - `search_risks(ticker: str) -> list[dict]` — pre-built query for risk factors
  - `search_guidance(ticker: str) -> list[dict]` — pre-built query for forward guidance

### src/data/cache.py

SQLite-based caching layer:

- Class `DataCache`:
  - Uses SQLite database at `data/cache/oracle_cache.db`
  - `get(key: str) -> str | None` — returns cached value if not expired
  - `set(key: str, value: str, ttl_hours: int = None)` — stores with TTL from settings
  - `is_valid(key: str) -> bool` — checks if cache entry exists and not expired
  - `clear(ticker: str = None)` — clears cache for specific ticker or all

### src/data/fetcher.py

Unified data fetcher that orchestrates all data collection:

- Class `DataFetcher`:
  - `__init__(cache: DataCache)`
  - `fetch_market_data(ticker: str) -> dict` — uses yfinance, checks cache first
  - `fetch_news(ticker: str) -> list[dict]` — uses DuckDuckGo, checks cache
  - `fetch_sec_filings(ticker: str) -> list[dict]` — uses SEC EDGAR, checks cache
  - `fetch_macro_data() -> dict` — uses FRED, checks cache

### src/data/processor.py

Data cleaning and transformation:

- `clean_market_data(raw: dict) -> TechnicalSnapshot`
- `clean_news_data(raw: list[dict]) -> list[HeadlineSentiment]`
- `normalize_sentiment_score(headlines: list[HeadlineSentiment]) -> float`
- `calculate_sentiment_uniformity(headlines: list[HeadlineSentiment]) -> float`

### src/scoring/divergence_calculator.py

The core scoring algorithm:

- Dataclass `DivergenceComponents` with fields: `technical_divergence`, `sentiment_uniformity`, `insider_activity`, `fundamental_risk`, `macro_headwinds` — all float 0-100

- Class `DivergenceCalculator`:
  - `__init__(weights: dict | None = None)` — uses settings weights as defaults
  - `calculate_technical_divergence(price_trend, rsi, rsi_trend, volume_trend, macd_signal, ma_crossover) -> float`:
    - Price up + RSI falling = +35 (bearish divergence)
    - RSI > 70 = +20, RSI > 80 = +30 (overbought)
    - Price up + volume decreasing = +20 (weak rally)
    - Price up + MACD bearish = +15 (momentum loss)
    - Death Cross = +10
    - Cap at 100
  - `calculate_sentiment_uniformity(sentiment_score, uniformity, num_bullish, num_bearish, num_total) -> float`:
    - Uniformity > 0.85 = +40, > 0.70 = +25, > 0.55 = +10
    - abs(sentiment) > 0.8 = +30, > 0.6 = +15
    - Bull ratio > 0.85 or < 0.15 = +30 (no dissent)
    - Cap at 100
  - `calculate_insider_activity(net_sells_90d, ceo_sold, total_value_sold, market_cap) -> float`:
    - Net sells > 10 = +35, > 5 = +20, > 2 = +10
    - CEO sold = +25
    - Sell value / market_cap > 0.1% = +25, > 0.05% = +15, > 0.01% = +5
    - Cap at 100
  - `calculate_fundamental_risk(num_risk_factors, max_severity, has_earnings_miss, guidance_lowered) -> float`:
    - Severity map: Low=5, Medium=15, High=30, Critical=50
    - Per risk factor: +5, capped at +25
    - Earnings miss: +15
    - Guidance lowered: +20
    - Cap at 100
  - `calculate_macro_headwinds(rate_sensitive, rates_rising, sector_rotating_away, recession_risk_elevated) -> float`:
    - Rate sensitive AND rates rising = +30
    - Sector rotating away = +35
    - Recession risk elevated = +25
    - Cap at 100
  - `compute_final_score(components: DivergenceComponents) -> tuple[int, str]`:
    - Weighted sum of all components
    - Returns (score, label) where labels are: 0-20 "Consensus Aligned", 21-40 "Minor Cracks", 41-60 "Significant Divergence", 61-80 "High Alert", 81-100 "Extreme Divergence"

### src/scoring/weights.py

Configurable weight profiles:

- `DEFAULT_WEIGHTS` dict matching settings defaults
- `AGGRESSIVE_WEIGHTS` — higher weight on insider activity and technicals
- `CONSERVATIVE_WEIGHTS` — higher weight on fundamentals and macro
- `get_weights(profile: str = "default") -> dict`

### src/agents/trend_scraper.py

Agent 1 definition:

- Function `create_trend_scraper() -> Agent`:
  - Uses role, goal, backstory from `src/config/prompts.py`
  - Tools: `[YFinanceTool()]`
  - LLM: `get_llm_model_name()` from settings
  - `verbose=True, memory=True, max_iter=3, allow_delegation=False`

### src/agents/sentiment_synthesizer.py

Agent 2 definition:

- Function `create_sentiment_synthesizer() -> Agent`:
  - Uses role, goal, backstory from prompts
  - Tools: `[FinancialNewsSearchTool()]`
  - LLM from settings
  - `verbose=True, memory=True, max_iter=3, allow_delegation=False`

### src/agents/contrarian_skeptic.py

Agent 3 definition:

- Function `create_contrarian_skeptic() -> Agent`:
  - Uses role, goal, backstory from prompts
  - Tools: `[FinancialNewsSearchTool(), SECEdgarTool(), RAGQueryTool()]`
  - LLM from settings
  - `verbose=True, memory=True, max_iter=5, allow_delegation=False`
  - NOTE: Gets 5 iterations (more than others) because it needs to search multiple sources

### src/agents/final_arbitrator.py

Agent 4 definition:

- Function `create_final_arbitrator() -> Agent`:
  - Uses role, goal, backstory from prompts
  - Tools: `[]` (NO tools — pure reasoning only)
  - LLM from settings
  - `verbose=True, memory=True, max_iter=3, allow_delegation=False`

### src/crew/tasks.py

Task definitions:

- Function `create_tasks(ticker: str) -> dict`:
  - Creates all 4 agents
  - Defines 4 tasks:

  1. `task_technicals` — assigned to trend_scraper:
     - Description: Collect market data for {ticker}, calculate all indicators, report facts
     - Expected output: detailed technical report with all metrics

  2. `task_sentiment` — assigned to sentiment_synth:
     - Description: Search latest news for {ticker}, classify headlines, calculate sentiment score, identify mainstream narrative
     - Expected output: narrative analysis with headline breakdown

  3. `task_contrarian` — assigned to contrarian skeptic:
     - Description: DESTROY the bull case. Search for risks, insider selling, technical divergences. Check SEC filings. Query earnings transcripts. Rate severity of each evidence.
     - `context=[task_technicals, task_sentiment]` — receives outputs from agents 1 and 2
     - Expected output: ranked contrarian evidence with sources

  4. `task_arbitration` — assigned to arbitrator:
     - Description: Synthesize bull and bear cases. Calculate Divergence Score using weighted formula. Produce full report.
     - `context=[task_technicals, task_sentiment, task_contrarian]` — receives ALL outputs
     - Expected output: complete final report with score breakdown

  - Returns `{"agents": [all 4], "tasks": [all 4]}`

### src/crew/oracle_crew.py

Crew assembly and execution:

- Class `OracleCrew`:
  - `__init__(ticker: str)`: stores uppercase ticker, initializes result=None
  - `run() -> str`:
    1. Calls `create_tasks(self.ticker)`
    2. Creates `Crew(agents=..., tasks=..., process=Process.sequential, verbose=True, memory=True, embedder={"provider": "huggingface", "config": {"model": "all-MiniLM-L6-v2"}}, full_output=True)`
    3. Calls `crew.kickoff()`
    4. Stores and returns result
  - `get_result() -> str`: returns stored result

### ui/styles.py

CSS string constants for Streamlit:

- `MAIN_CSS` — styles for:
  - `.main-header`: gradient text (purple to teal), large font, centered
  - `.sub-header`: gray italic, centered
  - `.score-card`: large centered number with colored background
  - `.agent-thought`: dark background, left border teal, monospace font
  - `.metric-card`: dark gradient background, rounded corners, subtle border
  - `.evidence-item`: styled cards for contrarian evidence with severity colors

### ui/sidebar.py

Streamlit sidebar component:

- Function `render_sidebar() -> dict`:
  - Ticker text input (default "NVDA", max 5 chars)
  - LLM provider selectbox: Gemini, Groq, Ollama
  - Divider
  - Score weight sliders (5 sliders, each 0-100, defaults matching settings)
  - Divider
  - "Run Contrarian Analysis" primary button
  - Disclaimer caption
  - Returns dict with all sidebar values

### ui/charts.py

Plotly chart components:

- `create_price_chart(ticker: str, hist_data: pd.DataFrame) -> go.Figure` — candlestick chart with MA50/MA200 overlays
- `create_sentiment_pie(num_bullish, num_bearish, num_neutral) -> go.Figure` — pie chart in green/red/gray
- `create_divergence_gauge(score: int) -> go.Figure` — gauge/speedometer chart for the divergence score
- `create_score_breakdown_radar(breakdown: dict) -> go.Figure` — radar/spider chart of 5 scoring components

### ui/agent_stream.py

Real-time agent thought display:

- Function `render_agent_progress(agent_name: str, status: str, thoughts: list[str])`:
  - Uses `st.status()` for expandable progress sections
  - Shows agent name and role
  - Lists each thought/action as it happens
  - Updates status (running → complete)

### ui/report_view.py

Final report renderer:

- Function `render_report(report: FinalReport)`:
  - Creates tabs: Bull Case, Bear Case, Technicals, Evidence, Verdict
  - Bull Case tab: narrative summary, headline table, sentiment score
  - Bear Case tab: contrarian narrative, evidence cards with severity badges
  - Technicals tab: price chart, indicator summary table
  - Evidence tab: full ranked evidence list with expandable details
  - Verdict tab: divergence gauge, score breakdown radar, verdict text

### app.py (Streamlit Entry Point)

Main application file:

- Set page config: title="The Contrarian Oracle", icon="🔮", layout="wide"
- Inject CSS from `ui/styles.py`
- Render gradient header and subtitle
- Render sidebar via `ui/sidebar.py`
- When "Run" button clicked:
  1. Show left column (2/3 width): agent progress stream
  2. Show right column (1/3 width): score card
  3. Create `OracleCrew(ticker)` and call `run()`
  4. Display real-time agent thoughts as they execute
  5. After completion: render full report below with tabs
- When not running: show landing state with 4 agent cards explaining the system
- Add disclaimer: "Not financial advice. For educational purposes only."

### tests/conftest.py

Shared pytest fixtures:

- `sample_ticker` fixture returning "NVDA"
- `sample_hist_data` fixture returning a mock DataFrame with 100 rows of OHLCV data
- `sample_headlines` fixture returning a list of 10 mock HeadlineSentiment objects
- `sample_components` fixture returning a DivergenceComponents instance

### tests/test_tools/test_yfinance_tool.py

- `test_yfinance_tool_valid_ticker()` — test with "AAPL", verify output contains expected fields
- `test_yfinance_tool_invalid_ticker()` — test with "XYZXYZ123", verify error handling
- `test_rsi_calculation()` — verify RSI calculation against known values
- `test_macd_calculation()` — verify MACD calculation

### tests/test_tools/test_news_search.py

- `test_news_search_returns_results()` — test with "NVDA stock news"
- `test_news_search_empty_query()` — test with obscure query

### tests/test_scoring/test_divergence.py

- `test_consensus_aligned()` — all low scores → score 0-20
- `test_extreme_divergence()` — all high scores → score 81-100
- `test_weight_normalization()` — verify weights sum reasonably
- `test_individual_components()` — test each component calculator
- `test_score_label_mapping()` — verify correct labels for each range

---

## AGENT COMMUNICATION FLOW

The agents communicate through CrewAI's built-in context passing:

```
Agent 1 (Trend Scraper)
  │ output: Technical analysis text
  ▼
Agent 2 (Sentiment Synth) — runs independently of Agent 1
  │ output: Narrative analysis text
  ▼
Agent 3 (Contrarian Skeptic)
  │ receives: Agent 1 + Agent 2 outputs via `context` parameter
  │ output: Contrarian evidence text
  ▼
Agent 4 (Arbitrator)
  │ receives: Agent 1 + Agent 2 + Agent 3 outputs via `context` parameter
  │ output: Final report with Divergence Score
```

Tasks 1 and 2 are INDEPENDENT (could theoretically run in parallel).
Task 3 DEPENDS on tasks 1 and 2.
Task 4 DEPENDS on tasks 1, 2, and 3.

The `process=Process.sequential` in CrewAI ensures they run in order.

---

## DIVERGENCE SCORE FORMULA

```
Score = (0.25 × Technical) + (0.20 × Sentiment) + (0.25 × Insider) + (0.15 × Fundamental) + (0.15 × Macro)

Where each component is 0-100 and:
  0-20   → "Consensus Aligned"
  21-40  → "Minor Cracks"
  41-60  → "Significant Divergence"
  61-80  → "High Alert"
  81-100 → "Extreme Divergence"
```

---

## CRITICAL IMPLEMENTATION NOTES

1. All `__init__.py` files should be EMPTY (just a comment like `# package init`).
2. Every CrewAI tool must inherit from `crewai.tools.BaseTool` and implement `_run()`.
3. Every tool must have `name`, `description`, and `args_schema` class attributes.
4. Use `loguru.logger` for all logging (not Python's built-in `logging`).
5. All API calls must have `try/except` with meaningful error messages.
6. All API calls to external services should have `timeout=10` parameter.
7. The SEC EDGAR API REQUIRES a `User-Agent` header — requests without it are blocked.
8. DuckDuckGo search requires NO API key — use the `duckduckgo-search` library directly.
9. For yfinance, handle the case where `stock.insider_transactions` may be `None` or empty.
10. ChromaDB collections are named `oracle_{ticker_lowercase}` (e.g., `oracle_nvda`).
11. The embeddings model `all-MiniLM-L6-v2` is downloaded automatically by `sentence-transformers` on first use.
12. The Streamlit app should handle the case where analysis hasn't run yet (show landing state).
13. All Pydantic models should use `from __future__ import annotations` for forward references if needed.
14. Use `Literal` types from `typing` for all enum-like string fields in Pydantic models.

---

## HOW TO RUN THE PROJECT

```bash
# After all files are created:

# 1. Copy .env.example to .env and fill in your API keys
cp .env.example .env

# 2. Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Run the Streamlit app
streamlit run app.py

# 4. Run tests
pytest tests/ -v

# 5. Lint and format
make lint
make format
```