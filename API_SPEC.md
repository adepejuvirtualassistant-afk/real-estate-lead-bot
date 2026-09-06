# Real Estate Lead Bot — API Specification

**Version:** 1.0  
**Status:** Draft  
**Product:** PrimeHomes Realty Lead Management System

**Related Documents:**
- `PRD.md`
- `SYSTEM_ARCHITECTURE.md`
- `TECHNICAL_SPEC.md`

---

# 1. Purpose

This document defines the API contract for the Real Estate Lead Bot.

The API is the communication layer between the frontend, backend, automation engine, AI services, database, and other system components.

It defines:

- Available endpoints.
- HTTP methods.
- Request formats.
- Response formats.
- Validation rules.
- Error responses.
- Authentication requirements.
- Lead operations.
- Conversation operations.
- Workflow integration.
- API conventions.

The goal is to ensure that developers and AI coding assistants have an explicit contract to follow when building the system.

---

# 2. API Architecture

The initial API architecture is:

```text
React Frontend
      │
      │ HTTPS / JSON
      ▼
FastAPI Backend
      │
      ├── Application Services
      │
      ├── SQL Database
      │
      └── n8n Webhooks
```

The frontend should communicate with the backend rather than directly accessing the database or internal automation infrastructure.

---

# 3. API Base URL

Development:

```text
http://localhost:8000
```

Production:

```text
https://api.example.com
```

The production domain is a placeholder and will be replaced during deployment.

---

# 4. API Versioning

The API should use URL versioning.

Initial version:

```text
/api/v1
```

Example:

```text
/api/v1/leads
```

This allows future versions to be introduced without immediately breaking existing clients.

---

# 5. API Communication Format

The default request and response format is:

```text
JSON
```

Content type:

```text
application/json
```

Example:

```http
Content-Type: application/json
```

---

# 6. General API Principles

The API should follow these principles:

1. Validate all incoming requests.
2. Return predictable response structures.
3. Use appropriate HTTP status codes.
4. Never expose database credentials.
5. Never expose internal secrets.
6. Keep business logic out of route handlers.
7. Use consistent error responses.
8. Validate external and AI-generated data.
9. Support idempotency for critical operations.
10. Document breaking changes.

---

# 7. Core API Resources

The initial API resources are:

```text
/leads
/customers
/conversations
/messages
/follow-ups
/sales-agents
/health
```

Future resources may include:

```text
/properties
/notifications
/users
/analytics
/auth
```

---

# 8. Lead Endpoints

The Lead API manages potential customers and their requirements.

Initial endpoints:

```text
POST   /api/v1/leads
GET    /api/v1/leads
GET    /api/v1/leads/{lead_id}
PATCH  /api/v1/leads/{lead_id}
DELETE /api/v1/leads/{lead_id}
```

Deletion behavior must be finalized before production.

---

# 9. Create Lead

## Endpoint

```http
POST /api/v1/leads
```

## Purpose

Creates a new lead.

## Request

Example:

```json
{
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+2348012345678"
  },
  "intent": "BUYING",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget": {
    "amount": 80000000,
    "currency": "NGN"
  },
  "timeline": "WITHIN_3_MONTHS",
  "source": "WEBSITE"
}
```

---

# 10. Create Lead Response

Successful response:

```http
201 Created
```

Example:

```json
{
  "data": {
    "id": "lead_123",
    "customer_id": "customer_456",
    "status": "NEW",
    "qualification": null,
    "score": null,
    "created_at": "2026-09-06T15:30:00Z"
  }
}
```

---

# 11. Get Leads

## Endpoint

```http
GET /api/v1/leads
```

## Purpose

Returns a list of leads.

Example:

```http
GET /api/v1/leads?status=HOT&page=1&page_size=20
```

Possible filters:

```text
status
qualification
intent
property_type
location
assigned_agent_id
source
created_from
created_to
```

---

# 12. Get Leads Response

Example:

```json
{
  "data": [
    {
      "id": "lead_123",
      "customer": {
        "name": "John Doe",
        "phone": "+2348012345678"
      },
      "intent": "BUYING",
      "property_type": "APARTMENT",
      "location": "Lekki",
      "budget": {
        "amount": 80000000,
        "currency": "NGN"
      },
      "score": 85,
      "qualification": "HOT",
      "status": "QUALIFIED"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1
  }
}
```

---

# 13. Get Single Lead

## Endpoint

```http
GET /api/v1/leads/{lead_id}
```

Example:

```http
GET /api/v1/leads/lead_123
```

## Response

```json
{
  "data": {
    "id": "lead_123",
    "customer_id": "customer_456",
    "intent": "BUYING",
    "property_type": "APARTMENT",
    "bedrooms": 3,
    "location": "Lekki",
    "budget": {
      "amount": 80000000,
      "currency": "NGN"
    },
    "timeline": "WITHIN_3_MONTHS",
    "score": 85,
    "qualification": "HOT",
    "status": "QUALIFIED",
    "assigned_agent_id": null,
    "created_at": "2026-09-06T15:30:00Z",
    "updated_at": "2026-09-06T15:35:00Z"
  }
}
```

---

# 14. Update Lead

## Endpoint

```http
PATCH /api/v1/leads/{lead_id}
```

Only fields supplied in the request should be modified.

Example:

```json
{
  "location": "Ikoyi",
  "budget": {
    "amount": 100000000,
    "currency": "NGN"
  }
}
```

---

# 15. Lead Status Update

Example:

```http
PATCH /api/v1/leads/lead_123
```

Request:

```json
{
  "status": "CONTACTED"
}
```

The backend must validate whether the requested state transition is allowed.

For example:

```text
NEW
 ↓
QUALIFYING
 ↓
QUALIFIED
 ↓
CONTACTED
```

An invalid transition should be rejected.

---

# 16. Lead Qualification Endpoint

The system may expose a dedicated qualification endpoint.

```http
POST /api/v1/leads/{lead_id}/qualify
```

Purpose:

- Calculate lead score.
- Determine qualification.
- Store qualification result.
- Store qualification reasons.

Example response:

```json
{
  "data": {
    "lead_id": "lead_123",
    "score": 85,
    "qualification": "HOT",
    "reasons": [
      "Immediate buying intent",
      "Specific location",
      "Budget provided",
      "Property requirement provided"
    ]
  }
}
```

---

# 17. Customer Endpoints

Initial endpoints:

```text
POST /api/v1/customers
GET  /api/v1/customers
GET  /api/v1/customers/{customer_id}
PATCH /api/v1/customers/{customer_id}
```

---

# 18. Create Customer

## Endpoint

```http
POST /api/v1/customers
```

Example:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+2348012345678"
}
```

Response:

```http
201 Created
```

Example:

```json
{
  "data": {
    "id": "customer_456",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+2348012345678"
  }
}
```

---

# 19. Conversation Endpoints

Initial endpoints:

```text
POST /api/v1/conversations
GET  /api/v1/conversations/{conversation_id}
GET  /api/v1/conversations/{conversation_id}/messages
```

---

# 20. Create Conversation

## Endpoint

```http
POST /api/v1/conversations
```

Example:

```json
{
  "customer_id": "customer_456",
  "channel": "WEB_CHAT"
}
```

Response:

```json
{
  "data": {
    "id": "conv_789",
    "customer_id": "customer_456",
    "channel": "WEB_CHAT",
    "status": "ACTIVE"
  }
}
```

---

# 21. Chat Endpoint

The chat endpoint is one of the most important endpoints in the system.

## Endpoint

```http
POST /api/v1/chat
```

## Purpose

Receives a customer message and starts or continues the lead-processing workflow.

Request:

```json
{
  "conversation_id": "conv_789",
  "message": "Hi, I need a 3-bedroom apartment around Lekki. My budget is about 80 million."
}
```

---

# 22. Chat Processing Flow

The request should follow:

```text
React
  ↓
POST /chat
  ↓
FastAPI
  ↓
Validate Request
  ↓
Persist Message
  ↓
Trigger n8n
  ↓
AI Processing
  ↓
Extract Requirements
  ↓
Validate AI Output
  ↓
Update Lead
  ↓
Calculate Qualification
  ↓
Generate Response
  ↓
Return Response
```

---

# 23. Chat Response

Example:

```json
{
  "data": {
    "conversation_id": "conv_789",
    "message": {
      "id": "msg_100",
      "sender_type": "BOT",
      "content": "Thanks for reaching out. I've noted that you're looking for a 3-bedroom apartment in Lekki with a budget of around ₦80 million. When are you looking to move?",
      "created_at": "2026-09-06T15:40:00Z"
    },
    "lead": {
      "id": "lead_123",
      "status": "QUALIFYING",
      "qualification": "NORMAL"
    }
  }
}
```

---

# 24. Missing Information

The API should support situations where the customer has not provided enough information.

Example:

Customer:

```text
"I want to buy a house."
```

The backend should not invent:

```text
location
budget
bedrooms
timeline
```

Instead, the AI/workflow may respond with clarification questions.

Example response:

```json
{
  "data": {
    "message": {
      "sender_type": "BOT",
      "content": "I'd be happy to help. Which location are you interested in, and what is your approximate budget?"
    },
    "missing_fields": [
      "location",
      "budget"
    ]
  }
}
```

---

# 25. Message Endpoints

## Create Message

```http
POST /api/v1/conversations/{conversation_id}/messages
```

Example:

```json
{
  "content": "I'm looking for something in Lekki.",
  "sender_type": "CUSTOMER"
}
```

---

# 26. Get Conversation Messages

```http
GET /api/v1/conversations/{conversation_id}/messages
```

Example response:

```json
{
  "data": [
    {
      "id": "msg_1",
      "sender_type": "CUSTOMER",
      "content": "I need a 3-bedroom apartment.",
      "created_at": "2026-09-06T15:30:00Z"
    },
    {
      "id": "msg_2",
      "sender_type": "BOT",
      "content": "Which location are you interested in?",
      "created_at": "2026-09-06T15:31:00Z"
    }
  ]
}
```

---

# 27. Follow-Up Endpoints

Initial endpoints:

```text
POST  /api/v1/follow-ups
GET   /api/v1/follow-ups
GET   /api/v1/follow-ups/{follow_up_id}
PATCH /api/v1/follow-ups/{follow_up_id}
```

---

# 28. Create Follow-Up

Example:

```http
POST /api/v1/follow-ups
```

Request:

```json
{
  "lead_id": "lead_123",
  "assigned_agent_id": "agent_001",
  "scheduled_for": "2026-09-08T10:00:00Z",
  "notes": "Call customer about Lekki apartment options."
}
```

---

# 29. Follow-Up Status

Initial statuses:

```text
PENDING
COMPLETED
CANCELLED
MISSED
```

---

# 30. Health Check

## Endpoint

```http
GET /health
```

Purpose:

Determine whether the API is running.

Response:

```json
{
  "status": "ok"
}
```

---

# 31. Readiness Check

A readiness endpoint may be introduced:

```http
GET /health/ready
```

This can verify dependencies such as:

```text
API
Database
Required external services
```

Example:

```json
{
  "status": "ready",
  "dependencies": {
    "database": "ok",
    "n8n": "ok"
  }
}
```

---

# 32. Error Response Standard

All API errors should follow a consistent format.

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request.",
    "details": [
      {
        "field": "message",
        "issue": "Message cannot be empty."
      }
    ]
  }
}
```

---

# 33. HTTP Status Codes

The API should use standard HTTP status codes.

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 202 | Request accepted for processing |
| 204 | Successful request with no response body |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Resource conflict |
| 422 | Validation failure |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 502 | Upstream service failure |
| 503 | Service unavailable |

---

# 34. Validation

FastAPI/Pydantic should validate request schemas.

Validation should include:

- Required fields.
- Data types.
- String lengths.
- Enum values.
- Numeric ranges.
- Email formats.
- Identifier formats.

Example:

```text
bedrooms
```

should not accept:

```json
{
  "bedrooms": "many"
}
```

---

# 35. Pagination

List endpoints should support pagination.

Example:

```http
GET /api/v1/leads?page=1&page_size=20
```

Response:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

---

# 36. Filtering

Example:

```http
GET /api/v1/leads?qualification=HOT
```

Multiple filters:

```http
GET /api/v1/leads?qualification=HOT&intent=BUYING&location=Lekki
```

The exact supported filters will depend on the database implementation.

---

# 37. Sorting

Example:

```http
GET /api/v1/leads?sort_by=created_at&sort_order=desc
```

Supported sorting fields should be explicitly defined by the backend.

Clients should not be allowed to request arbitrary database fields.

---

# 38. Idempotency

Critical POST requests should support an idempotency key where required.

Example:

```http
Idempotency-Key: 7b9f2c4d-1234
```

This helps prevent duplicate operations when requests are retried.

Example:

```text
React
 ↓
POST /leads
 ↓
Network Timeout
 ↓
React retries
 ↓
Same Idempotency-Key
 ↓
Backend recognizes existing operation
 ↓
No duplicate lead
```

---

# 39. Request Correlation

Requests should support a correlation identifier.

Example:

```http
X-Request-ID: req_123456
```

This allows developers to trace a request through:

```text
React
 ↓
FastAPI
 ↓
n8n
 ↓
AI
 ↓
Database
 ↓
Notification
```

---

# 40. FastAPI → n8n Communication

FastAPI may trigger n8n through a webhook.

Conceptual flow:

```text
FastAPI
   ↓
POST n8n Webhook
   ↓
n8n Workflow
```

Example payload:

```json
{
  "event": "lead.message_received",
  "request_id": "req_123456",
  "conversation_id": "conv_789",
  "message_id": "msg_100",
  "message": "I need a 3-bedroom apartment in Lekki."
}
```

---

# 41. Event Naming

Internal events should use predictable names.

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

# 42. n8n Response

n8n should return a predictable result to FastAPI when synchronous processing is used.

Example:

```json
{
  "success": true,
  "data": {
    "lead_id": "lead_123",
    "qualification": "HOT",
    "score": 85,
    "response": "Thanks for reaching out..."
  }
}
```

---

# 43. Asynchronous Processing

If AI processing becomes too slow for a synchronous API request, the architecture may move to asynchronous processing.

Instead of:

```text
POST /chat
   ↓
Wait
   ↓
AI
   ↓
Response
```

the system may use:

```text
POST /chat
   ↓
202 Accepted
   ↓
Workflow Processing
   ↓
Result
```

The frontend can then receive the result through polling, WebSockets, Server-Sent Events, or another appropriate mechanism.

This decision will be made based on performance requirements.

---

# 44. Authentication

Protected endpoints should require authentication.

Example:

```http
Authorization: Bearer <token>
```

The exact authentication provider and token strategy are not yet finalized.

Authentication details will be defined in:

```text
docs/SECURITY_SPEC.md
```

---

# 45. Authorization

Authentication answers:

> Who are you?

Authorization answers:

> What are you allowed to do?

Example:

```text
Sales Agent
→ View assigned leads

Sales Manager
→ View team leads

Admin
→ Manage all leads
```

The backend must enforce authorization.

---

# 46. Customer Chat Security

Customer-facing chat endpoints should not expose internal data.

For example, the customer should not receive:

```text
Internal lead score
Internal sales notes
Agent performance information
Database identifiers unnecessarily
Internal workflow details
```

---

# 47. API Security Rules

The API must:

- Validate all inputs.
- Authenticate protected endpoints.
- Authorize operations.
- Rate-limit public endpoints where necessary.
- Protect secrets.
- Avoid sensitive information in logs.
- Use HTTPS in production.
- Validate webhook authentication.
- Reject malformed requests.

---

# 48. n8n Webhook Security

n8n webhook endpoints should not be publicly trusted without authentication or verification.

Possible mechanisms include:

```text
Secret Header
API Key
HMAC Signature
Authenticated Service Request
```

The final mechanism will be selected during security design.

---

# 49. API and Database Separation

The frontend must not directly access the SQL database.

Correct:

```text
React
 ↓
FastAPI
 ↓
SQL
```

Incorrect:

```text
React
 ↓
SQL Database
```

This protects business logic and sensitive data.

---

# 50. API and Google Sheets Separation

The frontend should also not directly manipulate the operational Google Sheet.

Preferred architecture:

```text
React
 ↓
FastAPI
 ↓
n8n
 ↓
Google Sheets
```

or:

```text
SQL
 ↓
n8n
 ↓
Google Sheets
```

---

# 51. API Contract Ownership

The backend team owns the authoritative API contract.

If the frontend requires a new field:

```text
Frontend Requirement
        ↓
API Contract Change
        ↓
FastAPI
        ↓
Tests
        ↓
Documentation
```

The frontend should not assume undocumented fields exist.

---

# 52. API Schema Management

FastAPI should use typed schemas.

Conceptually:

```text
backend/
└── app/
    └── schemas/
        ├── lead.py
        ├── customer.py
        ├── conversation.py
        ├── message.py
        └── follow_up.py
```

Pydantic models should define request and response contracts.

---

# 53. Example Lead Schema

Conceptual:

```python
class LeadCreate:
    customer_id: str
    intent: Intent
    property_type: PropertyType
    bedrooms: int | None
    location: str | None
    budget: Budget | None
    timeline: Timeline | None
```

The actual implementation should use appropriate Pydantic syntax and validation.

---

# 54. API Documentation

FastAPI should automatically expose interactive API documentation.

Expected development endpoints:

```text
/docs
/redoc
```

These should be available during development.

Production exposure should follow the project's security policy.

---

# 55. API Testing

Each endpoint should have automated tests.

Example:

```text
tests/
└── api/
    ├── test_leads.py
    ├── test_customers.py
    ├── test_chat.py
    ├── test_conversations.py
    └── test_followups.py
```

Tests should cover:

- Valid requests.
- Invalid requests.
- Missing fields.
- Unauthorized requests.
- Forbidden operations.
- Not-found resources.
- Duplicate requests.
- Service failures.

---

# 56. Example End-to-End API Scenario

Customer sends:

```text
"Hi, I need a 3-bedroom apartment in Lekki. My budget is 80m."
```

Flow:

```text
React
 ↓
POST /api/v1/chat
 ↓
FastAPI
 ↓
Validate request
 ↓
Store message
 ↓
Trigger n8n
 ↓
AI extracts:
   property_type = APARTMENT
   bedrooms = 3
   location = Lekki
   budget = 80,000,000 NGN
 ↓
Validate AI output
 ↓
Update Lead
 ↓
Calculate Score
 ↓
Store Lead
 ↓
Generate Response
 ↓
FastAPI
 ↓
React
```

---

# 57. Example API Response

```json
{
  "data": {
    "conversation_id": "conv_789",
    "message": {
      "sender_type": "BOT",
      "content": "Thanks! I've noted your requirement for a 3-bedroom apartment in Lekki with a budget of around ₦80 million. When are you looking to buy?",
      "created_at": "2026-09-06T16:00:00Z"
    },
    "lead": {
      "id": "lead_123",
      "status": "QUALIFYING",
      "qualification": "NORMAL",
      "score": 45,
      "missing_fields": [
        "timeline"
      ]
    }
  }
}
```

---

# 58. API Contract Rules for AI Coding Assistants

AI coding assistants must follow this document when generating API code.

Before creating or modifying an endpoint, the agent should check:

```text
1. Does the endpoint already exist?
2. What HTTP method should it use?
3. What request schema is required?
4. What response schema is required?
5. What authentication is required?
6. What authorization is required?
7. What errors are possible?
8. What database entities are involved?
9. Does n8n need to be triggered?
10. What tests must be updated?
```

An AI coding assistant should not invent new API conventions when an existing convention is documented.

---

# 59. Breaking Changes

A change is considered breaking if it:

- Removes an endpoint.
- Changes an HTTP method.
- Removes a required response field.
- Changes a field type.
- Changes authentication behavior.
- Changes the meaning of an existing field.
- Removes a supported enum value.

Breaking changes require:

1. Documentation update.
2. Test updates.
3. Frontend impact review.
4. n8n impact review.
5. Migration plan where required.

---

# 60. API Development Checklist

Before considering an endpoint complete:

- [ ] Endpoint documented.
- [ ] Request schema defined.
- [ ] Response schema defined.
- [ ] Validation implemented.
- [ ] Authentication implemented if required.
- [ ] Authorization implemented if required.
- [ ] Business logic delegated to services.
- [ ] Database interaction implemented.
- [ ] Error handling implemented.
- [ ] Logging implemented where appropriate.
- [ ] Unit tests added.
- [ ] API tests added.
- [ ] OpenAPI documentation updated.
- [ ] Related n8n workflows updated.
- [ ] Frontend integration tested.

---

# 61. Current API Status

## Defined

- [x] API architecture.
- [x] API versioning.
- [x] JSON communication.
- [x] Lead endpoints.
- [x] Customer endpoints.
- [x] Conversation endpoints.
- [x] Message endpoints.
- [x] Follow-up endpoints.
- [x] Chat endpoint.
- [x] Health endpoint.
- [x] Error format.
- [x] Pagination concept.
- [x] Filtering concept.
- [x] Idempotency concept.
- [x] Request tracing concept.
- [x] n8n integration concept.

## To Finalize

- [ ] Authentication provider.
- [ ] Authorization roles.
- [ ] Complete request schemas.
- [ ] Complete response schemas.
- [ ] Exact database schema.
- [ ] Exact n8n webhook contracts.
- [ ] Webhook authentication.
- [ ] Rate limits.
- [ ] Production API domain.
- [ ] Asynchronous processing strategy.
- [ ] API deprecation policy.

---

# 62. Relationship With Other Documents

```text
PRD.md
  │
  │ Defines WHAT
  ▼
SYSTEM_ARCHITECTURE.md
  │
  │ Defines WHERE components live
  ▼
TECHNICAL_SPEC.md
  │
  │ Defines HOW components are implemented
  ▼
API_SPEC.md
  │
  │ Defines HOW components communicate
  ▼
DATA_MODEL.md
  │
  │ Defines HOW data is structured
  ▼
AI_AGENT_SPEC.md
  │
  │ Defines HOW AI behaves
  ▼
Implementation
```

---

# 63. Engineering Principle

The API is a **contract**, not merely a collection of URLs.

Every API contract should clearly define:

```text
INPUT
  ↓
VALIDATION
  ↓
PROCESSING
  ↓
OUTPUT
  ↓
ERRORS
```

This makes the system easier for:

- Human developers.
- Frontend developers.
- Backend developers.
- n8n builders.
- AI agents.
- Coding assistants.
- QA engineers.

to understand and extend safely.