# BUILD TASKS

## 1. Document Purpose

This document converts the system specifications and implementation plan into **small, executable development tasks**.

It is designed for:

- Human developers
- AI coding assistants
- Agentic development workflows
- Code review
- Progress tracking
- Testing and debugging

The goal is to prevent the developer or AI assistant from trying to build the entire system at once.

---

# 2. Development Principle

Build the system in **small vertical slices**.

Each task should:

1. Have a clear purpose.
2. Have defined files.
3. Have clear dependencies.
4. Have a measurable result.
5. Include tests where appropriate.
6. Avoid changing unrelated parts of the system.
7. Keep documentation synchronized with implementation.

The preferred development cycle is:

```text
TASK
 ↓
UNDERSTAND
 ↓
PLAN
 ↓
IMPLEMENT
 ↓
TEST
 ↓
REVIEW
 ↓
DOCUMENT
 ↓
COMMIT
```

---

# 3. System Development Order

The project should be built in this order:

```text
1. Project Setup
        ↓
2. Backend Foundation
        ↓
3. Database
        ↓
4. API
        ↓
5. Frontend
        ↓
6. FastAPI ↔ n8n Integration
        ↓
7. AI Processing
        ↓
8. Lead Qualification
        ↓
9. Notifications
        ↓
10. Google Sheets
        ↓
11. Follow-Up Automation
        ↓
12. End-to-End Testing
        ↓
13. Optimization
```

Do not begin advanced optimization before the MVP works end-to-end.

---

# 4. Task Status

Use the following status values:

```text
TODO
IN_PROGRESS
BLOCKED
IN_REVIEW
DONE
```

Optional priority:

```text
P0 = Critical
P1 = Important
P2 = Nice to have
```

---

# 5. Phase 0 — Project Setup

## TASK-001 — Create Project Structure

**Priority:** P0

Create:

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

- All required directories exist.
- `docs/` contains project documentation.
- Root README exists.
- No application logic is added yet.

---

## TASK-002 — Initialize Git Repository

**Priority:** P0

Initialize Git and create:

```text
main
develop
```

Feature branches should follow:

```text
feature/<feature-name>
```

Example:

```text
feature/backend-health-endpoint
feature/lead-api
feature/chat-ui
feature/ai-extraction
```

### Acceptance Criteria

- Git repository initialized.
- `.gitignore` created.
- Secrets and environment files excluded.
- Initial commit created.

---

## TASK-003 — Create Environment Configuration

**Priority:** P0

Create environment configuration for:

```text
backend
frontend
n8n
database
AI provider
```

Example backend variables:

```text
DATABASE_URL=
N8N_WEBHOOK_URL=
N8N_WEBHOOK_SECRET=
GEMINI_API_KEY=
ENVIRONMENT=development
```

Frontend:

```text
VITE_API_BASE_URL=http://localhost:8000
```

### Rules

Never commit:

```text
.env
.env.local
API keys
passwords
tokens
OAuth secrets
database credentials
```

---

# 6. Phase 1 — Backend Foundation

## TASK-004 — Create FastAPI Application

**Priority:** P0

Create the FastAPI application.

Expected structure:

```text
backend/
└── app/
    ├── main.py
    ├── api/
    ├── models/
    ├── schemas/
    ├── services/
    ├── db/
    └── core/
```

### Acceptance Criteria

The application starts successfully.

Expected development server:

```text
http://localhost:8000
```

FastAPI documentation should be available through its standard OpenAPI interfaces.

---

## TASK-005 — Create Health Endpoint

**Priority:** P0

Create:

```text
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Acceptance Criteria

- Endpoint returns HTTP 200.
- Response is JSON.
- Health endpoint does not require authentication.

---

## TASK-006 — Configure Application Settings

**Priority:** P0

Create centralized configuration.

Example:

```text
backend/app/core/config.py
```

Configuration should load values from environment variables.

Do not hard-code secrets.

---

# 7. Phase 2 — Database

## TASK-007 — Configure PostgreSQL

**Priority:** P0

Configure PostgreSQL as the primary application database.

Database responsibility:

```text
PostgreSQL
    ↓
Source of Truth
```

Google Sheets is NOT the primary database.

---

## TASK-008 — Configure Database Connection

**Priority:** P0

Create:

```text
backend/app/db/database.py
backend/app/db/session.py
```

### Acceptance Criteria

- FastAPI can connect to PostgreSQL.
- Connection errors are handled clearly.
- Database credentials come from environment variables.

---

## TASK-009 — Create Customer Model

**Priority:** P0

Create the customer database model.

Minimum fields:

```text
id
name
email
phone
created_at
updated_at
```

---

## TASK-010 — Create Lead Model

**Priority:** P0

Create the lead model based on `DATA_MODEL.md`.

Minimum fields:

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

## TASK-011 — Create Conversation Model

**Priority:** P0

Create:

```text
conversations
```

Fields should include:

```text
id
customer_id
lead_id
status
created_at
updated_at
```

---

## TASK-012 — Create Message Model

**Priority:** P0

Create:

```text
messages
```

Minimum fields:

```text
id
conversation_id
sender_type
content
created_at
```

Sender types:

```text
CUSTOMER
AI
SALES_AGENT
SYSTEM
```

---

## TASK-013 — Create Qualification Model

**Priority:** P1

Create:

```text
lead_qualifications
```

Include:

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

## TASK-014 — Create Follow-Up Model

**Priority:** P1

Create:

```text
follow_ups
```

Include:

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

## TASK-015 — Create Sales Agent Model

**Priority:** P1

Create:

```text
sales_agents
```

Include:

```text
id
name
email
phone
role
active
created_at
```

---

## TASK-016 — Create Lead Event Model

**Priority:** P1

Create an event/audit model.

Examples:

```text
lead.created
lead.updated
lead.message_received
lead.qualified
lead.assigned
lead.status_changed
follow_up.created
follow_up.completed
```

---

# 8. Phase 3 — Backend Schemas

## TASK-017 — Create Customer Schemas

Create Pydantic schemas for:

```text
CustomerCreate
CustomerUpdate
CustomerResponse
```

---

## TASK-018 — Create Lead Schemas

Create:

```text
LeadCreate
LeadUpdate
LeadResponse
LeadQualificationResponse
```

Validate:

```text
budget_min <= budget_max
```

when both values exist.

---

## TASK-019 — Create Chat Schemas

Create request and response schemas.

Example request:

```json
{
  "conversation_id": "conv_123",
  "message": "I need a 3 bedroom apartment in Lekki."
}
```

Example response:

```json
{
  "conversation_id": "conv_123",
  "message": "Great! What is your budget for the property?"
}
```

---

# 9. Phase 4 — Lead API

## TASK-020 — Create Lead Service

Create:

```text
backend/app/services/lead_service.py
```

The service should handle:

- Creating leads
- Updating leads
- Retrieving leads
- Lead status changes
- Customer association
- Agent assignment

Business logic belongs here rather than inside route handlers.

---

## TASK-021 — Create Lead Endpoint

Create:

```text
POST /api/v1/leads
```

The endpoint should:

```text
Request
 ↓
Validate
 ↓
Service
 ↓
Database
 ↓
Response
```

---

## TASK-022 — Create Lead List Endpoint

Create:

```text
GET /api/v1/leads
```

Support:

- Pagination
- Status filtering
- Intent filtering
- Location filtering
- Qualification filtering
- Sorting

---

## TASK-023 — Create Lead Detail Endpoint

Create:

```text
GET /api/v1/leads/{lead_id}
```

Return lead information.

Do not expose sensitive internal information to customer-facing clients.

---

## TASK-024 — Create Lead Update Endpoint

Create:

```text
PATCH /api/v1/leads/{lead_id}
```

Allow controlled updates.

Validate status transitions.

---

## TASK-025 — Create Lead Qualification Endpoint

Create:

```text
POST /api/v1/leads/{lead_id}/qualify
```

The endpoint should use deterministic backend business rules.

The AI may provide information.

The backend owns the final qualification score.

---

# 10. Phase 5 — Chat Backend

## TASK-026 — Create Chat Service

Create:

```text
backend/app/services/chat_service.py
```

Responsibilities:

- Receive customer message
- Validate message
- Find/create conversation
- Save message
- Trigger processing
- Return customer-safe response

---

## TASK-027 — Create Chat Endpoint

Create:

```text
POST /api/v1/chat
```

Flow:

```text
React
 ↓
FastAPI
 ↓
Validate message
 ↓
Save message
 ↓
Trigger n8n
 ↓
AI processing
 ↓
Validate AI response
 ↓
Update lead
 ↓
Generate response
 ↓
Return response
```

---

# 11. Phase 6 — React Frontend

## TASK-028 — Initialize React Application

Create the React frontend.

Expected structure:

```text
frontend/
└── src/
    ├── components/
    ├── pages/
    ├── services/
    ├── hooks/
    └── App.jsx
```

---

## TASK-029 — Create Home Page

Create a simple landing page for PrimeHomes Realty.

Purpose:

```text
Introduce service
 ↓
Invite customer to start conversation
```

---

## TASK-030 — Create Chat Window

Create:

```text
ChatWindow
MessageList
MessageBubble
ChatInput
TypingIndicator
```

The UI should be simple and mobile-friendly.

---

## TASK-031 — Connect React to FastAPI

Create:

```text
frontend/src/services/api.js
```

All backend requests should pass through the API service layer.

Do NOT put API requests randomly inside UI components.

---

## TASK-032 — Implement Chat State

Track:

```text
conversation_id
messages
loading
error
```

Message states:

```text
SENDING
SENT
FAILED
```

---

## TASK-033 — Add Error Handling

Display customer-friendly errors.

Do not expose:

```text
stack traces
database errors
API keys
internal workflow information
AI provider errors
```

---

## TASK-034 — Create Contact Form

Collect:

```text
name
email
phone
```

Validate fields before submission.

---

## TASK-035 — Create Lead Confirmation

After sufficient information is collected, show:

```text
Lead received
Requirements summary
Next step
```

Do not display internal qualification scores.

---

# 12. Phase 7 — n8n Integration

## TASK-036 — Create n8n Lead Intake Workflow

Workflow name:

```text
RE-LEAD-01 Lead Intake
```

Trigger:

```text
FastAPI Webhook
```

Expected flow:

```text
Webhook
 ↓
Validate
 ↓
Check Duplicate
 ↓
Load Context
 ↓
AI Processing
```

---

## TASK-037 — Create n8n AI Processing Workflow

Workflow:

```text
RE-LEAD-02 AI Processing
```

Flow:

```text
Receive Message
 ↓
Prepare Context
 ↓
Call Gemini
 ↓
Parse Structured Output
 ↓
Validate Output
 ↓
Return Result
```

---

## TASK-038 — Validate AI Output

AI output must never be trusted automatically.

Validation:

```text
AI Output
 ↓
Schema Validation
 ↓
Business Validation
 ↓
Normalization
 ↓
Database
```

If validation fails:

```text
AI Output
 ↓
Validation Failed
 ↓
Retry / Error Handling
```

---

# 13. Phase 8 — AI Processing

## TASK-039 — Implement Intent Detection

Supported intents:

```text
BUY
RENT
SELL
LAND
PROPERTY_ENQUIRY
UNKNOWN
```

Example:

```text
"I want to rent an apartment"
```

Expected:

```json
{
  "intent": "RENT"
}
```

---

## TASK-040 — Implement Requirement Extraction

Extract:

```text
property_type
bedrooms
location
budget
timeline
intent
```

Example:

```text
"I need a 3-bedroom apartment in Lekki for ₦80 million."
```

Expected:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_max": 80000000,
  "currency": "NGN"
}
```

---

## TASK-041 — Implement Missing Field Detection

The AI must identify missing information.

Example:

```text
"I want to buy a house in Lekki."
```

Possible missing fields:

```text
budget
bedrooms
timeline
```

The AI should ask for missing information rather than inventing it.

---

## TASK-042 — Implement Normalization

Normalize:

```text
3 bedroom
three bedroom
3BR
```

to:

```text
3
```

Normalize:

```text
80m
80 million
₦80m
```

to:

```text
80000000 NGN
```

when the meaning is clear.

---

## TASK-043 — Implement Customer Response Generation

AI should generate helpful responses based on:

- Known requirements
- Missing requirements
- Conversation history
- Business rules

The response should be:

- Professional
- Concise
- Helpful
- Customer-friendly

---

## TASK-044 — Implement AI Confidence

Track confidence for extracted information.

Low confidence should trigger:

```text
Clarification
```

or:

```text
Human Escalation
```

---

# 14. Phase 9 — Lead Qualification

## TASK-045 — Implement Qualification Rules

Create deterministic qualification logic.

Possible factors:

```text
Budget
Timeline
Property requirements completeness
Intent
Contact information
Customer engagement
```

Example classification:

```text
90–100 → HOT
70–89  → WARM
0–69   → COLD
```

These thresholds remain configurable.

---

## TASK-046 — Store Qualification

Save:

```text
score
classification
reasons
missing_fields
confidence
qualified_at
```

---

## TASK-047 — Assign Qualified Leads

Example:

```text
HOT
 ↓
Immediate sales assignment

WARM
 ↓
Standard sales queue

COLD
 ↓
Nurture queue
```

---

# 15. Phase 10 — Sales Notifications

## TASK-048 — Create Sales Notification Workflow

n8n workflow:

```text
RE-LEAD-03 Sales Notification
```

Trigger:

```text
lead.qualified
```

---

## TASK-049 — Implement HOT Lead Alert

When:

```text
classification = HOT
```

notify sales team.

Notification should contain:

```text
Lead name
Intent
Property requirements
Location
Budget
Timeline
Contact information
Lead ID
```

Do not expose unnecessary AI/internal data.

---

# 16. Phase 11 — Google Sheets

## TASK-050 — Create Operational Lead Sheet

Google Sheets should provide an operational/reporting view.

Suggested columns:

```text
Lead ID
Customer Name
Email
Phone
Intent
Property Type
Bedrooms
Location
Budget
Currency
Timeline
Lead Status
Qualification
Assigned Agent
Created At
Updated At
```

---

## TASK-051 — Build SQL → n8n → Google Sheets Sync

Flow:

```text
PostgreSQL
 ↓
n8n
 ↓
Google Sheets
```

SQL remains authoritative.

Google Sheets must not silently overwrite the database.

---

## TASK-052 — Prevent Duplicate Sheet Records

Use:

```text
Lead ID
```

as the unique reference.

If Lead ID exists:

```text
UPDATE
```

Otherwise:

```text
CREATE
```

---

# 17. Phase 12 — Follow-Up Automation

## TASK-053 — Create Follow-Up Workflow

Workflow:

```text
RE-LEAD-04 Follow-Up Automation
```

Responsibilities:

- Schedule follow-up
- Check due follow-ups
- Notify sales agent
- Record completion
- Escalate overdue follow-ups

---

## TASK-054 — Implement Follow-Up Status

Supported states:

```text
PENDING
COMPLETED
CANCELLED
```

---

## TASK-055 — Implement Follow-Up Reminders

Example:

```text
Follow-up due
 ↓
Reminder
 ↓
Agent completes
```

If overdue:

```text
Overdue
 ↓
Escalation
```

Maximum reminder attempts should be configurable.

---

# 18. Phase 13 — Error Handling

## TASK-056 — Create n8n Error Workflow

Workflow:

```text
RE-LEAD-99 Error Handler
```

Capture:

```text
request_id
lead_id
conversation_id
message_id
workflow_execution_id
error
timestamp
```

---

## TASK-057 — Implement Retry Rules

Retry only failures that are likely temporary.

Examples:

```text
Network timeout
Temporary API failure
Rate limit
Temporary service unavailable
```

Do not endlessly retry:

```text
Invalid customer input
Invalid AI output
Invalid database data
Authentication failure
```

---

# 19. Phase 14 — Testing

## TASK-058 — Backend Unit Tests

Test:

- Validation
- Lead creation
- Lead updates
- Status transitions
- Qualification
- Budget validation
- Missing fields

---

## TASK-059 — API Tests

Test:

```text
POST /leads
GET /leads
GET /leads/{id}
PATCH /leads/{id}
POST /leads/{id}/qualify
POST /chat
GET /health
```

---

## TASK-060 — AI Evaluation Tests

Create test cases for:

```text
Intent detection
Requirement extraction
Missing information
Normalization
Conversation context
Hallucination prevention
Prompt injection
Low confidence
Structured output
```

---

## TASK-061 — n8n Workflow Tests

Test:

```text
Lead Intake
AI Processing
Qualification
Notifications
Google Sheets
Follow-Up
Error Handling
```

---

## TASK-062 — End-to-End Test

Test complete journey:

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

The entire flow must work before MVP is considered complete.

---

# 20. Phase 15 — MVP Acceptance Test

The MVP should successfully handle this scenario:

### Customer

```text
Hi, I'm looking for a 3-bedroom apartment around Lekki.
My budget is around ₦80 million.
```

### System should:

```text
1. Receive message
2. Create/find customer
3. Create conversation
4. Save message
5. Identify BUY intent
6. Extract apartment
7. Extract 3 bedrooms
8. Extract Lekki
9. Extract ₦80 million
10. Identify missing information
11. Ask an appropriate question
12. Store structured requirements
13. Continue conversation
14. Qualify lead when enough information exists
15. Save qualification
16. Assign/route lead
17. Notify sales team if required
18. Sync operational data to Google Sheets
19. Maintain conversation history
```

---

# 21. AI Coding Assistant Rules

An AI coding assistant must follow these rules.

## Rule 1 — Read Before Coding

Before modifying code, read the relevant:

```text
PRD.md
SYSTEM_ARCHITECTURE.md
TECHNICAL_SPEC.md
API_SPEC.md
DATA_MODEL.md
AI_AGENT_SPEC.md
N8N_WORKFLOW_SPEC.md
UI_UX_SPEC.md
TESTING_STRATEGY.md
IMPLEMENTATION_PLAN.md
DEVELOPMENT_WORKFLOW.md
BUILD_TASKS.md
```

Only read the documents relevant to the task when the project becomes large.

---

## Rule 2 — Do Not Invent Requirements

If a requirement is not documented:

```text
Do not invent it.
```

Instead:

```text
Identify the ambiguity.
Use the smallest safe assumption.
Document the assumption.
```

---

## Rule 3 — Respect Architecture Boundaries

### React

Owns:

```text
UI
UX
Customer interaction
```

### FastAPI

Owns:

```text
API
Validation
Business logic
Database access
```

### PostgreSQL

Owns:

```text
Primary application data
```

### n8n

Owns:

```text
Workflow orchestration
Integrations
Notifications
Scheduled automation
AI orchestration
```

### AI

Owns:

```text
Natural-language understanding
Extraction
Classification
Response generation
```

### Google Sheets

Owns:

```text
Operational reporting
Secondary business visibility
```

---

## Rule 4 — No Direct React → Database

Never implement:

```text
React → PostgreSQL
```

Correct:

```text
React
 ↓
FastAPI
 ↓
PostgreSQL
```

---

## Rule 5 — No Direct AI → Database

AI must never directly modify the database.

Correct:

```text
AI
 ↓
Structured Output
 ↓
Validation
 ↓
Business Logic
 ↓
Database
```

---

## Rule 6 — Test Changes

Every meaningful implementation change should include appropriate tests.

Do not consider code complete merely because:

```text
"It runs."
```

The feature must also behave correctly.

---

# 22. Task Completion Checklist

Before marking a task `DONE`:

```text
[ ] Requirement understood
[ ] Correct documentation reviewed
[ ] Dependencies satisfied
[ ] Code implemented
[ ] Tests written/updated
[ ] Tests pass
[ ] Error handling considered
[ ] Security boundaries respected
[ ] No secrets committed
[ ] Documentation updated if necessary
[ ] Code reviewed
[ ] Git commit created
```

---

# 23. Standard AI Coding Task Prompt

When giving a task to an AI coding assistant, use:

```text
TASK:
Implement TASK-XXX.

OBJECTIVE:
Explain what needs to be built.

RELEVANT DOCUMENTS:
- docs/...
- docs/...

FILES TO MODIFY:
- ...

FILES NOT TO MODIFY:
- ...

REQUIREMENTS:
- ...
- ...
- ...

DEPENDENCIES:
- ...

ACCEPTANCE CRITERIA:
- ...
- ...
- ...

TESTING:
- Add/update tests for ...
- Run relevant tests.

CONSTRAINTS:
- Do not invent requirements.
- Do not change the architecture.
- Do not modify unrelated files.
- Do not expose secrets.
- Follow existing project conventions.

DELIVERABLE:
Provide the implementation and tests.
Summarize what changed and any assumptions made.
```

---

# 24. Recommended First Coding Tasks

Do not start by building the AI agent.

Start here:

```text
TASK-001
Create Project Structure

        ↓

TASK-002
Initialize Git

        ↓

TASK-003
Environment Configuration

        ↓

TASK-004
FastAPI Application

        ↓

TASK-005
Health Endpoint

        ↓

TASK-006
Application Settings

        ↓

TASK-007
PostgreSQL

        ↓

TASK-008
Database Connection

        ↓

TASK-009
Customer Model

        ↓

TASK-010
Lead Model
```

After the backend foundation is stable:

```text
Database
 ↓
API
 ↓
React
 ↓
n8n
 ↓
AI
 ↓
Qualification
 ↓
Notifications
 ↓
Google Sheets
 ↓
Follow-Up
```

---

# 25. Definition of MVP Complete

The Real Estate Lead Bot MVP is complete when:

```text
Customer
    ↓
React Chat
    ↓
FastAPI
    ↓
n8n
    ↓
Gemini
    ↓
Structured AI Output
    ↓
Validation
    ↓
PostgreSQL
    ↓
Lead Qualification
    ↓
Sales Notification
    ↓
Google Sheets
```

works reliably for the primary customer journeys defined in the PRD.

The MVP must:

- Capture customer messages.
- Understand customer intent.
- Extract property requirements.
- Detect missing information.
- Ask clarifying questions.
- Store structured lead information.
- Qualify leads.
- Notify the appropriate sales workflow.
- Maintain conversation history.
- Handle errors.
- Prevent duplicate processing.
- Keep AI output validated.
- Pass the required tests.

---

# 26. Final Development Principle

The objective is not to build the most complicated system.

The objective is to build a:

```text
Simple
+
Reliable
+
Testable
+
Maintainable
+
Documented
+
Business-useful
```

system.

Build one task at a time.

Do not allow AI coding assistants to turn a small task into an uncontrolled rewrite of the project.

**Small task → small change → test → review → commit → next task.**