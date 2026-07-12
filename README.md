# StockAI RAG

AI-powered stock research assistant using Retrieval-Augmented Generation (RAG).

## What it does
- Fetches live stock data for NSE-listed companies via yfinance
- Chunks and embeds financial data, news, and analyst recommendations
- Answers natural language questions grounded in real data
- Built with FastAPI, ChromaDB, Ollama, and llama3.1:8b

## Tech Stack
- **Backend**: Python, FastAPI, Uvicorn
- **RAG**: ChromaDB (in-memory), nomic-embed-text embeddings
- **LLM**: llama3.1:8b via Ollama (runs locally)
- **Data**: yfinance (Yahoo Finance)
- **Frontend**: Vanilla JS, HTML/CSS

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull nomic-embed-text
ollama pull llama3.1:8b
uvicorn app.main:app --reload
```

## Status
Work in progress — Day 2 of a 9-day learning project.
Raw Python build complete. LangChain and CrewAI rebuilds coming next.