# Real Estate Lead Bot — Technical Specification

**Version:** 1.0  
**Status:** Draft  
**Related Documents:**
- `PRD.md`
- `SYSTEM_ARCHITECTURE.md`

**Product:** PrimeHomes Realty Lead Management System

---

# 1. Purpose

This document defines the technical implementation requirements for the Real Estate Lead Bot.

The PRD defines **what the product must accomplish**.

The System Architecture defines **how the major system components interact**.

This document defines **how those components should be implemented**.

It establishes:

- Application responsibilities.
- Service boundaries.
- Data processing rules.
- Lead lifecycle.
- Lead qualification.
- AI processing.
- Validation.
- Error handling.
- Retry behavior.
- Idempotency.
- API behavior.
- Workflow behavior.
- Database interaction.
- Security boundaries.
- Testing requirements.

This document is intended to be used by:

- Backend developers.
- Frontend developers.
- Automation engineers.
- AI engineers.
- QA engineers.
- Technical project managers.
- AI coding assistants and agentic development systems.

---

# 2. Technical Goals

The implementation should prioritize:

1. Reliability.
2. Maintainability.
3. Clear separation of responsibilities.
4. Data integrity.
5. AI reliability.
6. Security.
7. Observability.
8. Testability.
9. Extensibility.
10. Simple architecture before unnecessary complexity.

---

# 3. Technology Stack

| Layer | Technology | Responsibility |
|---|---|---|
| Frontend | React | User interface |
| Backend | Python + FastAPI | API and application services |
| Automation | n8n | Workflow orchestration |
| AI | LLM | Natural-language processing |
| Primary Database | SQL | System of record |
| Operational Data | Google Sheets | Reporting / operational visibility |
| API Format | JSON | Data exchange |
| API Protocol | HTTP/HTTPS | Service communication |

The exact versions of technologies will be documented in the repository configuration and `README.md`.

---

# 4. System Boundaries

The system is divided into the following technical boundaries:

```text
┌─────────────────────────────────────────────┐
│                 React                       │
│              Presentation                   │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                FastAPI                      │
│        API + Application Services           │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                  n8n                        │
│            Workflow Orchestration           │
└──────────────┬──────────────┬───────────────┘
               │              │
               ▼              ▼
        ┌────────────┐   ┌──────────────┐
        │     AI     │   │  SQL Database│
        └────────────┘   └──────────────┘
               │
               ▼
       External Integrations
```

---

# 5. Responsibility Model

## 5.1 React

React owns:

- UI rendering.
- User interactions.
- Form state.
- Chat state.
- Client-side validation.
- API communication.
- Loading states.
- Error display.

React does not own:

- Database operations.
- Secrets.
- Authoritative lead qualification.
- Authentication authorization decisions.
- Critical business rules.

---

# 6. FastAPI Responsibilities

FastAPI owns the application API boundary.

Responsibilities include:

- Request validation.
- Response formatting.
- Authentication.
- Authorization.
- Application services.
- Database access where appropriate.
- Business rules that require application-level control.
- Idempotency handling.
- Error handling.
- Service coordination.

FastAPI should expose stable APIs to the frontend.

---

# 7. n8n Responsibilities

n8n owns workflow orchestration.

Responsibilities include:

- Triggering workflows.
- Calling external services.
- AI orchestration.
- Data transformation.
- Conditional workflow execution.
- Notifications.
- Google Sheets synchronization.
- Follow-up automation.
- Integration workflows.
- Retry workflows where appropriate.

n8n should not become the sole source of truth for core application state.

---

# 8. AI Responsibilities

The AI layer owns tasks requiring natural-language understanding.

AI responsibilities include:

- Intent classification.
- Entity extraction.
- Requirement extraction.
- Message interpretation.
- Conversation summarization.
- Missing-information detection.
- Response generation.

AI should not directly own:

- Database schema.
- Authentication.
- Authorization.
- Financial transactions.
- Lead ownership.
- Critical state transitions.
- Security decisions.

---

# 9. SQL Database Responsibilities

The SQL database is the authoritative system of record for application data.

It should store:

- Customers.
- Leads.
- Conversations.
- Messages.
- Requirements.
- Lead scores.
- Lead statuses.
- Sales assignments.
- Follow-ups.
- Audit information.

The database should enforce appropriate:

- Constraints.
- Relationships.
- Data types.
- Unique values.
- Referential integrity.

---

# 10. Google Sheets Responsibilities

Google Sheets is an operational integration rather than the primary database.

It may be used for:

- Sales visibility.
- Reporting.
- Export.
- Operational workflows.
- Early-stage demonstrations.

Google Sheets must not silently override authoritative SQL data.

---

# 11. Core Domain Entities

The initial domain model includes:

```text
Customer
Lead
Conversation
Message
PropertyRequirement
LeadScore
LeadStatusHistory
FollowUp
SalesAgent
User
AuditLog
```

---

# 12. Customer Entity

A customer represents the person communicating with PrimeHomes Realty.

Conceptual structure:

```text
Customer
├── id
├── name
├── email
├── phone
├── created_at
└── updated_at
```

A customer may have one or more conversations.

A customer may also generate one or more leads depending on the business rules.

---

# 13. Lead Entity

A lead represents a potential business opportunity.

Conceptual structure:

```text
Lead
├── id
├── customer_id
├── intent
├── property_type
├── location
├── bedrooms
├── budget
├── currency
├── timeline
├── score
├── qualification
├── status
├── assigned_agent_id
├── source
├── created_at
└── updated_at
```

The authoritative database schema will be documented in:

```text
docs/DATA_MODEL.md
```

---

# 14. Conversation Entity

A conversation represents an interaction between the customer and the system.

Conceptual structure:

```text
Conversation
├── id
├── customer_id
├── lead_id
├── channel
├── status
├── created_at
└── updated_at
```

---

# 15. Message Entity

Each individual customer or bot message should be represented as a message.

Conceptual structure:

```text
Message
├── id
├── conversation_id
├── sender_type
├── content
├── created_at
└── metadata
```

Possible sender types:

```text
CUSTOMER
BOT
SALES_AGENT
SYSTEM
```

---

# 16. Property Requirement Entity

Property requirements represent what the customer wants.

Examples:

```text
Property Type
Location
Bedrooms
Budget
Currency
Buy/Rent
Timeline
```

These requirements may initially be stored directly against the lead but should be modeled separately if the system becomes more complex.

---

# 17. Lead Status

The initial lead status model is:

```text
NEW
QUALIFYING
QUALIFIED
CONTACTED
FOLLOW_UP
NEGOTIATION
CONVERTED
LOST
UNQUALIFIED
NOT_INTERESTED
DUPLICATE
```

---

# 18. Lead State Machine

Lead statuses should follow controlled transitions.

Initial state:

```text
NEW
```

Normal progression:

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

Alternative terminal outcomes:

```text
QUALIFYING → UNQUALIFIED
QUALIFIED  → LOST
CONTACTED  → LOST
FOLLOW_UP  → LOST
NEGOTIATION → LOST
```

A terminal state should not normally transition back into an active state without an explicit administrative action.

---

# 19. Lead Intent

Initial intent values:

```text
BUYING
RENTING
SELLING
LAND
PROPERTY_ENQUIRY
GENERAL_ENQUIRY
UNKNOWN
```

Intent must be represented using controlled values rather than arbitrary strings wherever practical.

---

# 20. Property Type

Initial property types:

```text
APARTMENT
HOUSE
LAND
OFFICE
SHOP
DUPLEX
OTHER
UNKNOWN
```

The system should support future expansion.

---

# 21. Timeline

Initial normalized timeline values:

```text
IMMEDIATE
WITHIN_1_MONTH
WITHIN_3_MONTHS
RESEARCHING
UNKNOWN
```

The original customer wording may also be retained when useful.

Example:

```text
normalized_timeline:
WITHIN_3_MONTHS

original_timeline:
"I want to move in about two months."
```

---

# 22. Money Representation

Financial values should not be stored as formatted text.

Avoid:

```text
"₦80 million"
```

Prefer structured representation:

```json
{
  "amount": 80000000,
  "currency": "NGN"
}
```

The backend should validate numerical ranges.

The system should preserve currency explicitly.

---

# 23. Input Processing Pipeline

Every customer message should follow a controlled processing pipeline.

```text
Receive Request
      ↓
Validate Request
      ↓
Identify Conversation
      ↓
Persist Message
      ↓
Prepare AI Context
      ↓
AI Processing
      ↓
Validate AI Output
      ↓
Merge With Existing Lead Data
      ↓
Check Missing Information
      ↓
Qualify Lead
      ↓
Persist Lead
      ↓
Trigger Required Actions
      ↓
Generate Response
      ↓
Return Response
```

---

# 24. Request Validation

FastAPI should validate incoming requests before they reach downstream services.

Example request:

```json
{
  "conversation_id": "conv_123",
  "message": "I want a 3-bedroom apartment in Lekki."
}
```

Validation should include:

- Required fields.
- Data types.
- String length.
- Valid identifiers.
- Allowed values where applicable.

Invalid requests should return structured API errors.

---

# 25. AI Input Preparation

The AI should receive only the information required for the current task.

Possible AI context:

```text
Current Customer Message
Previous Relevant Messages
Known Lead Information
Business Instructions
Required Extraction Schema
```

The system should avoid unnecessarily sending sensitive information.

---

# 26. AI Structured Output

AI output should follow a defined schema.

Example:

```json
{
  "intent": "BUYING",
  "property_type": "APARTMENT",
  "location": "Lekki",
  "bedrooms": 3,
  "budget": {
    "amount": 80000000,
    "currency": "NGN"
  },
  "timeline": "UNKNOWN",
  "customer": {
    "name": null,
    "email": null,
    "phone": null
  }
}
```

The exact schema will be defined in `AI_AGENT_SPEC.md`.

---

# 27. AI Output Validation

AI output must be validated before it is stored or used for business decisions.

Validation should check:

```text
Schema
Types
Enums
Required fields
Numeric ranges
Data consistency
```

Example:

```text
AI Output
   ↓
Schema Validator
   ↓
Valid?
 ┌─┴─┐
YES  NO
 │    │
 ▼    ▼
Continue
      Retry / Repair / Escalate
```

---

# 28. AI Confidence

Where supported, AI processing should provide confidence or uncertainty information.

Example:

```json
{
  "intent": "BUYING",
  "confidence": 0.94
}
```

Low-confidence results should trigger:

- Clarification.
- Additional processing.
- Human escalation.

The system should not assume that every AI response is correct simply because it is syntactically valid.

---

# 29. Missing Information Logic

The system should determine which information is required before considering a lead sufficiently qualified.

Example:

```text
Property Type  ✓
Location       ✓
Budget         ✓
Bedrooms       ✓
Timeline       ✗
```

The system may ask for the missing information.

However, required fields should depend on the customer's intent.

For example, a land enquiry may not require bedroom information.

---

# 30. Context Merging

Newly extracted information should be merged with previously known lead information.

Example:

First message:

```text
"I want a 3-bedroom apartment."
```

Stored:

```text
property_type = APARTMENT
bedrooms = 3
```

Second message:

```text
"I'm interested in Lekki."
```

Updated:

```text
property_type = APARTMENT
bedrooms = 3
location = LEKKI
```

The system must avoid replacing known valid values with `null` unless the customer explicitly removes or changes the requirement.

---

# 31. Lead Qualification Model

Lead qualification should use deterministic business rules.

AI may extract information, but the final score should be calculated using controlled logic.

Conceptual model:

```text
Lead Data
   ↓
Qualification Rules
   ↓
Score
   ↓
Qualification Category
```

---

# 32. Example Qualification Factors

Potential factors include:

| Factor | Example |
|---|---|
| Budget | Higher verified budget |
| Timeline | Immediate requirement |
| Location | Specific location |
| Property Type | Clearly defined |
| Completeness | Required information available |
| Intent | Strong buying/renting intent |
| Engagement | Responsive customer |

The exact weights should be finalized after business requirements are confirmed.

---

# 33. Example Scoring Model

An initial scoring model may be:

```text
Budget clarity       0–20
Timeline              0–20
Location specificity  0–15
Property specificity  0–15
Intent strength       0–15
Information complete  0–15
                     ----
Maximum               100
```

Qualification:

```text
0–20     LOW
21–40    NORMAL
41–70    WARM
71–100   HOT
```

These values are initial engineering placeholders.

They must be validated against actual business requirements before production use.

---

# 34. Qualification Explainability

The system should store why a lead received its score.

Example:

```json
{
  "score": 85,
  "qualification": "HOT",
  "reasons": [
    "Immediate purchase timeline",
    "Specific location",
    "Clear property requirement",
    "Budget provided"
  ]
}
```

This allows sales staff to understand the qualification rather than receiving an unexplained score.

---

# 35. Lead Assignment

The system may assign qualified leads to sales agents.

Initial assignment strategies may include:

```text
Round Robin
Location-Based
Property-Type-Based
Manual Assignment
```

Assignment logic should be introduced only when the business requirements are finalized.

---

# 36. Customer Response Generation

The AI response should be generated only after the system has determined what information is safe and appropriate to communicate.

Response generation should consider:

- Customer message.
- Known requirements.
- Missing information.
- Lead state.
- Available verified data.
- Business instructions.

The AI should not invent:

- Properties.
- Prices.
- Availability.
- Discounts.
- Policies.
- Sales commitments.

---

# 37. Response Types

The system may generate responses such as:

### Information Collection

```text
"Thanks for reaching out. What location are you interested in,
and what is your approximate budget?"
```

### Confirmation

```text
"Thanks. I've noted that you're looking for a 3-bedroom
apartment in Lekki with a budget of around ₦80 million."
```

### Human Escalation

```text
"Thanks for sharing your requirements. A member of our sales
team will follow up with you shortly."
```

---

# 38. n8n Workflow Design

The primary n8n workflow should be modular.

Conceptually:

```text
Trigger
  ↓
Validate
  ↓
Prepare Data
  ↓
AI Processing
  ↓
Validate AI Output
  ↓
Lead Processing
  ↓
Qualification
  ↓
Database
  ↓
Notification
  ↓
Response
```

Where practical, complex operations should be separated into reusable workflows.

---

# 39. Suggested n8n Workflow Structure

```text
n8n/
└── workflows/
    ├── lead-intake
    ├── ai-lead-processing
    ├── lead-qualification
    ├── lead-storage
    ├── sales-notification
    ├── google-sheets-sync
    └── follow-up
```

The actual workflow organization may evolve.

---

# 40. n8n Workflow Responsibilities

Each workflow should have a clearly defined purpose.

For example:

### `lead-intake`

Receives and prepares lead data.

### `ai-lead-processing`

Calls AI and validates structured output.

### `lead-qualification`

Calculates qualification.

### `lead-storage`

Creates or updates the SQL lead.

### `sales-notification`

Notifies sales when conditions are met.

### `google-sheets-sync`

Synchronizes selected data.

### `follow-up`

Handles scheduled or triggered follow-up operations.

---

# 41. Idempotency

Critical operations should be idempotent where practical.

For example, if the same request is processed twice:

```text
Request A
↓
Create Lead
```

and then accidentally retried:

```text
Request A
↓
Do NOT create duplicate Lead
```

Instead:

```text
Request ID / Idempotency Key
          ↓
Check Existing Operation
          ↓
Return Existing Result
```

This is particularly important for:

- Lead creation.
- Notifications.
- Payment-like operations if added later.
- External integrations.

---

# 42. Retry Strategy

Retries should be used for temporary failures.

Examples:

- Network timeout.
- Temporary API outage.
- Rate limit.
- Temporary database connection failure.

Not every error should be retried.

For example:

```text
Invalid AI schema
```

may require repair or escalation rather than repeatedly sending the same request.

---

# 43. Retry Policy

Conceptual strategy:

```text
Attempt 1
   ↓
Failure
   ↓
Short delay
   ↓
Attempt 2
   ↓
Failure
   ↓
Longer delay
   ↓
Attempt 3
   ↓
Failure
   ↓
Fallback / Alert
```

The exact retry counts and delays should be defined per integration.

---

# 44. Timeout Strategy

External services should have reasonable timeouts.

Examples:

```text
Frontend → FastAPI
FastAPI → n8n
n8n → AI
n8n → Database
n8n → Notification Service
```

The system should not wait indefinitely for an external service.

---

# 45. Error Categories

Errors should be classified.

```text
VALIDATION_ERROR
AUTHENTICATION_ERROR
AUTHORIZATION_ERROR
NOT_FOUND
CONFLICT
AI_ERROR
DATABASE_ERROR
INTEGRATION_ERROR
TIMEOUT
RATE_LIMIT
INTERNAL_ERROR
```

This allows consistent error handling.

---

# 46. API Error Format

API errors should use a predictable structure.

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request.",
    "details": {
      "field": "message"
    }
  }
}
```

The exact API contract will be documented in:

```text
docs/API_SPEC.md
```

---

# 47. Backend Service Structure

The FastAPI backend should separate concerns.

Recommended structure:

```text
backend/
└── app/
    ├── main.py
    │
    ├── api/
    │   ├── routes/
    │   └── dependencies.py
    │
    ├── schemas/
    │
    ├── models/
    │
    ├── services/
    │
    ├── repositories/
    │
    ├── core/
    │
    └── utils/
```

---

# 48. API Layer

The API layer should:

- Receive requests.
- Validate input.
- Authenticate.
- Authorize.
- Call application services.
- Return responses.

Routes should not contain large amounts of business logic.

Avoid:

```text
Route
 ↓
100+ lines of business logic
```

Prefer:

```text
Route
 ↓
Service
 ↓
Repository / External Service
```

---

# 49. Service Layer

Services should contain application behavior.

Examples:

```text
LeadService
ConversationService
QualificationService
NotificationService
AIService
FollowUpService
```

Example:

```text
Lead API
   ↓
LeadService
   ↓
Repository
   ↓
SQL Database
```

---

# 50. Repository Layer

Repositories provide a controlled way for application services to interact with the database.

Example:

```text
LeadService
    ↓
LeadRepository
    ↓
SQL Database
```

This reduces direct database logic throughout the application.

---

# 51. Database Transactions

Operations that require multiple related database changes should use transactions where appropriate.

Example:

```text
Create Lead
+
Create Lead Status
+
Create Conversation Link
```

These should not leave the database in an inconsistent state if one operation fails.

---

# 52. Frontend Architecture

The React application should separate:

```text
Components
Pages
API Client
State
Hooks
Types
Utilities
```

Example:

```text
frontend/
└── src/
    ├── components/
    ├── pages/
    ├── features/
    ├── services/
    ├── hooks/
    ├── types/
    ├── utils/
    └── app/
```

The exact structure may evolve.

---

# 53. Frontend API Client

API calls should be centralized rather than scattered across UI components.

Prefer:

```text
React Component
      ↓
API Client
      ↓
FastAPI
```

rather than allowing every component to independently construct API requests.

---

# 54. Frontend State

The frontend should distinguish between:

### Local UI State

Examples:

```text
Modal open/closed
Input value
Loading indicator
```

### Server State

Examples:

```text
Lead data
Customer data
Conversation data
```

Server state should be managed consistently using the selected React data-fetching/state strategy.

---

# 55. Authentication

Authentication should be implemented at the backend/API boundary.

The frontend should not be considered a trusted environment.

Authentication architecture will be finalized in:

```text
docs/SECURITY_SPEC.md
```

---

# 56. Authorization

Authorization should determine what authenticated users can do.

Example:

```text
Admin
→ Full management

Sales Manager
→ Team lead visibility

Sales Agent
→ Assigned leads

Viewer
→ Read-only
```

The exact roles and permissions must be finalized before production.

---

# 57. Logging

Important operations should produce structured logs.

Examples:

```text
lead.created
lead.updated
lead.qualified
lead.assigned
ai.processing_started
ai.processing_failed
workflow.failed
notification.sent
```

Logs should avoid exposing sensitive customer information unnecessarily.

---

# 58. Observability

The system should make it possible to trace a lead through the system.

A useful conceptual identifier is:

```text
request_id
```

or:

```text
trace_id
```

Example:

```text
Customer Message
      │
      └── trace_id: abc123
              │
              ├── FastAPI
              ├── n8n
              ├── AI
              ├── SQL
              └── Notification
```

This makes debugging much easier.

---

# 59. Audit Trail

Important lead changes should be auditable.

Example:

```text
Lead Status Changed

From:
QUALIFIED

To:
CONTACTED

Changed By:
sales_agent_123

Timestamp:
2026-09-06T15:30:00
```

---

# 60. Security Requirements

The implementation must:

- Keep secrets outside source code.
- Use environment variables or secure credential storage.
- Validate input.
- Authenticate protected endpoints.
- Authorize sensitive operations.
- Protect customer data.
- Restrict AI tools.
- Avoid exposing database credentials.
- Avoid exposing internal system details to customers.

---

# 61. Environment Configuration

Environment-specific values should not be hardcoded.

Example:

```text
DATABASE_URL
N8N_WEBHOOK_URL
AI_API_KEY
GOOGLE_SHEETS_CREDENTIALS
JWT_SECRET
```

An example environment file may be provided:

```text
.env.example
```

Actual secrets must never be committed to Git.

---

# 62. AI Tool Permission Model

If the AI agent is given tools, each tool must have explicit permissions.

Example:

```text
Tool: get_lead
Permission: READ

Tool: update_lead
Permission: WRITE

Tool: delete_lead
Permission: DENIED

Tool: notify_sales
Permission: CONTROLLED
```

AI should operate according to least-privilege principles.

---

# 63. Human Escalation

The system should escalate to a human when:

- AI confidence is low.
- Customer request is ambiguous.
- AI output repeatedly fails validation.
- Customer requests unsupported actions.
- A business decision requires human judgment.
- A high-value lead requires immediate human attention.

---

# 64. Data Consistency

The system should prevent conflicting representations of the same lead.

For example:

```text
SQL:
status = HOT
```

while:

```text
Google Sheets:
status = LOST
```

should not happen without a defined synchronization process.

SQL remains authoritative.

---

# 65. Google Sheets Synchronization

Synchronization should follow a defined direction.

Initial model:

```text
SQL Database
      ↓
n8n
      ↓
Google Sheets
```

Google Sheets should not automatically write back to SQL unless a specific two-way synchronization design is introduced.

---

# 66. Notification Rules

Example:

```text
IF qualification = HOT
THEN notify sales team
```

Another example:

```text
IF follow_up_required = TRUE
THEN create follow-up action
```

Notification rules should be deterministic and documented.

AI should not independently decide to send arbitrary notifications.

---

# 67. Duplicate Detection

Potential duplicate indicators include:

```text
Email
Phone
Conversation ID
Customer ID
```

Duplicate detection should occur before creating a new lead when practical.

---

# 68. Data Normalization

The system should normalize extracted values.

Example:

AI:

```text
"80m"
```

Normalize:

```text
amount = 80000000
currency = NGN
```

AI:

```text
"three bedrooms"
```

Normalize:

```text
bedrooms = 3
```

AI:

```text
"Ikeja"
```

Normalize:

```text
location = "Ikeja"
```

The original wording may be preserved when useful for context.

---

# 69. Business Rules vs AI

A critical architectural rule:

```text
AI
→ Interpret

Application Logic
→ Decide

Database
→ Persist

n8n
→ Orchestrate
```

For example:

AI may determine:

```text
Customer appears to want to buy.
```

The application/business rules determine:

```text
Buying + immediate timeline + complete requirements
→ qualifies for HOT review.
```

The AI should not silently replace deterministic business rules.

---

# 70. Testing Strategy

Testing should exist at multiple levels.

```text
Unit Tests
Integration Tests
API Tests
Workflow Tests
AI Evaluation Tests
End-to-End Tests
```

---

# 71. Unit Testing

Unit tests should cover isolated business logic.

Examples:

```text
calculate_lead_score()
normalize_budget()
validate_lead()
determine_missing_fields()
validate_status_transition()
```

---

# 72. Integration Testing

Integration tests should verify interactions between components.

Examples:

```text
FastAPI + SQL
FastAPI + n8n
n8n + AI
n8n + Google Sheets
```

---

# 73. API Testing

Test:

```text
POST /api/chat
POST /api/leads
GET /api/leads
GET /api/leads/{id}
PATCH /api/leads/{id}
```

Test both successful and failure scenarios.

---

# 74. AI Evaluation

AI should be tested using representative customer messages.

Examples:

### Complete Lead

```text
"I need a 3-bedroom apartment in Lekki for ₦80m."
```

### Missing Information

```text
"I want to buy a house."
```

### Informal Language

```text
"Abeg I dey find 2 bed for Ikeja around 50m."
```

### Ambiguous Message

```text
"Do you have anything nice?"
```

### Multiple Requirements

```text
"I need a 4-bedroom duplex in Lekki or Ikoyi,
budget around ₦150m and I want to move next month."
```

The AI evaluation set should grow as real-world examples become available.

---

# 75. End-to-End Testing

An end-to-end test should verify the complete journey:

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
Qualification
 ↓
SQL
 ↓
Notification
 ↓
Sales
```

---

# 76. Failure Scenarios

The system must be tested against:

- Invalid request.
- Missing message.
- AI timeout.
- AI malformed output.
- AI unavailable.
- Database unavailable.
- n8n workflow failure.
- Google Sheets failure.
- Notification failure.
- Duplicate request.
- Duplicate lead.
- Unauthorized API request.
- Invalid lead status transition.

---

# 77. Performance Considerations

The system should monitor:

```text
API latency
AI latency
n8n execution time
Database query time
Notification latency
End-to-end response time
```

Performance optimization should be based on observed bottlenecks rather than premature optimization.

---

# 78. Scalability Strategy

The first version should remain simple.

If traffic increases, possible future improvements include:

```text
Background Jobs
Message Queues
Caching
Redis
Worker Processes
Dedicated AI Service
Database Optimization
Horizontal Scaling
```

These should only be introduced when justified by actual requirements.

---

# 79. Deployment Considerations

The system will eventually consist of independently deployable components:

```text
React Application
FastAPI Application
n8n
SQL Database
External AI Service
```

Each component should have a clearly defined configuration strategy.

Deployment details will be documented in the development/deployment documentation.

---

# 80. Versioning

The API should use a versioning strategy where appropriate.

Example:

```text
/api/v1/leads
/api/v1/chat
```

Versioning should be introduced before breaking changes become necessary.

---

# 81. Backward Compatibility

Changes to APIs, database structures, or AI schemas should consider existing consumers.

A breaking change should not be introduced without:

1. Identifying affected components.
2. Updating documentation.
3. Updating tests.
4. Updating dependent clients.
5. Providing a migration strategy where required.

---

# 82. Migration Strategy

Database schema changes should use migrations.

Example:

```text
database/
└── migrations/
    ├── 001_initial_schema
    ├── 002_add_lead_score
    └── 003_add_follow_up
```

Direct uncontrolled production schema changes should be avoided.

---

# 83. Definition of Technical Completion

A feature is technically complete when:

- Required code is implemented.
- Appropriate tests exist.
- API contracts are updated.
- Database changes are migrated.
- AI schemas are updated where applicable.
- n8n workflows are updated where applicable.
- Error handling is implemented.
- Logging is implemented where necessary.
- Security requirements are satisfied.
- Documentation is updated.
- No known critical regression exists.

---

# 84. Change Management

Any major change should consider its effect on:

```text
PRD
Architecture
Technical Specification
API
Database
AI
n8n
Frontend
Backend
Tests
Security
```

A change should not be implemented in isolation if it affects another system boundary.

---

# 85. Example Feature Implementation

Consider:

> Add automatic hot-lead notification.

The implementation should follow:

```text
PRD
 ↓
Requirement:
Notify sales for HOT leads
 ↓
Technical Specification
 ↓
Define qualification condition
 ↓
n8n Workflow
 ↓
Detect HOT lead
 ↓
Notification Service
 ↓
SQL
 ↓
Record notification
 ↓
Sales Team
```

---

# 86. Example AI Feature Implementation

Requirement:

> Extract customer requirements from natural language.

Flow:

```text
Customer Message
       ↓
FastAPI
       ↓
n8n
       ↓
AI
       ↓
Structured JSON
       ↓
Schema Validation
       ↓
Normalization
       ↓
Lead Update
```

The AI output must pass validation before being treated as application data.

---

# 87. Example Follow-Up Implementation

A future follow-up workflow could be:

```text
Lead
 ↓
FOLLOW_UP_REQUIRED
 ↓
n8n
 ↓
Create Follow-Up
 ↓
Wait / Schedule
 ↓
Notify Sales
 ↓
Sales Agent Contacts Customer
 ↓
Update Lead
```

The exact scheduling implementation will be defined later.

---

# 88. Technical Decision Rules

When deciding where new functionality belongs, use:

```text
UI behavior
→ React

API / application behavior
→ FastAPI

Workflow / integration
→ n8n

Natural-language reasoning
→ AI

Persistent authoritative data
→ SQL

Operational spreadsheet visibility
→ Google Sheets
```

If functionality appears to belong in multiple layers, define a clear ownership boundary rather than duplicating the same logic.

---

# 89. Anti-Patterns to Avoid

## Anti-Pattern 1 — Business Logic Everywhere

Avoid duplicating qualification rules across:

```text
React
FastAPI
n8n
AI
```

There should be one authoritative implementation.

---

## Anti-Pattern 2 — AI as the Database

AI output should not be treated as permanent truth without validation and persistence.

---

## Anti-Pattern 3 — Google Sheets as the Entire Backend

Google Sheets should not become the accidental application database.

---

## Anti-Pattern 4 — Giant n8n Workflow

Avoid creating one enormous workflow containing every possible operation.

Prefer modular workflows.

---

## Anti-Pattern 5 — Frontend as Trusted Environment

Never trust React to enforce security.

Security must be enforced server-side.

---

## Anti-Pattern 6 — AI With Unlimited Tools

AI should receive only the tools and permissions required for its task.

---

## Anti-Pattern 7 — Silent Failures

A failed lead-processing operation should not disappear without logging or notification.

---

# 90. Technical Architecture Summary

The intended implementation is:

```text
                         CUSTOMER
                            │
                            ▼
                     ┌─────────────┐
                     │   REACT     │
                     │  Frontend   │
                     └──────┬──────┘
                            │
                         HTTPS
                            │
                            ▼
                     ┌─────────────┐
                     │   FASTAPI   │
                     │ API / Logic │
                     └──────┬──────┘
                            │
                       Workflow Event
                            │
                            ▼
                     ┌─────────────┐
                     │     n8n     │
                     │ Orchestrator│
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
          ┌────────┐   ┌──────────┐  ┌────────────┐
          │   AI   │   │ SQL DB   │  │ Google     │
          │        │   │          │  │ Sheets     │
          └───┬────┘   └────┬─────┘  └────────────┘
              │             │
              └──────┬──────┘
                     ▼
              ┌──────────────┐
              │ Notifications│
              └──────┬───────┘
                     ▼
                SALES TEAM
```

---

# 91. Core Engineering Principles

The implementation should follow these principles:

### 1. Single Source of Truth

SQL is the authoritative application database.

### 2. Explicit Contracts

APIs and AI outputs should have defined schemas.

### 3. Validate Before Acting

External and AI-generated data must be validated.

### 4. Least Privilege

Users, services and AI agents receive only required permissions.

### 5. Deterministic Business Rules

Important business decisions should not depend entirely on probabilistic AI behavior.

### 6. Observable Automation

n8n workflows must be traceable and failures must be visible.

### 7. Human-in-the-Loop

The system must allow human intervention.

### 8. Modular Design

Components should have clear boundaries.

### 9. Test Critical Paths

Lead intake, qualification, persistence and notification require strong testing.

### 10. Documentation Is Part of Engineering

When system behavior changes, the relevant documentation must change with it.

---

# 92. Technical Specification Status

The following areas are currently defined:

- [x] Technology stack.
- [x] System boundaries.
- [x] Component responsibilities.
- [x] Lead lifecycle.
- [x] AI processing pipeline.
- [x] AI validation principles.
- [x] Lead qualification concept.
- [x] Error handling.
- [x] Retry strategy.
- [x] Idempotency principles.
- [x] Testing strategy.
- [x] Security principles.
- [x] Data ownership.
- [x] n8n responsibilities.
- [x] React responsibilities.
- [x] FastAPI responsibilities.

The following require further specification:

- [ ] Exact SQL database technology.
- [ ] Complete database schema.
- [ ] Complete API contract.
- [ ] Exact AI structured-output schema.
- [ ] Exact AI model/provider.
- [ ] Exact lead-scoring weights.
- [ ] Authentication mechanism.
- [ ] Authorization matrix.
- [ ] Notification provider.
- [ ] Deployment architecture.
- [ ] CI/CD implementation.
- [ ] Detailed n8n workflow definitions.

These will be documented in the appropriate project documents.

---

# 93. Document Dependencies

```text
PRD.md
   │
   ▼
SYSTEM_ARCHITECTURE.md
   │
   ▼
TECHNICAL_SPEC.md
   │
   ├───────────────┐
   ▼               ▼
API_SPEC.md     DATA_MODEL.md
   │               │
   └───────┬───────┘
           ▼
AI_AGENT_SPEC.md
           │
           ▼
UI_UX_SPEC.md
           │
           ▼
SECURITY_SPEC.md
           │
           ▼
DEVELOPMENT_GUIDE.md
           │
           ▼
Implementation
           │
           ▼
Testing
           │
           ▼
Deployment
```

This document therefore acts as the bridge between **architecture and implementation**.