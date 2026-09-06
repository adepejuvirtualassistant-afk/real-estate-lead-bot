# IMPLEMENTATION PLAN

## 1. Document Purpose

This document converts the product and technical specifications for the **PrimeHomes Realty Real Estate Lead Bot** into a practical implementation sequence.

The project contains multiple layers:

```text
React
  ↓
FastAPI
  ↓
n8n
  ↓
AI
  ↓
SQL Database
  ↓
Notifications / Google Sheets / Follow-ups
```

Because these components depend on one another, development must happen in a controlled order.

The goal of this document is to define:

- What should be built first
- What depends on what
- Which components should be developed independently
- When components should be integrated
- What should be tested at each stage
- What constitutes completion for each phase
- How an AI coding assistant should implement the system safely

---

# 2. Implementation Philosophy

The project should be built incrementally.

Do not attempt to build the complete system in one prompt or one coding session.

Use this approach:

```text
Plan
 ↓
Build Small Component
 ↓
Test
 ↓
Integrate
 ↓
Test Again
 ↓
Add Next Component
```

The system should become progressively more functional.

At every stage, there should be a working version.

---

# 3. Development Order

The recommended development order is:

```text
PHASE 0
Project Setup
      ↓
PHASE 1
Backend Foundation
      ↓
PHASE 2
Database
      ↓
PHASE 3
API
      ↓
PHASE 4
Frontend
      ↓
PHASE 5
n8n Integration
      ↓
PHASE 6
AI Processing
      ↓
PHASE 7
Lead Qualification
      ↓
PHASE 8
Notifications & Follow-up
      ↓
PHASE 9
Google Sheets Integration
      ↓
PHASE 10
End-to-End Testing
      ↓
PHASE 11
Optimization & Documentation
```

This sequence minimizes unnecessary rework.

---

# 4. Phase 0 — Project Setup

## Objective

Create the project structure and development environment.

## Tasks

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

The `docs/` directory already contains the product specifications.

Required documentation:

```text
docs/
├── PRD.md
├── SYSTEM_ARCHITECTURE.md
├── TECHNICAL_SPEC.md
├── API_SPEC.md
├── DATA_MODEL.md
├── AI_AGENT_SPEC.md
├── N8N_WORKFLOW_SPEC.md
├── UI_UX_SPEC.md
├── TESTING_STRATEGY.md
└── IMPLEMENTATION_PLAN.md
```

Do not create `SECURITY_SPEC.md` unless the project requirements are changed later.

---

# 5. Phase 0 Environment Setup

Confirm the development environment contains the required tools.

Expected technologies:

```text
Python
FastAPI
React
Node.js
n8n
PostgreSQL
Git
```

AI provider:

```text
Google Gemini
```

where appropriate for the project implementation.

n8n will initially run locally during development.

---

# 6. Phase 0 Definition of Done

The phase is complete when:

- Project folders exist
- Git repository is initialized
- Backend environment works
- React environment works
- n8n is accessible
- Database development environment is available
- Environment variables are configured
- Documentation is present
- Basic README exists

---

# 7. Phase 1 — Backend Foundation

## Objective

Create the FastAPI application structure.

Recommended structure:

```text
backend/
└── app/
    ├── main.py
    │
    ├── api/
    │   └── v1/
    │       ├── leads.py
    │       ├── chat.py
    │       ├── customers.py
    │       └── health.py
    │
    ├── models/
    │
    ├── schemas/
    │   ├── lead.py
    │   ├── customer.py
    │   ├── conversation.py
    │   ├── message.py
    │   └── follow_up.py
    │
    ├── services/
    │   ├── lead_service.py
    │   ├── qualification_service.py
    │   └── chat_service.py
    │
    ├── db/
    │   ├── database.py
    │   └── session.py
    │
    └── core/
        ├── config.py
        └── errors.py
```

The exact structure may evolve during implementation.

---

# 8. Backend First Endpoint

Create:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

This gives us the simplest possible way to verify that FastAPI is running.

---

# 9. Backend Definition of Done

The backend foundation is complete when:

- FastAPI starts successfully
- `/health` works
- API versioning structure exists
- Configuration system exists
- Database connection layer exists
- Pydantic schemas can be created
- Basic error handling exists
- Unit tests run successfully

---

# 10. Phase 2 — Database

## Objective

Implement the SQL database defined in `DATA_MODEL.md`.

Recommended production database:

```text
PostgreSQL
```

Core tables:

```text
customers
leads
conversations
messages
lead_qualifications
follow_ups
sales_agents
lead_events
```

---

# 11. Database Implementation Order

Create tables in dependency order.

```text
customers
    ↓
sales_agents
    ↓
leads
    ↓
conversations
    ↓
messages
    ↓
lead_qualifications
    ↓
follow_ups
    ↓
lead_events
```

Foreign-key relationships must be respected.

---

# 12. Database Migration Strategy

Database changes should use migrations.

Do not manually modify production database structures.

Every schema change should be represented as a migration.

Example:

```text
Migration 001
Create customers

Migration 002
Create leads

Migration 003
Create conversations

Migration 004
Create messages
```

The exact migration tool will be selected during backend implementation.

---

# 13. Database Definition of Done

Verify:

- Tables exist
- Relationships work
- Foreign keys work
- Constraints work
- UUIDs work
- Timestamps work
- Status values are controlled
- Duplicate records are prevented where required
- Database tests pass

---

# 14. Phase 3 — Core API

## Objective

Implement the API contract defined in `API_SPEC.md`.

First implement:

```text
POST /api/v1/leads
GET /api/v1/leads
GET /api/v1/leads/{lead_id}
PATCH /api/v1/leads/{lead_id}
```

Then:

```text
POST /api/v1/leads/{lead_id}/qualify
```

Then:

```text
POST /api/v1/chat
```

---

# 15. Create Lead Flow

Initial flow:

```text
Request
  ↓
Pydantic Validation
  ↓
Business Validation
  ↓
Database
  ↓
Response
```

Do not introduce AI or n8n yet.

The first goal is to prove that the backend can reliably create and retrieve leads.

---

# 16. API Definition of Done

The API phase is complete when:

- Lead can be created
- Lead can be retrieved
- Lead can be updated
- Validation works
- Errors are predictable
- Database persistence works
- API tests pass
- OpenAPI documentation is generated
- Idempotency behavior is implemented where required

---

# 17. Phase 4 — React Frontend

## Objective

Build the customer-facing interface.

Initial structure:

```text
frontend/
└── src/
    ├── components/
    │   ├── ChatWindow
    │   ├── MessageList
    │   ├── MessageBubble
    │   ├── ChatInput
    │   ├── TypingIndicator
    │   ├── ContactForm
    │   ├── LeadSummary
    │   └── ErrorMessage
    │
    ├── pages/
    │   ├── Home
    │   ├── Chat
    │   └── Confirmation
    │
    ├── services/
    │   └── api.js
    │
    ├── hooks/
    │   └── useChat.js
    │
    └── App.jsx
```

---

# 18. Frontend Development Order

Build:

### Step 1

Basic page layout.

### Step 2

Chat interface.

### Step 3

Message display.

### Step 4

Message input.

### Step 5

Loading state.

### Step 6

Error state.

### Step 7

FastAPI connection.

### Step 8

Contact form.

### Step 9

Confirmation screen.

---

# 19. Frontend Definition of Done

The customer should be able to:

```text
Open application
      ↓
Start conversation
      ↓
Enter message
      ↓
Send message
      ↓
See loading state
      ↓
Receive API response
      ↓
Continue conversation
```

The frontend should not connect directly to:

```text
SQL
n8n
AI provider
Google Sheets
```

All communication should go through the appropriate backend boundary.

---

# 20. Phase 5 — n8n Integration

## Objective

Connect FastAPI to n8n.

Initial architecture:

```text
React
 ↓
FastAPI
 ↓
n8n Webhook
```

Create the Lead Intake workflow.

Example:

```text
Webhook
 ↓
Validate Input
 ↓
Load Context
 ↓
Process
```

Initially, the workflow can return a test response.

---

# 21. n8n Integration Milestone

Before introducing AI, verify:

```text
React
 ↓
FastAPI
 ↓
n8n
 ↓
FastAPI
 ↓
React
```

This proves the communication pipeline works.

Only after this works should AI processing be added.

---

# 22. n8n Definition of Done

Verify:

- FastAPI can trigger n8n
- n8n receives correct payload
- Request IDs are preserved
- Message IDs are preserved
- Conversation IDs are preserved
- Duplicate messages are handled
- Workflow execution can be inspected
- Errors are captured

---

# 23. Phase 6 — AI Processing

## Objective

Add AI-powered natural-language understanding.

AI responsibilities:

```text
Message
 ↓
Intent Detection
 ↓
Requirement Extraction
 ↓
Missing Fields
 ↓
Normalization
 ↓
Customer Response
```

The AI should return structured output.

---

# 24. AI Integration Order

Implement AI features incrementally.

### Step 1

Intent classification.

### Step 2

Property requirement extraction.

### Step 3

Missing-field detection.

### Step 4

Normalization.

### Step 5

Customer response generation.

### Step 6

Confidence handling.

### Step 7

Human escalation.

Do not implement everything in one AI prompt initially.

---

# 25. AI Validation Boundary

The system must follow:

```text
Customer Message
      ↓
AI
      ↓
Structured Output
      ↓
Schema Validation
      ↓
Business Validation
      ↓
Normalization
      ↓
Database
```

AI must never directly write unrestricted data into the database.

---

# 26. AI Definition of Done

The AI can:

- Identify supported intents
- Extract property requirements
- Identify missing fields
- Normalize common expressions
- Generate appropriate clarification questions
- Generate customer responses
- Return valid structured output
- Handle low-confidence cases
- Avoid inventing property information
- Escalate when required

AI evaluation tests must pass before moving forward.

---

# 27. Phase 7 — Lead Qualification

## Objective

Implement deterministic lead qualification.

Example:

```text
Lead Information
      ↓
Business Rules
      ↓
Score
      ↓
HOT / WARM / COLD
```

The AI may help provide context, but the official score should be calculated using backend-controlled rules.

---

# 28. Qualification Implementation

Example factors:

```text
Purchase intent
Budget
Timeline
Location specificity
Requirement completeness
```

Example conceptual scoring:

```text
Intent            +20
Budget            +20
Location          +20
Timeline          +20
Complete details  +20
----------------------
Maximum           100
```

The exact weights can be changed according to business requirements.

---

# 29. Qualification Definition of Done

Verify:

- Score is between 0–100
- HOT/WARM/COLD classification works
- Missing fields affect qualification appropriately
- Rules are deterministic
- Tests cover boundary values
- Qualification is persisted
- Qualification events are recorded

---

# 30. Phase 8 — Sales Notifications

## Objective

Notify the sales team when important leads are ready for follow-up.

Example:

```text
Lead Qualified
      ↓
Classification
      ↓
HOT?
  ↙       ↘
YES       NO
 ↓         ↓
Alert    Standard
Sales    Follow-up
```

Possible integrations:

```text
Slack
Email
```

The exact notification provider can be finalized during implementation.

---

# 31. Sales Notification Definition of Done

For a HOT lead:

- Lead is qualified
- Sales notification is triggered
- Notification contains useful lead information
- Internal information is not exposed to customer
- Duplicate notifications are prevented

---

# 32. Phase 9 — Follow-Up Automation

## Objective

Automatically create and manage follow-up actions.

Example:

```text
Lead Qualified
      ↓
Create Follow-up
      ↓
Schedule
      ↓
Reminder
      ↓
Sales Contact
      ↓
Completed
```

Possible follow-up types:

```text
Call
Email
WhatsApp
Property Viewing
General Follow-up
```

---

# 33. Follow-Up Definition of Done

Verify:

- Follow-up is created
- Correct lead is associated
- Due date is correct
- Reminder works
- Completion works
- Cancellation works
- Duplicate follow-ups are prevented
- Failed automation is retried appropriately

---

# 34. Phase 10 — Google Sheets Integration

## Objective

Synchronize operational lead information with Google Sheets.

Architecture:

```text
SQL Database
      ↓
n8n
      ↓
Google Sheets
```

SQL remains the authoritative source.

Google Sheets is used for:

- Operational visibility
- Reporting
- Sales team convenience
- Lightweight analysis

---

# 35. Google Sheets Definition of Done

Verify:

- New lead appears
- Updates synchronize
- Lead ID is preserved
- Duplicate rows are prevented
- Field mappings are correct
- API failures are handled
- SQL remains authoritative

---

# 36. Phase 11 — Complete End-to-End Integration

At this point, connect the complete system.

```text
Customer
   ↓
React
   ↓
FastAPI
   ↓
n8n
   ↓
AI
   ↓
Validation
   ↓
SQL
   ↓
Qualification
   ↓
Sales Notification
   ↓
Google Sheets
   ↓
Follow-up
```

---

# 37. First Complete Customer Journey

Test:

> "Hi, I'm looking for a 3-bedroom apartment in Lekki. My budget is ₦80 million and I want to buy immediately."

Expected:

```text
Message received
       ↓
AI identifies BUY
       ↓
Apartment
       ↓
3 bedrooms
       ↓
Lekki
       ↓
₦80M
       ↓
Immediate
       ↓
Lead saved
       ↓
Lead qualified
       ↓
Sales notified
       ↓
Follow-up created
       ↓
Google Sheets updated
       ↓
Customer receives response
```

This becomes one of the primary E2E tests.

---

# 38. Phase 12 — Testing

Run the complete testing strategy defined in `TESTING_STRATEGY.md`.

Test:

```text
Unit
 ↓
Integration
 ↓
API
 ↓
Database
 ↓
n8n
 ↓
AI
 ↓
E2E
 ↓
UAT
```

---

# 39. Failure Testing

Do not only test successful scenarios.

Test:

```text
AI unavailable
Database unavailable
n8n unavailable
Google Sheets unavailable
Invalid API request
Duplicate webhook
Malformed AI output
Network timeout
Notification failure
Missing customer information
```

The system should fail safely.

---

# 40. Phase 13 — Optimization

After functionality is stable, improve:

- Performance
- Error handling
- User experience
- AI prompts
- AI accuracy
- Database queries
- n8n workflows
- Logging
- Monitoring
- Documentation

Do not optimize prematurely.

First:

> **Make it work.**

Then:

> **Make it reliable.**

Then:

> **Make it efficient.**

---

# 41. Development Milestones

The project should use clear milestones.

## Milestone 1 — Foundation

```text
Project
Backend
Database
Documentation
```

## Milestone 2 — API

```text
FastAPI
CRUD
Validation
Database persistence
```

## Milestone 3 — Frontend

```text
React
Chat
Forms
API integration
```

## Milestone 4 — Automation

```text
FastAPI
 ↓
n8n
```

## Milestone 5 — AI

```text
AI extraction
AI classification
AI responses
```

## Milestone 6 — Business Logic

```text
Qualification
Sales alerts
Follow-ups
```

## Milestone 7 — Integrations

```text
Google Sheets
Notifications
```

## Milestone 8 — Production Readiness

```text
Testing
Error handling
Performance
Documentation
```

---

# 42. Dependency Map

The following dependencies must be respected:

```text
Project Setup
     ↓
Backend Foundation
     ↓
Database
     ↓
API
     ↓
Frontend API Integration
     ↓
n8n Integration
     ↓
AI
     ↓
Qualification
     ↓
Notifications
     ↓
Follow-ups
     ↓
Google Sheets
     ↓
E2E Testing
```

Some work can happen in parallel once the required contracts are stable.

For example:

```text
Backend ──────────────┐
                      ├── Integration
Frontend ─────────────┤
                      │
Database ─────────────┘
```

---

# 43. Parallel Development

Once API contracts are defined, frontend and backend development can proceed in parallel.

```text
             API_SPEC
                ↓
        ┌───────┴───────┐
        ↓               ↓
     React           FastAPI
        ↓               ↓
        └───────┬───────┘
                ↓
           Integration
```

This is one reason the API specification was created before implementation.

---

# 44. Git Strategy

Use Git for version control.

Recommended branches:

```text
main
develop
feature/*
```

Example:

```text
feature/backend-leads
feature/react-chat
feature/n8n-intake
feature/ai-extraction
feature/lead-qualification
```

The exact branching strategy can remain simple for a small project.

---

# 45. Commit Strategy

Commits should represent logical changes.

Good:

```text
feat: add lead creation endpoint
```

```text
feat: add customer chat interface
```

```text
feat: add AI requirement extraction
```

```text
test: add lead qualification tests
```

```text
fix: prevent duplicate webhook processing
```

Avoid large commits containing unrelated changes.

---

# 46. Environment Variables

Environment-specific configuration must not be hardcoded.

Examples:

```text
DATABASE_URL
AI_API_KEY
N8N_WEBHOOK_URL
N8N_API_KEY
GOOGLE_SHEETS_ID
NOTIFICATION_API_KEY
```

Frontend configuration may include:

```text
VITE_API_BASE_URL
```

Secrets must remain server-side.

---

# 47. Configuration Principle

Use:

```text
Environment Variables
        ↓
Application Configuration
        ↓
Services
```

Not:

```text
Hardcoded Secrets
        ↓
Source Code
```

The frontend must never contain private API credentials.

---

# 48. Agentic AI Development Workflow

When using an AI coding assistant, work in small tasks.

Do not ask:

> "Build the entire real estate lead bot."

Instead use tasks such as:

```text
Task 1:
Create FastAPI project structure.

Task 2:
Implement database connection.

Task 3:
Create Customer model.

Task 4:
Create Lead model.

Task 5:
Create POST /api/v1/leads.

Task 6:
Write tests for lead creation.

Task 7:
Build React chat interface.

Task 8:
Connect React to /api/v1/chat.
```

This makes the AI coding assistant easier to control and review.

---

# 49. AI Coding Assistant Rules

The coding assistant must:

1. Read relevant documentation before coding.
2. Follow the architecture.
3. Respect API contracts.
4. Respect database models.
5. Never invent undocumented requirements.
6. Ask before making major architectural changes.
7. Make small changes.
8. Run tests after changes.
9. Fix root causes rather than hiding errors.
10. Update documentation when architecture changes.
11. Never expose secrets.
12. Never use production customer data for testing.
13. Preserve existing working functionality.
14. Explain significant architectural decisions.
15. Keep code maintainable.

---

# 50. Change Control

When a requirement changes:

```text
Requirement Change
       ↓
PRD
       ↓
Affected Specifications
       ↓
Implementation
       ↓
Tests
       ↓
Documentation
```

For example, if PrimeHomes changes the lead status model:

```text
PRD
 ↓
DATA_MODEL
 ↓
API_SPEC
 ↓
N8N_WORKFLOW_SPEC
 ↓
Backend
 ↓
Frontend
 ↓
Tests
```

Do not change only the code.

---

# 51. Definition of Done for the Entire Product

The Real Estate Lead Bot is considered complete when:

### Product

- Customer can submit property requirements
- Customer can have a conversation with the bot
- Customer can provide contact information
- Customer receives appropriate responses

### Backend

- FastAPI APIs work
- Validation works
- Business rules work
- Database persistence works

### AI

- Requirements are extracted
- Intent is identified
- Missing information is detected
- Responses are generated
- Hallucination controls work
- Structured output is validated

### Automation

- n8n workflows execute correctly
- Lead qualification works
- Sales notifications work
- Follow-ups work
- Errors are handled

### Database

- Data is stored correctly
- Relationships work
- Constraints work
- Duplicate processing is prevented

### Integrations

- Google Sheets synchronization works
- Notification integration works

### Testing

- Unit tests pass
- Integration tests pass
- API tests pass
- AI evaluations pass
- Workflow tests pass
- E2E tests pass
- UAT passes

### Documentation

- Architecture reflects implementation
- API documentation is current
- Data model is current
- AI behavior is documented
- n8n workflows are documented
- Testing strategy is current
- README explains how to run the project

---

# 52. Recommended Build Sequence

The actual implementation should follow this sequence:

```text
STEP 1
Create project repository
        ↓
STEP 2
Set up FastAPI
        ↓
STEP 3
Set up PostgreSQL
        ↓
STEP 4
Create database models
        ↓
STEP 5
Create migrations
        ↓
STEP 6
Implement Lead API
        ↓
STEP 7
Write backend tests
        ↓
STEP 8
Create React application
        ↓
STEP 9
Build chat UI
        ↓
STEP 10
Connect React → FastAPI
        ↓
STEP 11
Create n8n Lead Intake workflow
        ↓
STEP 12
Connect FastAPI → n8n
        ↓
STEP 13
Implement AI extraction
        ↓
STEP 14
Validate AI output
        ↓
STEP 15
Implement qualification
        ↓
STEP 16
Implement notifications
        ↓
STEP 17
Implement follow-ups
        ↓
STEP 18
Implement Google Sheets sync
        ↓
STEP 19
Run complete E2E tests
        ↓
STEP 20
Fix bugs
        ↓
STEP 21
Optimize
        ↓
STEP 22
Finalize documentation
```

---

# 53. Final Implementation Principle

The project should be built as a **real software system**, not as one giant automation workflow.

The architecture should remain:

```text
React
  ↓
FastAPI
  ↓
n8n
  ↓
AI + Integrations
  ↓
SQL
```

Each component has a clear responsibility.

```text
React
→ User experience

FastAPI
→ API + validation + business logic

SQL
→ Source of truth

n8n
→ Automation + orchestration

AI
→ Natural-language understanding

Integrations
→ Notifications + operational tools
```

The implementation strategy is therefore:

> **Build one reliable layer at a time, test it, then connect it to the next layer.**

The objective is not to produce the most code.

The objective is to produce a system that is:

- Understandable
- Testable
- Reliable
- Maintainable
- Extensible
- Easy for humans and AI coding assistants to work on

**A well-planned implementation is what turns our documentation into a working product.**