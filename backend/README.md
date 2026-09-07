# Backend (FastAPI)

Python + FastAPI application that owns the API boundary, request validation, business logic, and database access.

## Structure (target)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       ├── leads.py
│   │       ├── chat.py
│   │       └── customers.py
│   ├── core/
│   │   ├── config.py
│   │   └── errors.py
│   ├── db/
│   │   ├── database.py
│   │   └── session.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── requirements.txt
├── pyproject.toml          # optional
└── README.md
```

## Local Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check: `GET http://localhost:8000/health`

## Principles

- FastAPI owns the trusted API boundary.
- Business rules that must be reliable live here (or in services), not only in n8n.
- AI output is validated before being used for important decisions.
- See `docs/TECHNICAL_SPEC.md` and `docs/API_SPEC.md`.
