# Agentic Insights Copilot

> AI-powered analytics planning assistant — turns plain-English business questions into structured segmentation briefs using RAG and Groq LLM.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.3-1C3C3C?logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-F55036?logo=groq&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?logo=docker&logoColor=white)
![AWS ECS](https://img.shields.io/badge/AWS-ECS_Express-FF9900?logo=amazonaws&logoColor=white)

---

## Live Demo

**[https://co-42334f43db734366b0c188714c294893.ecs.us-east-1.on.aws](https://co-42334f43db734366b0c188714c294893.ecs.us-east-1.on.aws)**

> Screenshot: [Add screenshot of UI here]

---

## What It Does

Analytics and strategy teams regularly face the same problem: a stakeholder arrives with a vague question like _"How should we segment our customers?"_ and it takes hours of back-and-forth to turn that into a usable analysis plan.

**Agentic Insights Copilot** short-circuits that process. Submit a plain-English business question and the system returns a structured segmentation brief in seconds — grounded in a curated segmentation playbook via RAG, not just generic LLM output.

### How RAG is used

1. The user's question is embedded using `all-MiniLM-L6-v2` (HuggingFace)
2. The top 3 most relevant chunks are retrieved from a ChromaDB vector store built from `data/segmentation_playbook.md`
3. Retrieved context + the user question are passed to Groq's `llama-3.3-70b-versatile`
4. The LLM returns a Pydantic-validated `SegmentationBrief` via structured output

### What a segmentation brief contains

| Field | Description |
|---|---|
| `business_objective` | The business goal behind the request |
| `target_population` | Who the analysis is focused on |
| `recommended_segmentation_approach` | Best-fit approach based on retrieved context |
| `alternative_approaches` | Other reasonable approaches if applicable |
| `suggested_variables` | Useful features to consider (demographic, behavioral, financial) |
| `recommended_method` | Rules-based, clustering-based, or hybrid |
| `expected_deliverables` | Likely outputs for the stakeholder |
| `assumptions_and_risks` | Key assumptions, ambiguities, and risks |
| `missing_information` | What additional context would improve the recommendation |

---

## Architecture

```
User (Browser)
      │
      │  POST /api/brief  {"question": "..."}
      ▼
┌─────────────────────────────────────────────┐
│              FastAPI  (app/api.py)           │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│           Retrieval  (app/retrieval.py)      │
│                                             │
│  HuggingFace Embeddings (all-MiniLM-L6-v2)  │
│           ↓                                 │
│    ChromaDB vector store                    │
│    (chroma_store/ — baked into image)       │
│           ↓                                 │
│    Top-3 relevant chunks returned           │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│           Generator  (app/generator.py)      │
│                                             │
│  Groq API  (llama-3.3-70b-versatile)        │
│  + retrieved context + system prompt        │
│           ↓                                 │
│  Pydantic SegmentationBrief (structured)    │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
             JSON response → Browser
```

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | [Groq](https://console.groq.com) — `llama-3.3-70b-versatile` |
| Orchestration | [LangChain](https://python.langchain.com) 1.3 |
| Vector DB | [ChromaDB](https://www.trychroma.com) 1.5 |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| API Framework | [FastAPI](https://fastapi.tiangolo.com) 0.115 + Uvicorn |
| Schema / Validation | [Pydantic](https://docs.pydantic.dev) v2 |
| Deployment | Docker → AWS ECR → AWS ECS Express Mode |

---

## Project Structure

```
Agentic Insights Copilot/
├── app/
│   ├── api.py            # FastAPI app — endpoints, HTML UI, health check
│   ├── main.py           # run_pipeline() — core logic + CLI entry point
│   ├── retrieval.py      # ChromaDB retriever with module-level cache
│   ├── generator.py      # Groq/Ollama LLM + SegmentationBrief schema
│   └── prompts.py        # System prompt for grounding LLM output
├── data/
│   └── segmentation_playbook.md   # Knowledge base — RAG source document
├── chroma_store/          # Pre-built vector store (baked into Docker image)
├── eval/
│   ├── retrieval_notes.md         # Retrieval quality notes
│   └── test_prompts.md            # Manual test cases
├── docs/
│   └── prompt_iteration_notes.md  # Prompt engineering log
├── prompts/               # Prompt drafts and experiments
├── .env.example           # Environment variable template
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt       # Production dependencies
└── requirements-dev.txt   # Dev dependencies (Ollama, Jupyter, etc.)
```

---

## Local Development

### Prerequisites

- Python 3.11+
- Docker Desktop (for containerized run)
- A free [Groq API key](https://console.groq.com)

### Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd "Agentic Insights Copilot"

# 2. Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install development dependencies
pip install -r requirements-dev.txt
```

### Configure environment

```bash
# Copy the template
cp .env.example .env
```

Edit `.env` and add your key:

```env
GROQ_API_KEY=your_groq_key_here       # Get from https://console.groq.com
GROQ_MODEL=llama-3.3-70b-versatile
USE_GROQ=true
ENVIRONMENT=development
```

### Run the web app

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8080 --reload
```

Open [http://localhost:8080](http://localhost:8080)

### Run in CLI mode

```bash
python -m app.main
```

### Run with Docker

```bash
docker build -t copilot-local .

docker run -p 8080:8080 \
  -e GROQ_API_KEY=your_key_here \
  -e USE_GROQ=true \
  -e GROQ_MODEL=llama-3.3-70b-versatile \
  copilot-local
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | Yes (if `USE_GROQ=true`) | — | Groq API key — get from [console.groq.com](https://console.groq.com) |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Groq model ID to use |
| `USE_GROQ` | No | `true` | Set `false` to fall back to local Ollama (`qwen2.5:3b`) |
| `ENVIRONMENT` | No | `development` | Runtime environment label |

---

## Deployment

The app is containerized and deployed to AWS ECS Express Mode:

```
docker build -t copilot-local .
docker tag copilot-local:latest <ecr-uri>/copilot:latest
docker push <ecr-uri>/copilot:latest
# → Force new ECS deployment
```

**Switching LLM providers:**
- **Groq (production):** set `USE_GROQ=true` and provide `GROQ_API_KEY`
- **Ollama (local dev):** set `USE_GROQ=false`, run `ollama pull qwen2.5:3b` locally — no API key required

The ChromaDB vector store is baked into the Docker image at build time (`chroma_store/`), so no embedding step runs at startup. The HuggingFace embedding model loads lazily on the first request and is cached in memory for the container's lifetime.

---

## Future Improvements

- **LangGraph orchestration** — multi-step agentic workflows with state management (clarification → retrieval → generation → validation)
- **Improved UI** — richer interface with session history, follow-up questions, and brief export
- **RAGAS evaluation** — programmatic retrieval and generation quality scoring to track regression
- **Multi-domain playbooks** — extend beyond segmentation to churn, pricing, and propensity modeling briefs
- **Authentication** — user auth and session isolation for production team use

---

## About

Analytics planning — turning a stakeholder's ambiguous question into a 
sound analytical approach — is a skill that often lives as tribal knowledge. 
It happens informally, inconsistently, and takes years to develop.

This project explores whether RAG and structured LLM output can encode 
some of that domain expertise, making analytics planning faster, more 
consistent, and more accessible to teams earlier in the process.

It is also a hands-on exploration of applying agentic AI patterns to 
real analytical workflows, rather than synthetic toy problems.