# StockAI RAG

AI-powered stock research assistant using Retrieval-Augmented Generation (RAG), built from scratch in plain Python — without AI code generation tools — to develop genuine understanding of RAG architecture internals.

## What it does

- Fetches live stock data for NSE-listed companies via yfinance
- Chunks and embeds financial data, news and analyst recommendations into a vector store
- Answers natural language questions grounded in real-time market data
- Exposes a FastAPI backend with a lightweight vanilla JS frontend

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **RAG**: ChromaDB (vector store), nomic-embed-text embeddings
- **LLM**: llama3.1:8b via Ollama (runs locally, no API key required)
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

Functional and working. Built as a learning project to understand RAG internals before adopting frameworks. LangChain and CrewAI rebuilds planned as next phase.

## About

AI-powered stock research assistant using RAG — built with yfinance, ChromaDB, FastAPI and Ollama.
