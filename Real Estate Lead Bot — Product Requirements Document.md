# Real Estate Lead Bot
## Product Requirements Document (PRD)

**Version:** 1.0  
**Status:** Draft  
**Product:** PrimeHomes Realty Lead Management System  
**Document Owner:** Product / Engineering  
**Primary Stack:** React, FastAPI, n8n, SQL Database, Google Sheets, LLM/AI

---

# 1. Product Overview

## 1.1 Product Name

**Real Estate Lead Bot**

## 1.2 Product Purpose

The Real Estate Lead Bot is a small business lead-management system designed to help real estate companies automatically receive, understand, capture, qualify, route, and track potential customers.

The system acts as a **digital receptionist and lead qualification assistant**.

Instead of requiring a salesperson to manually read every incoming customer message and extract the relevant information, the system uses AI and automation to transform unstructured customer conversations into structured lead information.

The system will:

1. Receive potential customer messages.
2. Understand customer intent.
3. Extract relevant customer and property requirements.
4. Validate and normalize the extracted information.
5. Create or update a lead record.
6. Qualify and score the lead.
7. Generate an appropriate customer response.
8. Notify the appropriate sales team member.
9. Support human follow-up.
10. Track the lead lifecycle and status.

The system is not intended to replace salespeople.

Its primary purpose is to **reduce manual lead-processing work, improve response speed, prevent lead loss, and give the sales team better information for follow-up.**

---

# 2. Business Context

## 2.1 Example Client

For this project, the example real estate company will be:

**PrimeHomes Realty**

PrimeHomes Realty advertises residential and land properties online and receives enquiries from potential customers.

Incoming enquiries may arrive as structured information or natural-language messages.

Examples:

> "Hi, I'm looking for a 3-bedroom apartment around Lekki. My budget is around ₦80 million."

> "Do you have any 2-bedroom apartments in Ikeja?"

> "I need land around Ibadan, preferably below ₦20 million."

> "Hello, I want to buy a house."

The information contained in these messages varies considerably.

Some customers provide detailed requirements, while others provide very little information.

---

# 3. Business Problem

A manual lead-processing process becomes difficult to manage as enquiry volume increases.

For example, if the company receives approximately 200 customer messages per day, sales staff may need to manually:

- Read each message.
- Identify the customer's intent.
- Extract the customer's name.
- Extract contact information.
- Identify the property type.
- Identify location preferences.
- Identify budget.
- Identify bedroom requirements.
- Determine whether the customer wants to buy or rent.
- Determine the customer's timeframe.
- Record the information.
- Decide how important the lead is.
- Respond to the customer.
- Notify another salesperson when necessary.
- Remember to follow up.

This creates several business problems.

### Problems

- Slow response times.
- Inconsistent lead capture.
- Missing customer information.
- Leads being forgotten.
- Poor visibility into lead status.
- Manual duplication of work.
- Difficulty prioritizing high-value leads.
- Lost sales opportunities.
- Limited ability to scale the sales process.

---

# 4. Product Vision

Create a reliable AI-assisted lead management system that allows a real estate company to move from:

**Incoming message → structured lead → qualified opportunity → human follow-up → tracked outcome**

with as little unnecessary manual work as possible.

The system should combine:

- React for customer-facing interaction.
- FastAPI for application APIs and business logic.
- n8n for workflow orchestration and integrations.
- AI for natural-language understanding and generation.
- SQL for durable system-of-record data.
- Google Sheets for selected operational workflows and sales visibility.

---

# 5. Goals

## 5.1 Primary Goals

The system should:

### G1 — Capture Leads

Automatically receive potential customer enquiries and create lead records.

### G2 — Understand Customer Intent

Determine what the customer is trying to accomplish.

Examples:

- Buy property.
- Rent property.
- Sell property.
- Find land.
- General property enquiry.

### G3 — Extract Requirements

Convert natural-language messages into structured information.

Example:

```json
{
  "property_type": "apartment",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": 80000000,
  "intent": "buy",
  "timeline": "within_3_months"
}
```

### G4 — Qualify Leads

Determine the potential value and urgency of a lead using defined qualification rules.

### G5 — Respond Quickly

Provide customers with an appropriate automated response when automation is appropriate.

### G6 — Notify Sales

Alert the appropriate sales team when human intervention or follow-up is required.

### G7 — Track Lead Lifecycle

Maintain visibility into what happens to each lead from initial enquiry through follow-up and eventual outcome.

### G8 — Reduce Manual Work

Reduce the amount of repetitive lead-processing work performed by sales staff.

### G9 — Maintain Human Oversight

Allow sales staff to take control when the AI cannot confidently or safely handle a situation.

---

# 6. Non-Goals

The first version of the system will NOT attempt to become a complete real estate ERP or CRM.

The MVP will not initially include:

- Full property marketplace functionality.
- Property listing management.
- Online property purchasing.
- Payment processing.
- Mortgage processing.
- Legal transaction management.
- Automated contract signing.
- Fully autonomous sales negotiations.
- Autonomous property recommendations without validated property data.
- Fully autonomous closing of property transactions.

These may become future features.

---

# 7. Target Users

## 7.1 Potential Customer

A person interested in buying, renting, selling, or enquiring about property.

### Needs

- Fast response.
- Simple communication.
- Ability to describe requirements naturally.
- Relevant follow-up.
- Ability to provide missing information.

---

## 7.2 Sales Agent

A salesperson responsible for following up with leads.

### Needs

- Complete lead information.
- Lead priority.
- Customer requirements.
- Conversation history.
- Follow-up reminders.
- Clear lead status.
- Ability to update lead information.

---

## 7.3 Sales Manager

A manager responsible for monitoring sales activity.

### Needs

- Lead pipeline visibility.
- Lead volume.
- Lead quality.
- Sales-agent workload.
- Lead status.
- Follow-up performance.
- Conversion information.

---

## 7.4 System Administrator

Responsible for configuring and maintaining the system.

### Needs

- System configuration.
- User management.
- Integration management.
- Workflow monitoring.
- Error visibility.
- Security controls.

---

# 8. Core User Journey

The primary customer journey is:

```text
Customer sends message
        ↓
System receives message
        ↓
Validate input
        ↓
AI understands intent
        ↓
AI extracts requirements
        ↓
Check required information
        ↓
Ask for missing information if necessary
        ↓
Create/update lead
        ↓
Qualify lead
        ↓
Calculate lead score
        ↓
Store lead
        ↓
Generate customer response
        ↓
Notify sales team when required
        ↓
Sales agent follows up
        ↓
Lead status updated
        ↓
Lead outcome tracked
```

---

# 9. Functional Requirements

## FR-001 — Receive Customer Message

The system must be able to receive a customer message through the supported customer interface.

The initial MVP will use a React-based interface.

The architecture should allow additional channels to be integrated later.

Potential future channels include:

- WhatsApp.
- Website chat.
- Telegram.
- Email.
- Social messaging platforms.

---

## FR-002 — Validate Incoming Data

The system must validate incoming requests before processing.

Validation should include:

- Required request fields.
- Valid data types.
- Maximum message length.
- Valid identifiers.
- Basic input sanitization.

Invalid requests should produce appropriate errors without causing the workflow to fail unpredictably.

---

## FR-003 — Understand Customer Intent

The AI processing layer should classify the customer's intent.

Initial intent categories:

```text
BUYING
RENTING
SELLING
LAND
PROPERTY_ENQUIRY
GENERAL_ENQUIRY
UNKNOWN
```

The system should support an `UNKNOWN` or equivalent state when confidence is insufficient.

---

## FR-004 — Extract Customer Information

The system should attempt to extract:

- Name.
- Email.
- Phone number.

The system must not invent information that the customer has not provided.

Unknown values should remain explicitly unknown/null rather than being fabricated.

---

## FR-005 — Extract Property Requirements

The system should attempt to extract:

- Property type.
- Number of bedrooms.
- Location.
- Budget.
- Currency.
- Buy/rent preference.
- Property-related requirements.

Potential property types include:

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

---

## FR-006 — Extract Timeline

The system should classify the customer's expected timeframe.

Initial categories:

```text
IMMEDIATE
WITHIN_1_MONTH
WITHIN_3_MONTHS
RESEARCHING
UNKNOWN
```

The system should preserve the original customer wording where useful rather than relying exclusively on a normalized category.

---

## FR-007 — Missing Information Detection

The system should determine whether sufficient information exists to continue the lead process.

For example:

Customer:

> "I want to buy a house."

The system may respond with a follow-up question such as:

> "I'd be happy to help. What location are you interested in, and what is your approximate budget?"

The system should avoid asking unnecessary questions when the required information is already available.

---

# 10. Lead Qualification

The system must classify leads according to defined qualification rules.

Initial lead categories:

```text
HOT
WARM
NORMAL
LOW
UNQUALIFIED
```

The exact scoring formula will be defined in the Technical Specification.

Potential qualification factors include:

- Budget.
- Property type.
- Location.
- Purchase/rental intent.
- Timeline.
- Completeness of information.
- Customer engagement.
- Other business-defined signals.

The qualification system should be **rule-based and explainable**, even when AI is involved.

AI may extract and classify information, but the final qualification process should use controlled business rules.

---

# 11. Lead Score

Each lead may receive a numerical score.

Example:

```text
0–20     LOW
21–40    NORMAL
41–70    WARM
71–100   HOT
```

The exact scoring thresholds are placeholders and must be finalized during system design.

The system should store both:

- The numerical score.
- The resulting qualification category.

Where possible, the system should also store the reasons contributing to the score.

Example:

```json
{
  "score": 82,
  "qualification": "HOT",
  "reasons": [
    "High budget",
    "Immediate purchase timeline",
    "Specific location",
    "Property type identified"
  ]
}
```

---

# 12. Lead Lifecycle

Every lead should have a defined lifecycle.

Initial lifecycle:

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

The exact state machine will be defined in the Technical Specification.

The system should prevent invalid state transitions where practical.

---

# 13. Lead Record

A lead should contain structured information such as:

```text
Lead
├── ID
├── Customer Information
│   ├── Name
│   ├── Email
│   └── Phone
│
├── Property Requirements
│   ├── Property Type
│   ├── Bedrooms
│   ├── Location
│   ├── Budget
│   └── Buy/Rent
│
├── Intent
├── Timeline
├── Qualification
├── Score
├── Status
├── Source
├── Conversation Reference
├── Assigned Sales Agent
├── Created At
├── Updated At
└── Follow-up Information
```

The final database schema will be defined separately in `DATA_MODEL.md`.

---

# 14. Customer Response

The system should generate customer responses using AI where appropriate.

Responses should be:

- Relevant.
- Professional.
- Concise.
- Helpful.
- Based on known information.
- Clear about missing information.
- Free from fabricated property availability or pricing.

The AI must not claim that a property exists, is available, or has a specific price unless the system has reliable data supporting that claim.

---

# 15. Sales Notification

The system should notify the sales team when a lead requires attention.

Examples:

### Hot Lead

```text
🔥 HOT LEAD

Customer: John
Location: Lekki
Property: 3-bedroom apartment
Budget: ₦80,000,000
Timeline: Within 1 month
Score: 86
```

### Normal Lead

A lower-priority lead may be recorded without generating an urgent alert.

Notification channels may include:

- Google Sheets.
- Email.
- Slack.
- Other supported systems.

The exact notification architecture will be defined separately.

---

# 16. Sales Follow-Up

Sales agents should be able to:

- View lead information.
- Review conversation information.
- See qualification.
- See lead status.
- Update lead status.
- Add notes.
- Record follow-up activity.
- Assign/reassign leads where permitted.
- Continue communication with the customer through supported channels.

The first MVP may use a simplified interface before a full CRM-style dashboard is implemented.

---

# 17. Automation Requirements

n8n will function as the **workflow orchestration layer**.

n8n may be responsible for:

- Receiving workflow events.
- Calling AI services.
- Transforming data.
- Executing conditional logic.
- Storing operational records.
- Calling external APIs.
- Sending notifications.
- Triggering follow-up workflows.
- Handling retries.
- Connecting multiple systems.

n8n should not become the only location where core business logic exists.

Critical business rules that require strong version control, testing, or transactional guarantees should be implemented in the appropriate application/backend layer where necessary.

---

# 18. Backend Requirements

The backend will use:

**Python + FastAPI**

FastAPI will provide application APIs and backend services where required.

Potential initial endpoints include:

```http
POST /api/leads
GET /api/leads/{id}
PATCH /api/leads/{id}

POST /api/chat
GET /api/leads
```

The final API contract will be documented in:

```text
docs/API_SPEC.md
```

The backend should be responsible for appropriate:

- Request validation.
- Authentication/authorization.
- Business logic.
- Database access.
- Service orchestration where appropriate.
- API responses.
- Error handling.

---

# 19. Frontend Requirements

The frontend will use:

**React**

The initial interface should provide:

### Customer Interface

- Chat interface.
- Message input.
- Bot responses.
- Loading state.
- Error state.
- Basic lead information capture where required.

### Sales Interface

Potential MVP dashboard functionality:

- Lead list.
- Lead details.
- Lead status.
- Lead score.
- Qualification.
- Customer requirements.
- Follow-up information.

The UI should prioritize usability and clarity over unnecessary visual complexity.

---

# 20. Database Requirements

The system will use a **SQL database as the primary system of record** for durable application data.

The SQL database is intended to provide:

- Structured storage.
- Relationships.
- Querying.
- Data integrity.
- Transaction support.
- Reliable application state.

Google Sheets may be used by n8n for operational workflows such as:

- Simple sales-team visibility.
- Reporting.
- Export.
- Temporary operational workflows.
- Early-stage demonstrations.

Google Sheets should not automatically be treated as the authoritative source for all application data.

The final source-of-truth strategy will be defined in `DATA_MODEL.md` and `SYSTEM_ARCHITECTURE.md`.

---

# 21. AI Requirements

The AI layer should perform tasks that benefit from natural-language understanding.

Primary AI responsibilities:

1. Intent classification.
2. Information extraction.
3. Requirement normalization.
4. Conversation understanding.
5. Missing-information detection.
6. Response generation.
7. Conversation summarization.

AI output should preferably be converted into **structured data** before downstream automation uses it.

Example:

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

The system should validate AI-generated structured output before using it for important operations.

---

# 22. AI Safety and Reliability Requirements

The AI must not:

- Invent customer information.
- Invent property availability.
- Invent prices.
- Invent company policies.
- Make unauthorized changes.
- Expose sensitive information.
- Perform actions outside its permitted tools.

AI decisions that have business consequences should be constrained by application logic and business rules.

Where confidence is low, the system should prefer:

```text
Ask for clarification
        OR
Escalate to human
```

rather than confidently guessing.

---

# 23. Human-in-the-Loop

The system must support human intervention.

Human intervention may be required when:

- AI confidence is low.
- Customer requests something outside the system's capabilities.
- A customer becomes complex or sensitive.
- A high-value lead requires immediate attention.
- The AI cannot safely determine the correct action.
- A business decision requires human approval.

The system should make it clear when automation ends and human follow-up begins.

---

# 24. Non-Functional Requirements

## Performance

The system should provide reasonably fast responses for normal customer interactions.

Target response times will be defined during technical design.

## Reliability

Workflow failures should be detectable and recoverable where possible.

## Scalability

The architecture should be capable of handling increasing lead volume without requiring a complete redesign.

## Maintainability

The system should use clear separation of responsibilities between:

```text
Frontend
Backend
Automation
AI
Database
External Integrations
```

## Observability

Important system events should be logged sufficiently to diagnose:

- API failures.
- Workflow failures.
- AI failures.
- Database failures.
- Integration failures.

## Security

Sensitive credentials must not be stored directly in source code.

Authentication and authorization requirements will be defined in `SECURITY_SPEC.md`.

---

# 25. Error Handling

The system should account for failures including:

### API failure

```text
Frontend
   ↓
FastAPI
   ↓
ERROR
```

The user should receive a meaningful response rather than an application crash.

### AI failure

If AI processing fails:

```text
AI failure
↓
Retry where appropriate
↓
Fallback / human escalation
```

### n8n workflow failure

Failed workflow executions should be observable and retryable where appropriate.

### Database failure

The system should fail safely and avoid falsely telling the customer that a lead has been successfully stored when it has not.

---

# 26. Duplicate Lead Handling

The system should attempt to identify duplicate leads where sufficient information exists.

Potential matching information:

- Email.
- Phone number.
- Customer identity.
- Conversation/session.
- Other business-defined identifiers.

Duplicate handling rules will be defined during technical design.

---

# 27. Data Ownership and Source of Truth

The system should establish clear ownership for each type of information.

Initial principle:

```text
Application Data
        ↓
SQL Database
        ↓
System of Record
```

n8n acts primarily as:

```text
Automation / Orchestration Layer
```

Google Sheets acts primarily as:

```text
Operational / Reporting / Integration Surface
```

AI acts primarily as:

```text
Understanding / Classification / Generation Layer
```

FastAPI acts primarily as:

```text
Application API / Business Logic Layer
```

React acts primarily as:

```text
Presentation / User Interaction Layer
```

---

# 28. Success Criteria

The MVP will be considered successful when the system can reliably complete the core flow:

```text
Customer
↓
React UI
↓
FastAPI
↓
n8n
↓
AI Processing
↓
Structured Lead
↓
SQL Database
↓
Lead Qualification
↓
Sales Notification
↓
Sales Follow-Up
```

The system should demonstrate that:

1. A customer can submit a natural-language enquiry.
2. The system can understand the customer's intent.
3. Relevant information can be extracted.
4. Missing information can be identified.
5. A lead can be created or updated.
6. The lead can be scored.
7. The lead can be stored.
8. An appropriate customer response can be generated.
9. The sales team can be notified.
10. A salesperson can update the lead status.
11. The lead lifecycle can be tracked.
12. Failures can be detected and handled appropriately.

---

# 29. MVP Scope

## Included in MVP

### Customer

- Chat interface.
- Send enquiry.
- Receive automated response.
- Provide additional information.

### AI

- Intent classification.
- Requirement extraction.
- Missing information detection.
- Response generation.
- Conversation summarization.

### Backend

- FastAPI application.
- Lead APIs.
- Validation.
- Database integration.

### Automation

- n8n workflow.
- AI processing.
- Lead processing.
- Qualification.
- Notification.

### Database

- SQL lead storage.
- Customer information.
- Requirements.
- Lead status.
- Qualification.
- Score.

### Sales

- Basic lead visibility.
- Lead status updates.
- Follow-up tracking.

### Google Sheets

- Operational integration/reporting where useful.

---

# 30. Future Scope

Potential future capabilities include:

- WhatsApp integration.
- Email integration.
- Telegram integration.
- Full CRM dashboard.
- Property inventory integration.
- Automated property matching.
- Advanced lead scoring.
- Sales-agent assignment.
- Calendar scheduling.
- Follow-up reminders.
- Analytics dashboard.
- Conversion analytics.
- Multi-agent AI architecture.
- Voice-based lead capture.
- Multi-language support.

These features are outside the initial MVP unless explicitly added to scope.

---

# 31. Core Product Principles

The system should follow these principles.

### Principle 1 — Automation With Human Control

Automate repetitive work while keeping humans responsible for important decisions.

### Principle 2 — Structured Data Over Unstructured Guessing

AI should transform natural language into validated structured data before downstream systems act on it.

### Principle 3 — Clear Separation of Responsibilities

Each layer should have a clear responsibility.

```text
React
→ Presentation

FastAPI
→ Application API / Business Logic

n8n
→ Workflow Orchestration

AI
→ Natural Language Understanding

SQL
→ System of Record

Google Sheets
→ Operational / Reporting Surface
```

### Principle 4 — AI Is Not the Source of Truth

AI-generated information must be treated as an input that can require validation.

### Principle 5 — Fail Safely

When the system cannot confidently determine the correct action, it should ask for clarification or escalate rather than inventing an answer.

### Principle 6 — Build for Change

The architecture and documentation should allow individual components to evolve without unnecessarily rewriting the entire system.

---

# 32. Key Product Terminology

| Term | Meaning |
|---|---|
| Lead | A potential customer/opportunity |
| Lead Source | Where the lead originated |
| Lead Score | Numerical representation of lead priority/value |
| Qualification | Classification of lead quality/priority |
| Intent | What the customer is trying to accomplish |
| Property Requirement | What the customer wants in a property |
| Lead Lifecycle | Stages a lead passes through |
| Workflow | Automated sequence of actions |
| Orchestration | Coordinating multiple systems/actions |
| Agent | AI system capable of reasoning and taking actions |
| AI Tool | Capability available to an AI agent |
| Context | Information available to AI during processing |
| Memory | Information retained across interactions |
| Human-in-the-loop | Human involvement in an automated process |
| API | Interface through which software systems communicate |
| System of Record | Authoritative source of stored business data |
| Validation | Checking whether data meets defined requirements |
| Idempotency | Ability to safely repeat an operation without unintended duplication |
| Observability | Ability to understand system behavior through logs/metrics/traces |
| Fallback | Alternative behavior when the primary process fails |

---

# 33. High-Level Architecture Reference

The initial product architecture is:

```text
                    CUSTOMER
                       │
                       ▼
                ┌──────────────┐
                │    REACT     │
                │  Frontend    │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │   FASTAPI    │
                │ Backend/API  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │     n8n      │
                │ Orchestrator │
                └──────┬───────┘
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           ┌────┐   ┌─────┐   ┌────────────┐
           │ AI │   │ SQL │   │ Google     │
           │    │   │ DB  │   │ Sheets     │
           └────┘   └─────┘   └────────────┘
             │         │
             └────┬────┘
                  ▼
           ┌──────────────┐
           │ Sales Team   │
           └──────────────┘
```

This architecture is a starting point and should be refined during the **System Architecture** phase.

---

# 34. Requirements Traceability

Each major requirement should eventually map to:

```text
PRD
 ↓
Technical Specification
 ↓
Architecture
 ↓
API / Data Model
 ↓
Implementation
 ↓
Tests
```

This allows the team and AI coding agents to determine:

> Why does this piece of code exist?

and:

> Which requirement does this implementation satisfy?

---

# 35. Definition of Done — MVP

The MVP is considered complete when:

- [ ] Customer can submit a message.
- [ ] React receives/displays messages correctly.
- [ ] FastAPI validates incoming requests.
- [ ] n8n receives the appropriate workflow event.
- [ ] AI extracts structured lead information.
- [ ] AI output is validated.
- [ ] Missing information can be identified.
- [ ] Lead is created/updated in SQL.
- [ ] Lead qualification is calculated.
- [ ] Lead score is stored.
- [ ] Customer receives an appropriate response.
- [ ] Sales team receives required notifications.
- [ ] Sales user can view the lead.
- [ ] Sales user can update lead status.
- [ ] Follow-up activity can be recorded.
- [ ] Errors are logged and observable.
- [ ] Basic tests cover critical functionality.
- [ ] Documentation is updated to reflect the implemented system.

---

# 36. Document Dependencies

This PRD is the product-level source of truth.

The following documents will be developed from it:

```text
PRD.md
   │
   ├── SYSTEM_ARCHITECTURE.md
   │
   ├── TECHNICAL_SPEC.md
   │
   ├── API_SPEC.md
   │
   ├── DATA_MODEL.md
   │
   ├── AI_AGENT_SPEC.md
   │
   ├── UI_UX_SPEC.md
   │
   ├── SECURITY_SPEC.md
   │
   └── DEVELOPMENT_GUIDE.md
```

Changes to product scope should first be reflected in the PRD before implementation changes are made.

---

# 37. Current Product Decision Summary

| Area | Initial Decision |
|---|---|
| Product | Real Estate Lead Bot |
| Example Client | PrimeHomes Realty |
| Frontend | React |
| Backend | Python + FastAPI |
| Automation | n8n |
| AI | LLM-based AI processing |
| Primary Database | SQL database |
| Operational Data | Google Sheets where appropriate |
| Customer Interface | React chat interface |
| Sales Interface | Basic lead-management interface |
| Lead Processing | AI + deterministic business rules |
| Qualification | Rule-based scoring |
| Architecture Style | Layered / service-oriented |
| AI Control | Human-in-the-loop |
| Primary Goal | Capture, understand, qualify, route and track leads |
| MVP Priority | Reliability and clear separation of responsibilities |