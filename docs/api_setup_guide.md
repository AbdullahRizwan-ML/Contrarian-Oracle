# API Setup Guide

## Required API Keys

### 1. Google Gemini (Recommended - Free)

1. Go to [https://aistudio.google.com/](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" → "Create API Key"
4. Copy the key to `.env` as `GEMINI_API_KEY`

### 2. Groq (Alternative - Free)

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Create an account
3. Navigate to API Keys → Create new key
4. Copy the key to `.env` as `GROQ_API_KEY`

### 3. FRED API (Macro Data - Free)

1. Go to [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Create an account
3. Request an API key
4. Copy the key to `.env` as `FRED_API_KEY`

### 4. Ollama (Local - Free)

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Pull a model: `ollama pull llama3.1:8b`
3. Set `OLLAMA_BASE_URL=http://localhost:11434` in `.env`
4. Set `LLM_PROVIDER=ollama` in `.env`

## No API Key Needed

- **DuckDuckGo Search**: Used for news search, no API key required
- **SEC EDGAR**: Only needs a User-Agent string (pre-configured)
- **yfinance**: Yahoo Finance data, no API key required
- **Sentence-Transformers**: Embedding model downloaded automatically

## Testing Your Setup

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Test Gemini
python -c "import google.generativeai; print('Gemini SDK OK')"

# Test yfinance
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info.get('shortName'))"

# Test ChromaDB
python -c "import chromadb; print(f'ChromaDB {chromadb.__version__}')"
```
