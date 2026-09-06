# REAL ESTATE LEAD BOT — TASK TRACKER

## Project

**Project Name:** Real Estate Lead Bot  
**Client:** PrimeHomes Realty  
**Status:** Development  
**Architecture:** React + FastAPI + n8n + Gemini + PostgreSQL + Google Sheets

---

# Task Status

- `TODO` — Not started
- `IN_PROGRESS` — Currently working
- `BLOCKED` — Waiting for something
- `IN_REVIEW` — Implementation completed, needs review
- `DONE` — Completed and tested

---

# PHASE 0 — PROJECT SETUP

## TASK-001 — Create Project Structure

**Status:** TODO  
**Priority:** P0

### Objective

Create the basic project folders.

### Structure

```text
real-estate-lead-bot/
├── frontend/
├── backend/
├── n8n/
├── database/
├── tests/
├── docs/
└── README.md
```

### Acceptance Criteria

- [ ] All directories created.
- [ ] `README.md` created.
- [ ] Existing documentation remains inside `docs/`.
- [ ] No application code yet.

---

## TASK-002 — Initialize Git

**Status:** TODO  
**Priority:** P0

### Objective

Initialize version control.

### Requirements

Create:

```text
main
develop
feature/*
```

### Acceptance Criteria

- [ ] Git repository initialized.
- [ ] `.gitignore` created.
- [ ] `.env` excluded.
- [ ] Secrets excluded.
- [ ] Initial commit created.

---

## TASK-003 — Environment Configuration

**Status:** TODO  
**Priority:** P0

### Objective

Create environment configuration for local development.

### Backend Variables

```text
DATABASE_URL=
GEMINI_API_KEY=
N8N_WEBHOOK_URL=
N8N_WEBHOOK_SECRET=
ENVIRONMENT=development
```

### Frontend Variables

```text
VITE_API_BASE_URL=http://localhost:8000
```

### Acceptance Criteria

- [ ] `.env.example` created.
- [ ] `.env` ignored by Git.
- [ ] No real credentials committed.
- [ ] Backend can load configuration.

---

# PHASE 1 — FASTAPI BACKEND

## TASK-004 — Create FastAPI Application

**Status:** TODO  
**Priority:** P0

### Objective

Create the initial FastAPI backend.

### Expected Structure

```text
backend/
└── app/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   └── v1/
    ├── core/
    ├── db/
    ├── models/
    ├── schemas/
    └── services/
```

### Acceptance Criteria

- [ ] FastAPI installed.
- [ ] Application starts.
- [ ] No import errors.
- [ ] Root endpoint responds.

---

## TASK-005 — Health Endpoint

**Status:** TODO  
**Priority:** P0

### Endpoint

```text
GET /health
```

### Expected Response

```json
{
  "status": "ok"
}
```

### Acceptance Criteria

- [ ] HTTP 200 returned.
- [ ] JSON response returned.
- [ ] Endpoint works locally.

---

## TASK-006 — Backend Configuration

**Status:** TODO  
**Priority:** P0

### Objective

Create centralized application configuration.

### File

```text
backend/app/core/config.py
```

### Acceptance Criteria

- [ ] Environment variables loaded.
- [ ] Configuration centralized.
- [ ] Secrets not hard-coded.

---

# PHASE 2 — DATABASE

## TASK-007 — PostgreSQL Setup

**Status:** TODO  
**Priority:** P0

### Objective

Set PostgreSQL as the primary application database.

### Acceptance Criteria

- [ ] PostgreSQL available locally.
- [ ] Database created.
- [ ] Connection string configured.

---

## TASK-008 — Database Connection

**Status:** TODO  
**Priority:** P0

### Files

```text
backend/app/db/database.py
backend/app/db/session.py
```

### Acceptance Criteria

- [ ] FastAPI connects to PostgreSQL.
- [ ] Connection errors handled.
- [ ] Database session available to services.

---

# PHASE 3 — DATA MODELS

## TASK-009 — Customer Model

**Status:** TODO  
**Priority:** P0

Fields:

```text
id
name
email
phone
created_at
updated_at
```

---

## TASK-010 — Lead Model

**Status:** TODO  
**Priority:** P0

Fields:

```text
id
customer_id
status
intent
property_type
bedrooms
location
budget_min
budget_max
currency
timeline
source
assigned_agent_id
created_at
updated_at
```

---

## TASK-011 — Conversation Model

**Status:** TODO  
**Priority:** P0

Fields:

```text
id
customer_id
lead_id
status
created_at
updated_at
```

---

## TASK-012 — Message Model

**Status:** TODO  
**Priority:** P0

Fields:

```text
id
conversation_id
sender_type
content
created_at
```

---

## TASK-013 — Qualification Model

**Status:** TODO  
**Priority:** P1

Fields:

```text
id
lead_id
score
classification
reasons
missing_fields
confidence
qualified_at
```

---

## TASK-014 — Follow-Up Model

**Status:** TODO  
**Priority:** P1

Fields:

```text
id
lead_id
assigned_agent_id
type
status
scheduled_at
completed_at
notes
```

---

# PHASE 4 — API

## TASK-015 — Lead Create API

**Status:** TODO  
**Priority:** P0

```text
POST /api/v1/leads
```

---

## TASK-016 — Lead List API

**Status:** TODO  
**Priority:** P0

```text
GET /api/v1/leads
```

---

## TASK-017 — Lead Detail API

**Status:** TODO  
**Priority:** P0

```text
GET /api/v1/leads/{lead_id}
```

---

## TASK-018 — Lead Update API

**Status:** TODO  
**Priority:** P0

```text
PATCH /api/v1/leads/{lead_id}
```

---

## TASK-019 — Lead Qualification API

**Status:** TODO  
**Priority:** P1

```text
POST /api/v1/leads/{lead_id}/qualify
```

---

## TASK-020 — Chat API

**Status:** TODO  
**Priority:** P0

```text
POST /api/v1/chat
```

---

# PHASE 5 — REACT FRONTEND

## TASK-021 — Initialize React

**Status:** TODO

---

## TASK-022 — Home Page

**Status:** TODO

---

## TASK-023 — Chat Interface

**Status:** TODO

Components:

```text
ChatWindow
MessageList
MessageBubble
ChatInput
TypingIndicator
```

---

## TASK-024 — FastAPI Connection

**Status:** TODO

Create:

```text
frontend/src/services/api.js
```

---

## TASK-025 — Chat State

**Status:** TODO

Track:

```text
conversation_id
messages
loading
error
```

---

## TASK-026 — Contact Form

**Status:** TODO

Fields:

```text
name
email
phone
```

---

# PHASE 6 — N8N

## TASK-027 — Lead Intake Workflow

**Status:** TODO

Workflow:

```text
RE-LEAD-01 Lead Intake
```

---

## TASK-028 — AI Processing Workflow

**Status:** TODO

Workflow:

```text
RE-LEAD-02 AI Processing
```

---

## TASK-029 — Qualification Workflow

**Status:** TODO

---

## TASK-030 — Sales Notification Workflow

**Status:** TODO

---

## TASK-031 — Google Sheets Sync

**Status:** TODO

---

## TASK-032 — Follow-Up Automation

**Status:** TODO

---

# PHASE 7 — AI

## TASK-033 — Intent Detection

**Status:** TODO

Supported intents:

```text
BUY
RENT
SELL
LAND
PROPERTY_ENQUIRY
UNKNOWN
```

---

## TASK-034 — Requirement Extraction

**Status:** TODO

Extract:

```text
property_type
bedrooms
location
budget
timeline
intent
```

---

## TASK-035 — Missing Field Detection

**Status:** TODO

---

## TASK-036 — Requirement Normalization

**Status:** TODO

---

## TASK-037 — Customer Response Generation

**Status:** TODO

---

## TASK-038 — AI Confidence

**Status:** TODO

---

# PHASE 8 — LEAD QUALIFICATION

## TASK-039 — Qualification Rules

**Status:** TODO

---

## TASK-040 — Qualification Score

**Status:** TODO

---

## TASK-041 — Lead Classification

**Status:** TODO

```text
90–100 → HOT
70–89  → WARM
0–69   → COLD
```

---

# PHASE 9 — TESTING

## TASK-042 — Backend Tests

**Status:** TODO

---

## TASK-043 — API Tests

**Status:** TODO

---

## TASK-044 — Database Tests

**Status:** TODO

---

## TASK-045 — AI Evaluation Tests

**Status:** TODO

---

## TASK-046 — n8n Workflow Tests

**Status:** TODO

---

## TASK-047 — End-to-End Tests

**Status:** TODO

---

# PHASE 10 — MVP VALIDATION

## TASK-048 — Complete Customer Journey

**Status:** TODO

Test:

```text
Customer
 ↓
React
 ↓
FastAPI
 ↓
n8n
 ↓
Gemini
 ↓
Validation
 ↓
PostgreSQL
 ↓
Qualification
 ↓
Sales Notification
 ↓
Google Sheets
```

---

# CURRENT TASK

## TASK-001

**Create Project Structure**

### Current Status

`TODO`

### Next Action

Create the folders defined in this document.

After completion:

```text
TASK-001 → DONE
TASK-002 → IN_PROGRESS
```

Do not begin TASK-002 until TASK-001 has been verified.

---

# RULE

Only work on the **current task** unless a dependency requires another task.

Do not implement the entire application at once.

```text
ONE TASK
   ↓
IMPLEMENT
   ↓
TEST
   ↓
REVIEW
   ↓
MARK DONE
   ↓
NEXT TASK
```