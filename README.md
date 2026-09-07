# Real Estate Lead Bot

**PrimeHomes Realty Lead Management System**

An AI-assisted lead management system that automatically receives, understands, captures, qualifies, routes, and tracks potential real estate customers.

## Overview

The system acts as a digital receptionist and lead qualification assistant. It transforms unstructured customer conversations into structured lead information using AI and automation, then routes high-quality leads to the sales team.

**Primary Stack:**
- **Frontend:** React
- **Backend:** Python + FastAPI
- **Automation:** n8n
- **AI:** Google Gemini (LLM)
- **Database:** PostgreSQL (system of record)
- **Operational Visibility:** Google Sheets

## Project Structure

```text
real-estate-lead-bot/
├── frontend/          # React customer & sales UI
├── backend/           # FastAPI application
├── n8n/               # Workflow definitions & exports
├── database/          # Migrations, seeds, schema references
├── tests/             # Shared / cross-cutting tests
├── docs/              # Product & technical specifications
├── .env.example       # Environment variable template
├── .gitignore
├── LICENSE
└── README.md
```

## Documentation

All foundational documents live in the `docs/` directory:

| Document | Purpose |
|----------|---------|
| [PRD.md](docs/PRD.md) | Product Requirements Document |
| [SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md) | High-level architecture |
| [TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) | Technical implementation requirements |
| [API_SPEC.md](docs/API_SPEC.md) | API contracts |
| [DATA_MODEL.md](docs/DATA_MODEL.md) | Database schema & entities |
| [AI_AGENT_SPEC.md](docs/AI_AGENT_SPEC.md) | AI behavior & prompts |
| [N8N_WORKFLOW_SPEC.md](docs/N8N_WORKFLOW_SPEC.md) | n8n workflow design |
| [UI_UX_SPEC.md](docs/UI_UX_SPEC.md) | Frontend & UX requirements |
| [TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md) | Testing approach |
| [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | Build phases & order |
| [BUILD_TASKS.md](docs/BUILD_TASKS.md) | Executable development tasks |
| [DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md) | How to work on the project |
| [TASK.md](docs/TASK.md) | Current task tracker |

## Getting Started (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- n8n (local or Docker)
- Git

### 1. Clone & Setup

```bash
git clone https://github.com/adepejuvirtualassistant-afk/real-estate-lead-bot.git
cd real-estate-lead-bot
cp .env.example .env
# Edit .env with your values
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check: http://localhost:8000/health

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Database

Ensure PostgreSQL is running and `DATABASE_URL` is set in `.env`.

### 5. n8n

Run n8n locally and import workflows from `n8n/workflows/` when available.

## Development Philosophy

- Build in small, verifiable increments (see `docs/IMPLEMENTATION_PLAN.md` and `docs/BUILD_TASKS.md`)
- Follow the documented architecture and boundaries
- AI output is always validated before use
- SQL is the system of record; Google Sheets is operational only
- Human-in-the-loop for important decisions

## Current Phase

**Phase 0 — Project Setup** (in progress)

See `docs/TASK.md` for the live task tracker.

## License

MIT — see [LICENSE](LICENSE)
