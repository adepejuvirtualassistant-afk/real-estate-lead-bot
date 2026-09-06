# Real Estate Lead Bot — System Architecture

**Version:** 1.0  
**Status:** Draft  
**Related Document:** `PRD.md`  
**Product:** PrimeHomes Realty Lead Management System

---

# 1. Architecture Overview

The Real Estate Lead Bot is a multi-layer business application that combines:

- React frontend
- FastAPI backend
- n8n workflow automation
- AI/LLM processing
- SQL database
- Google Sheets
- Sales-team notification and follow-up systems

The architecture is designed around **separation of responsibilities**.

Each technology has a defined role rather than allowing one system to become responsible for everything.

At a high level:

```text
Customer
   │
   ▼
┌──────────────────────┐
│      React UI        │
│  Customer / Sales UI │
└──────────┬───────────┘
           │
           │ HTTPS / JSON
           ▼
┌──────────────────────┐
│      FastAPI         │
│    Backend / API     │
└──────────┬───────────┘
           │
           │ Workflow Event
           ▼
┌──────────────────────┐
│        n8n           │
│ Workflow Orchestrator│
└───────┬──────┬───────┘
        │      │
        │      │
        ▼      ▼
     ┌────┐  ┌──────────────┐
     │ AI │  │ SQL Database │
     └────┘  └──────────────┘
        │
        ▼
┌──────────────────────┐
│ Lead Qualification   │
│ + Business Rules     │
└──────────┬───────────┘
           │
     ┌─────┴───────────┐
     ▼                 ▼
Google Sheets      Notifications
                       │
                       ▼
                  Sales Team
```

---

# 2. Architecture Goals

The architecture should achieve the following:

1. Clear separation of responsibilities.
2. Reliable lead processing.
3. Maintainable code.
4. Controlled AI behavior.
5. Reliable data storage.
6. Easy integration with external services.
7. Human oversight of important decisions.
8. Clear boundaries between frontend, backend, automation and AI.
9. Good observability and error handling.
10. Ability to evolve without rebuilding the entire system.

---

# 3. Architecture Principles

## 3.1 Separation of Concerns

Each layer should have a clearly defined responsibility.

```text
React
→ User interface

FastAPI
→ API + application/backend logic

n8n
→ Workflow orchestration + integrations

AI
→ Natural-language understanding and generation

SQL
→ Persistent system-of-record data

Google Sheets
→ Operational visibility / reporting / selected workflows
```

A component should not take responsibility for another component's entire domain.

---

# 4. System Components

The system consists of the following major components:

```text
1. Customer
2. React Frontend
3. FastAPI Backend
4. n8n Automation Layer
5. AI Processing Layer
6. SQL Database
7. Google Sheets
8. Notification Services
9. Sales Team
```

---

# 5. Component 1 — Customer

The customer is the external user interacting with the real estate company.

The customer may communicate information such as:

```text
"I need a 3-bedroom apartment in Lekki.
My budget is ₦80 million and I want to move within two months."
```

The customer's message begins the lead-processing workflow.

---

# 6. Component 2 — React Frontend

## Responsibility

React is responsible for the presentation layer and user interaction.

The frontend should handle:

- Chat interface.
- Message input.
- Message display.
- Lead forms.
- Loading states.
- Error states.
- Sales dashboard UI.
- Lead list.
- Lead details.
- Lead status updates.

The frontend should not contain critical business rules that need to be trusted.

For example, the frontend should not be responsible for determining whether a lead is officially `HOT`.

That decision belongs to the backend/business-rule layer.

---

# 7. Component 3 — FastAPI Backend

## Responsibility

FastAPI provides the application's backend API layer.

It acts as the controlled interface between the frontend and backend services.

Potential responsibilities include:

- API endpoints.
- Request validation.
- Authentication.
- Authorization.
- Business logic.
- Database access.
- Service coordination.
- Error handling.
- API response formatting.

Example endpoints:

```http
POST /api/chat
POST /api/leads
GET /api/leads
GET /api/leads/{id}
PATCH /api/leads/{id}
```

The exact API contract will be defined in:

```text
docs/API_SPEC.md
```

---

# 8. Component 4 — n8n

## Responsibility

n8n acts as the **workflow orchestration layer**.

n8n coordinates actions between the application, AI services, database, Google Sheets and notification systems.

Example workflow:

```text
Receive Event
     ↓
Validate / Transform
     ↓
AI Processing
     ↓
Validate AI Output
     ↓
Qualification
     ↓
Database Operation
     ↓
Google Sheets Sync
     ↓
Notification
     ↓
Response
```

n8n should be treated as an orchestration engine rather than the entire application.

---

# 9. Component 5 — AI Processing Layer

The AI layer is responsible for tasks requiring natural-language understanding.

Primary responsibilities:

- Intent classification.
- Entity extraction.
- Requirement extraction.
- Natural-language normalization.
- Missing-information detection.
- Response generation.
- Conversation summarization.

Example:

Input:

```text
Hi, I'm looking for a 3-bedroom apartment around Lekki.
My budget is around ₦80 million.
I'd like to move within two months.
```

AI output:

```json
{
  "intent": "buying",
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "currency": "NGN",
  "timeline": "within_3_months"
}
```

The AI output must be treated as **untrusted input until validated**.

---

# 10. Component 6 — SQL Database

The SQL database is the primary **system of record**.

It should store durable application data.

Potential entities include:

```text
Users
Customers
Leads
Conversations
Messages
Property Requirements
Lead Scores
Lead Status History
Follow-Ups
Sales Agents
Audit Records
```

The database provides:

- Persistence.
- Data integrity.
- Relationships.
- Transactions.
- Querying.
- Structured storage.

The detailed database design will be defined in:

```text
docs/DATA_MODEL.md
```

---

# 11. Component 7 — Google Sheets

Google Sheets is not the primary system of record.

It may be used for:

- Sales-team visibility.
- Operational reporting.
- Simple exports.
- n8n demonstrations.
- Temporary operational workflows.
- Lightweight reporting.

Example:

```text
SQL Database
      │
      │ selected lead data
      ▼
Google Sheets
      │
      ▼
Sales Team
```

The system should avoid creating conflicting sources of truth.

If a lead's official status is stored in SQL, Google Sheets should not silently become a second authoritative database.

---

# 12. Component 8 — Notification Services

The notification layer informs sales staff when action is required.

Possible notification channels include:

- Email.
- Slack.
- Google Sheets.
- Future messaging integrations.

Example:

```text
Lead Score = 87
Qualification = HOT
        ↓
n8n
        ↓
Sales Notification
```

---

# 13. Component 9 — Sales Team

The sales team is the human decision-making and follow-up layer.

Sales agents should be able to:

- View leads.
- Review customer requirements.
- See lead scores.
- Review conversation summaries.
- Update lead status.
- Add notes.
- Follow up.
- Record outcomes.

The system should support **human-in-the-loop operations**.

---

# 14. Layered Architecture

The application should follow a layered architecture.

```text
┌─────────────────────────────────────┐
│ Presentation Layer                  │
│ React                               │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ API / Application Layer             │
│ FastAPI                             │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ Workflow / Integration Layer        │
│ n8n                                 │
└───────────┬──────────┬───────────────┘
            │          │
     ┌──────▼─────┐ ┌──▼────────────┐
     │ AI Layer   │ │ Data Layer    │
     │ LLM        │ │ SQL Database  │
     └────────────┘ └───────────────┘
            │
            ▼
     External Services
```

---

# 15. End-to-End Lead Flow

The main workflow begins when a customer sends a message.

## Step 1 — Customer Message

Customer enters:

```text
"I want to buy a 3-bedroom apartment in Lekki.
My budget is ₦80m."
```

---

## Step 2 — React

React sends the message to the backend.

```http
POST /api/chat
```

Example request:

```json
{
  "conversation_id": "conv_123",
  "message": "I want to buy a 3-bedroom apartment in Lekki. My budget is ₦80m."
}
```

---

# 16. Step 3 — FastAPI

FastAPI:

1. Receives the request.
2. Validates the payload.
3. Performs authentication/authorization where required.
4. Creates or identifies the conversation.
5. Passes the appropriate event into the processing workflow.

Conceptually:

```text
React
  ↓
FastAPI
  ↓
Validated Request
```

---

# 17. Step 4 — n8n

n8n receives the workflow event.

It orchestrates the processing pipeline.

```text
n8n
 │
 ├── Validate
 │
 ├── Prepare AI Input
 │
 ├── Call AI
 │
 ├── Validate AI Output
 │
 ├── Qualify Lead
 │
 ├── Store Data
 │
 ├── Notify Sales
 │
 └── Prepare Response
```

---

# 18. Step 5 — AI Processing

The AI receives the customer's message and relevant context.

It attempts to determine:

```text
Intent
Property Type
Location
Budget
Bedrooms
Timeline
Customer Information
```

The AI returns structured output.

Example:

```json
{
  "intent": "buying",
  "property_type": "apartment",
  "location": "Lekki",
  "budget": 80000000,
  "currency": "NGN",
  "bedrooms": 3,
  "timeline": null
}
```

---

# 19. Step 6 — AI Output Validation

AI output must not automatically be trusted.

The system validates:

- Data types.
- Allowed enum values.
- Required fields.
- Numeric values.
- Expected structure.
- Business constraints.

Example:

```text
AI
 ↓
Structured Output
 ↓
Schema Validation
 ↓
Valid?
 ├── YES → Continue
 └── NO  → Retry / Repair / Escalate
```

This protects downstream systems from malformed AI responses.

---

# 20. Step 7 — Missing Information

The system checks whether important information is missing.

Example:

```text
Property Type: ✓
Location: ✓
Budget: ✓
Bedrooms: ✓
Timeline: ✗
```

The system may ask:

```text
"When are you looking to move?"
```

The customer can then provide the missing information.

The system should maintain conversation context so that the new response can be combined with previously collected information.

---

# 21. Step 8 — Lead Creation / Update

Once enough information is available, the system creates or updates the lead.

Conceptually:

```text
Customer Message
       ↓
Lead Identification
       ↓
Existing Lead?
   ┌───┴────┐
   │        │
  YES      NO
   │        │
Update    Create
   │        │
   └───┬────┘
       ▼
   Lead Record
```

---

# 22. Step 9 — Lead Qualification

The lead qualification engine calculates the lead score.

Example:

```text
Budget              +25
Specific Location   +20
Property Type       +15
Short Timeline      +25
Complete Information +10
                    ----
Total                95
```

Example result:

```json
{
  "score": 95,
  "qualification": "HOT"
}
```

The exact scoring rules must be defined separately.

---

# 23. Step 10 — Database Storage

The system stores the lead in SQL.

Example conceptual record:

```text
Lead
├── ID
├── Customer
├── Intent
├── Property Type
├── Location
├── Budget
├── Bedrooms
├── Timeline
├── Score
├── Qualification
├── Status
├── Assigned Agent
├── Created At
└── Updated At
```

---

# 24. Step 11 — Google Sheets Synchronization

Selected lead information can be synchronized to Google Sheets.

Example:

```text
SQL
 │
 ▼
n8n
 │
 ▼
Google Sheets
```

The synchronization should be designed carefully to avoid accidental duplication.

SQL remains the authoritative application database.

---

# 25. Step 12 — Sales Notification

If the lead meets notification criteria:

```text
Qualification = HOT
        ↓
n8n
        ↓
Sales Notification
```

Example:

```text
🔥 HOT LEAD

Customer: John
Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80,000,000
Timeline: Within 2 months
Score: 88
```

---

# 26. Step 13 — Customer Response

The AI can generate an appropriate response.

The response should be based on verified information.

Example:

```text
Thanks for sharing your requirements. I have noted that
you're looking for a 3-bedroom apartment in Lekki with a
budget of around ₦80 million.

A member of our sales team will follow up with you shortly.
```

The system must not invent available properties.

---

# 27. Step 14 — Sales Follow-Up

The sales agent receives the lead.

The agent can:

```text
View Lead
   ↓
Review Requirements
   ↓
Contact Customer
   ↓
Update Status
   ↓
Add Notes
   ↓
Schedule Follow-Up
```

---

# 28. Lead Lifecycle Architecture

The lead lifecycle should be represented as a controlled state machine.

Initial states:

```text
NEW
 ↓
QUALIFYING
 ↓
QUALIFIED
 ↓
CONTACTED
 ↓
FOLLOW_UP
 ↓
NEGOTIATION
 ↓
CONVERTED
```

Alternative outcomes:

```text
LOST
UNQUALIFIED
NOT_INTERESTED
DUPLICATE
```

Not every state transition should be allowed.

Example:

```text
NEW
 ↓
QUALIFYING
```

is valid.

But:

```text
CONVERTED
 ↓
NEW
```

should generally not be permitted without an explicit administrative action.

The detailed state machine belongs in `TECHNICAL_SPEC.md`.

---

# 29. Synchronous vs Asynchronous Processing

The system should distinguish between actions that need an immediate response and actions that can happen asynchronously.

## Synchronous

Examples:

```text
Customer sends message
        ↓
FastAPI validation
        ↓
Immediate response
```

These operations are directly related to the customer's current interaction.

## Asynchronous

Examples:

```text
Lead Created
     ↓
Notify Sales
     ↓
Sync Google Sheets
     ↓
Create Follow-Up Task
```

These operations may happen after the primary customer response.

This distinction helps improve performance and reliability.

---

# 30. Event-Driven Concepts

The architecture should use events where appropriate.

Example events:

```text
LeadCreated
LeadUpdated
LeadQualified
LeadScoreChanged
LeadAssigned
FollowUpRequired
FollowUpCompleted
```

Example:

```text
LeadQualified
      │
      ├──> Update SQL
      │
      ├──> Update Google Sheets
      │
      └──> Notify Sales
```

This reduces unnecessary coupling between components.

---

# 31. API Boundary

The frontend should communicate with the backend through defined APIs.

```text
React
  │
  │ HTTP/JSON
  ▼
FastAPI
```

React should not directly connect to the SQL database.

React should also not contain database credentials.

---

# 32. Database Boundary

The SQL database should be accessed through trusted backend/application services.

Preferred:

```text
React
 ↓
FastAPI
 ↓
Database
```

Not:

```text
React
 ↓
Database
```

The backend provides the security and business-rule boundary.

---

# 33. n8n Boundary

n8n should communicate with systems through explicit interfaces.

For example:

```text
FastAPI
   ↓
n8n Webhook/API
   ↓
Workflow
```

and:

```text
n8n
 ├── AI API
 ├── SQL
 ├── Google Sheets
 └── Notification API
```

Credentials should be stored securely within the appropriate credential-management mechanism.

---

# 34. AI Boundary

AI should not have unrestricted access to the entire application.

The AI should receive only the context it needs.

Example:

```text
Customer Message
        ↓
AI
        ↓
Structured Result
```

Rather than:

```text
AI
 ↓
Full Database
 ↓
Full Application
 ↓
All APIs
```

AI tools should follow the **principle of least privilege**.

---

# 35. AI Tool Architecture

If the system later uses an agentic architecture, tools may include:

```text
get_lead()
create_lead()
update_lead()
search_properties()
get_customer()
create_followup()
notify_sales()
```

Each tool should have:

- Defined input schema.
- Defined output schema.
- Permission boundaries.
- Error handling.
- Logging.

The AI Agent Specification will define these in detail.

---

# 36. Data Flow

The primary data flow is:

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
Structured Lead Data
   ↓
Validation
   ↓
Qualification
   ↓
SQL Database
   ↓
Google Sheets / Notifications
   ↓
Sales Team
```

---

# 37. Conversation Data Flow

Conversation information should be retained so the system can understand follow-up messages.

Example:

```text
Customer:
"I want a 3-bedroom apartment."

        ↓

Bot:
"Which location are you interested in?"

        ↓

Customer:
"Lekki."

        ↓

Bot:
"What is your budget?"

        ↓

Customer:
"About ₦80m."
```

The system should combine these messages into the appropriate lead context.

Conceptually:

```text
Conversation
     │
     ├── Message 1
     ├── Message 2
     ├── Message 3
     └── Message 4
             │
             ▼
       Lead Context
```

---

# 38. Error Architecture

Errors should be handled according to where they occur.

## Frontend Error

```text
React
 ↓
Display user-friendly error
```

## API Error

```text
FastAPI
 ↓
Structured error response
 ↓
React
```

## AI Error

```text
AI Failure
 ↓
Retry
 ↓
Fallback
 ↓
Human Escalation
```

## n8n Error

```text
Workflow Failure
 ↓
Error Handling
 ↓
Log
 ↓
Retry / Alert
```

## Database Error

```text
Database Failure
 ↓
Log
 ↓
Do not falsely confirm success
 ↓
Retry / Error Response
```

---

# 39. Reliability Principles

The system should use:

- Validation.
- Retries where appropriate.
- Timeouts.
- Idempotency.
- Error handling.
- Logging.
- Monitoring.
- Fallbacks.
- Human escalation.

Critical operations should not rely on an AI model successfully responding every time.

---

# 40. Security Architecture

Security should exist across all layers.

```text
React
 ↓
Authentication
 ↓
FastAPI Authorization
 ↓
Business Rules
 ↓
Database
```

Sensitive credentials should never be placed directly into:

- React source code.
- Git repositories.
- README files.
- Public configuration.
- AI prompts.

Security requirements will be documented separately in:

```text
docs/SECURITY_SPEC.md
```

---

# 41. Observability

The system should provide enough visibility to answer:

- What happened?
- When did it happen?
- Which component failed?
- Which lead was affected?
- What workflow executed?
- Did AI processing succeed?
- Did database storage succeed?
- Was the sales team notified?

Important events should be logged.

Example:

```text
2026-09-06 15:32
LeadCreated
Lead ID: lead_123
Source: React Chat
```

---

# 42. Auditability

Important changes should be traceable.

Examples:

```text
Lead created
Lead score changed
Lead assigned
Lead status changed
Sales note added
Follow-up completed
```

Where appropriate, the system should record:

```text
Who
What
When
Previous Value
New Value
```

This becomes particularly important when multiple sales users interact with the same lead.

---

# 43. Source of Truth

The architecture establishes the following ownership model:

| Data / Responsibility | Primary Owner |
|---|---|
| UI State | React |
| API | FastAPI |
| Application Business Logic | FastAPI / defined service layer |
| Workflow Orchestration | n8n |
| AI Understanding | AI Layer |
| Persistent Business Data | SQL Database |
| Operational Reporting | Google Sheets |
| Human Sales Decisions | Sales Team |

This prevents unclear ownership.

---

# 44. Dependency Direction

Dependencies should generally flow inward toward controlled application logic.

Preferred:

```text
React
 ↓
FastAPI
 ↓
Services
 ↓
Database
```

n8n may interact with APIs and external systems:

```text
n8n
 ├── FastAPI
 ├── AI
 ├── SQL
 ├── Google Sheets
 └── Notifications
```

Components should avoid unnecessary circular dependencies.

---

# 45. Initial Repository Architecture

The project should evolve toward a structure such as:

```text
real-estate-lead-bot/
│
├── README.md
├── AGENTS.md
│
├── docs/
│   ├── PRD.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── TECHNICAL_SPEC.md
│   ├── API_SPEC.md
│   ├── DATA_MODEL.md
│   ├── AI_AGENT_SPEC.md
│   ├── UI_UX_SPEC.md
│   ├── SECURITY_SPEC.md
│   └── DEVELOPMENT_GUIDE.md
│
├── frontend/
│   └── React application
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── core/
│   │
│   └── tests/
│
├── n8n/
│   └── workflows/
│
├── database/
│   └── migrations/
│
└── tests/
```

The exact structure may change during implementation.

---

# 46. Responsibility Matrix

| Component | Responsible For | Should Not Own |
|---|---|---|
| React | UI and user interaction | Database credentials |
| FastAPI | APIs and application logic | UI rendering |
| n8n | Workflow orchestration | Entire application business domain |
| AI | Understanding and generation | Unrestricted system control |
| SQL | Persistent data | UI behavior |
| Google Sheets | Operational reporting | Primary system-of-record data |
| Sales Team | Human decisions/follow-up | Technical workflow execution |

---

# 47. Architecture Decision Principles

When introducing a new feature, the team should ask:

### Question 1

Does this belong in the frontend?

If it concerns presentation or user interaction, probably yes.

### Question 2

Does this belong in FastAPI?

If it concerns application behavior, API validation, authorization, or core business logic, probably yes.

### Question 3

Does this belong in n8n?

If it concerns orchestration, integration, notifications, or workflow sequencing, probably yes.

### Question 4

Does this require AI?

Only use AI where natural-language reasoning or generation provides meaningful value.

### Question 5

Does this belong in SQL?

If the information must persist as authoritative business data, it should generally belong in SQL.

### Question 6

Does this belong in Google Sheets?

Only when spreadsheet-based visibility, reporting, or operational workflows provide a clear benefit.

---

# 48. Architecture Evolution

The initial architecture is intentionally simple.

Future versions may introduce:

```text
API Gateway
Message Queue
Redis
Background Workers
Dedicated AI Service
Vector Database
Property Search Service
CRM Integration
Analytics Service
```

These should only be introduced when actual requirements justify their complexity.

The project should avoid **premature architecture**.

---

# 49. MVP Architecture

For the first working version, the architecture should remain relatively simple:

```text
                 CUSTOMER
                    │
                    ▼
             ┌─────────────┐
             │    React    │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │   FastAPI   │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │     n8n     │
             └───┬─────┬───┘
                 │     │
            ┌────▼┐   ┌▼─────────┐
            │ AI  │   │ SQL DB   │
            └──┬──┘   └────┬────┘
               │           │
               └─────┬─────┘
                     ▼
              ┌─────────────┐
              │   n8n       │
              │ Notifications│
              └──────┬──────┘
                     ▼
                SALES TEAM
```

Google Sheets can be connected through n8n as an operational surface.

---

# 50. Architecture Success Criteria

The architecture is successful if:

- Frontend and backend have clear boundaries.
- Backend and n8n have clear responsibilities.
- AI cannot freely modify the entire system.
- SQL remains the primary system of record.
- Google Sheets does not become an accidental second database.
- Lead processing can be traced end-to-end.
- Failures can be detected.
- Important operations can be retried safely.
- Human intervention is possible.
- New integrations can be added without rewriting the entire application.
- AI coding agents can understand where new code belongs.

---

# 51. Relationship With Other Documents

This architecture document provides the structural foundation for the remaining technical documents.

```text
PRD.md
   │
   ▼
SYSTEM_ARCHITECTURE.md
   │
   ├──────────────┐
   ▼              ▼
TECHNICAL_SPEC   DATA_MODEL
   │              │
   ▼              ▼
API_SPEC       Database
   │
   ├──────────────┐
   ▼              ▼
UI_UX_SPEC    AI_AGENT_SPEC
   │              │
   └──────┬───────┘
          ▼
   IMPLEMENTATION
          │
          ▼
       TESTING
```

The architecture should be updated when major structural decisions change.

---

# 52. Current Architecture Decisions

| Decision | Status |
|---|---|
| React for frontend | Approved |
| FastAPI for backend | Approved |
| n8n for orchestration | Approved |
| SQL as system of record | Approved |
| Google Sheets for operational use | Approved |
| AI for natural-language processing | Approved |
| Human-in-the-loop | Approved |
| AI output validation | Required |
| Rule-based lead qualification | Recommended |
| API boundary between frontend/backend | Required |
| Direct frontend-to-database access | Prohibited |
| Secrets in source code | Prohibited |
| AI unrestricted system access | Prohibited |

---

# 53. Open Architecture Decisions

The following decisions remain to be finalized during technical design:

- Exact SQL database technology.
- Authentication provider/mechanism.
- Exact LLM provider/model.
- AI structured-output mechanism.
- n8n deployment strategy.
- API-to-n8n communication mechanism.
- Database-to-n8n integration approach.
- Notification provider.
- React application structure.
- State management strategy.
- Background processing strategy.
- Logging/monitoring solution.
- Deployment infrastructure.
- CI/CD strategy.

These decisions should be recorded as they are made rather than being assumed.

---

# 54. Final Architecture Principle

The Real Estate Lead Bot should be treated as a **small distributed business system**, not merely an automation workflow.

The architecture therefore follows this principle:

```text
React
    = Experience

FastAPI
    = Application/API

n8n
    = Orchestration

AI
    = Intelligence

SQL
    = System of Record

Google Sheets
    = Operational Surface

Sales Team
    = Human Decision Maker
```

The goal is not to make every part autonomous.

The goal is to make the overall system **reliable, understandable, maintainable, observable, and useful to the business**.