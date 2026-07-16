# ⚡ StockAI RAG

### An AI-powered stock research assistant built from scratch in Python

---

## What This Does

StockAI RAG is a locally-running financial research tool that lets you compare multiple NSE-listed stocks and ask natural language questions about them — fundamentals, news, analyst sentiment, financials, and more.

Select up to 3 stocks, fetch their live data, then ask anything:

- *"Which of these stocks is best for short-term profit booking?"*
- *"Compare TCS and Reliance on revenue growth. Is either a good buy right now?"*
- *"What is Infosys's PE ratio and analyst sentiment over the last 3 months?"*

The system fetches real market data, chunks and embeds it into a local vector store, and answers your questions using a locally-running LLM — with no API keys, no cloud dependency, and no data leaving your machine.

---

## Why I Built This

Built as a **learning project** to understand how RAG (Retrieval-Augmented Generation) actually works under the hood — without using AI code generation tools. Every line of code was written and understood by hand, referencing documentation and debugging real errors.

The goal was to go from "I understand RAG conceptually" to "I built a working RAG pipeline" — and understand what that actually means technically: vector embeddings, cosine similarity search, chunking strategy, prompt construction, and LLM integration — all wired together manually.

This project deliberately avoids high-level RAG frameworks to expose the real mechanics.

---

## Pipeline Architecture

```
User selects stock symbols (up to 3)
        │
        ▼
yfinance → Fetch live stock data
(price, PE, 52W high/low, market cap, news, analyst recommendations, financials)
        │
        ▼
Chunker → Domain-aware chunking
(summary chunk, metrics chunk, news chunks, recommendation chunks, financials chunks)
        │
        ▼
Ollama (nomic-embed-text) → Generate embeddings
        │
        ▼
ChromaDB → Store chunks + embeddings (in-memory, cosine similarity)
        │
        ▼
User asks a natural language question
        │
        ▼
Ollama (nomic-embed-text) → Embed the question
        │
        ▼
ChromaDB → Retrieve top 20 relevant chunks
        │
        ▼
Ollama (llama3.1:8b) → Generate grounded answer
        │
        ▼
FastAPI → Return answer to frontend (Vanilla JS UI)
```

---

## Tech Stack

| Component        | Technology                                      |
|------------------|-------------------------------------------------|
| Language         | Python 3.13                                     |
| Web Framework    | FastAPI + Uvicorn                               |
| Data Source      | yfinance (Yahoo Finance — live NSE data)        |
| Chunking         | Custom domain-aware chunker (pure Python)       |
| Vector Store     | ChromaDB (in-memory, cosine similarity via HNSW)|
| Embeddings       | nomic-embed-text via Ollama (runs locally)      |
| LLM              | llama3.1:8b via Ollama (runs locally)           |
| Templating       | Jinja2                                          |
| Frontend         | Vanilla JS + HTML/CSS                           |

---

## Project Structure

```
stockai-rag/
├── app/
│   ├── main.py          # FastAPI app — routes for /load and /ask
│   ├── fetcher.py       # yfinance integration — fetches live stock data
│   ├── chunker.py       # Domain-aware chunking — splits data into typed chunks
│   ├── vectorstore.py   # ChromaDB integration — embed, store, query
│   ├── rag.py           # RAG pipeline — retrieves context, builds prompt, calls LLM
│   └── templates/
│       └── index.html   # Frontend UI — stock selector + Q&A interface
├── dryrun.py            # CLI dry run — test the pipeline without the web UI
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running locally
- Two local models pulled:
  ```bash
  ollama pull nomic-embed-text
  ollama pull llama3.1:8b
  ```

---

## Setup

**1. Clone and create virtual environment**

```bash
git clone https://github.com/gauravrustogi1/stockai-rag.git
cd stockai-rag
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Start Ollama** (if not already running)

```bash
ollama serve
```

---

## Running the App

```bash
uvicorn app.main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

**Step 1** — Enter up to 3 NSE stock symbols (e.g. `RELIANCE.NS`, `INFY.NS`, `TCS.NS`) and click **Fetch Data**

**Step 2** — Type any natural language question and click **Answer**

---

## Dry Run (CLI — no web UI needed)

To test the full pipeline from the command line:

```bash
python dryrun.py
```

This fetches Reliance data, saves it to the vector store, and asks a sample question — useful for verifying the pipeline end to end before running the web app.

---

## How the Chunking Works

A key design decision in this project is **domain-aware chunking** — rather than splitting text by character count, each stock's data is split into semantically typed chunks:

| Chunk Type       | Contents                                              |
|------------------|-------------------------------------------------------|
| `summary`        | Company's long business summary                       |
| `metrics`        | Current price, PE ratio, 52W high/low, market cap     |
| `news`           | Individual news article summaries (one chunk each)    |
| `recommendation` | Analyst buy/sell/hold ratings per time period         |
| `financials_*`   | Revenue, EBITDA, net income, expenses (grouped by type)|

This means when you ask "what's the analyst sentiment?", the retrieval system finds the recommendation chunks — not a random slice of text mid-paragraph.

---

## What I Learned Building This

- **RAG architecture** — the difference between naive document retrieval and grounded LLM responses; why chunk design matters
- **Vector embeddings** — how `nomic-embed-text` converts text into vectors; cosine similarity vs dot product; why HNSW indexing is used
- **ChromaDB internals** — collection design, metadata filtering, embedding storage, querying with `n_results`
- **Domain-aware chunking** — why splitting financial data by semantic type (metrics, news, financials) produces better retrieval than naive chunking
- **Prompt engineering** — framing the LLM as a research analyst, not an advisor; grounding answers in context; handling LLM verbosity
- **FastAPI** — async routes, Pydantic request models, Jinja2 templating, serving a frontend from FastAPI
- **yfinance internals** — ticker info structure, recommendations DataFrame format, financials matrix, news content structure

---

## Limitations

- **In-memory vector store** — ChromaDB resets on every app restart; re-fetch stocks each session
- **NSE stocks only** — built and tested with NSE-listed symbols (`.NS` suffix via yfinance)
- **Local LLM quality** — answer quality depends on the model; llama3.1:8b is the recommended minimum
- **No investment advice** — this is a data analysis tool; the LLM is explicitly prompted to report data, not recommend trades

---

## Roadmap

- [ ] Persistent ChromaDB storage (no re-fetch on restart)
- [ ] Typeahead / autocomplete for stock symbol input
- [ ] LangChain rebuild (to compare framework vs. from-scratch approach)
- [ ] CrewAI multi-agent rebuild (research agent + analyst agent)
- [ ] Support for BSE symbols and international exchanges

---

## Author

**Gaurav Rustogi** — Engineering Leader with 20+ years experience  
[linkedin.com/in/gauravrustogi](https://linkedin.com/in/gauravrustogi) · [gauravrustogi.dev](https://gauravrustogi.dev)

---

*Built from scratch as a Python learning project. No AI code generation tools were used in writing this codebase (except this README.md file 😉) — every line was written by hand to develop genuine understanding of RAG internals.*
