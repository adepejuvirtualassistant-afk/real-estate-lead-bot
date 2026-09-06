# n8n Workflow Specification

## 1. Purpose

This document defines the automation workflows for the **Real Estate Lead Bot** using **n8n**.

n8n acts as the **workflow orchestration layer** of the system.

It connects:

- FastAPI
- AI services
- SQL database
- Google Sheets
- Email
- Slack or other notifications
- Calendar/follow-up systems
- Sales team workflows

The purpose of this document is to make the automation behavior explicit and reproducible.

---

# 2. Role of n8n

n8n is responsible for **orchestrating processes**, not owning the application's core business data.

The architecture is:

```text
React
   ↓
FastAPI
   ↓
n8n
   ↓
AI / Integrations
   ↓
FastAPI / SQL
   ↓
Sales Team
```

### n8n should handle

- Workflow orchestration
- Webhook triggers
- AI service calls
- Notifications
- Google Sheets synchronization
- Follow-up automation
- External integrations
- Retry logic
- Error workflows
- Scheduled jobs

### n8n should NOT become

- The primary database
- The only place business rules exist
- The frontend backend
- A replacement for FastAPI
- A place to store secrets in plain text

---

# 3. Source of Truth

The system follows this rule:

```text
SQL Database
     ↓
PRIMARY SOURCE OF TRUTH
```

n8n reads from and writes to the backend/database through controlled interfaces.

Google Sheets is secondary:

```text
SQL
 ↓
n8n
 ↓
Google Sheets
```

Google Sheets should primarily support:

- Reporting
- Operational visibility
- Simple sales-team access
- Manual review
- Exporting

---

# 4. Workflow Naming Convention

Workflows should use descriptive names.

Recommended naming:

```text
REAL ESTATE - Lead Intake
REAL ESTATE - Lead AI Processing
REAL ESTATE - Lead Qualification
REAL ESTATE - Sales Notification
REAL ESTATE - Google Sheets Sync
REAL ESTATE - Follow-Up
REAL ESTATE - Error Handler
```

Avoid names such as:

```text
Workflow 1
Test
New Workflow
AI Thing
```

A workflow name should explain its business purpose.

---

# 5. Core Workflows

The MVP should contain these workflows:

```text
1. Lead Intake
2. Lead AI Processing
3. Lead Qualification
4. Sales Notification
5. Google Sheets Synchronization
6. Follow-Up Automation
7. Error Handling
```

---

# 6. Workflow 1 — Lead Intake

## Purpose

Receive a customer message from FastAPI and begin the lead-processing pipeline.

### Trigger

FastAPI sends an authenticated webhook request to n8n.

```text
POST /webhook/lead-message
```

### Input

Example:

```json
{
  "event": "lead.message_received",
  "request_id": "req_123456",
  "conversation_id": "conv_789",
  "message_id": "msg_100",
  "lead_id": "lead_456",
  "message": "I need a 3-bedroom apartment in Lekki."
}
```

---

# 7. Lead Intake Flow

```text
Webhook
   ↓
Validate Request
   ↓
Check Required Fields
   ↓
Load Lead Context
   ↓
Load Conversation Context
   ↓
Send to AI Processing
```

### Node sequence

```text
1. Webhook
2. Validate Input
3. IF - Valid Request?
4. HTTP Request - Get Lead
5. HTTP Request - Get Conversation
6. Execute Workflow - AI Processing
```

---

# 8. Lead Intake Validation

Required fields:

```text
event
request_id
conversation_id
message_id
message
```

If `lead_id` exists, it should also be validated.

Invalid request:

```json
{
  "error": "Missing required field: message"
}
```

The workflow should stop processing invalid requests.

---

# 9. Idempotency

The workflow must avoid processing the same message multiple times.

The primary identifier should be:

```text
message_id
```

Conceptually:

```text
Receive message
      ↓
Check whether message_id was processed
      ↓
YES → Stop duplicate processing
      ↓
NO → Continue
```

This protects against:

- Duplicate webhooks
- Network retries
- n8n retries
- FastAPI retries

---

# 10. Workflow 2 — Lead AI Processing

## Purpose

Use AI to understand the customer's message and produce structured lead information.

### Input

```json
{
  "lead": {},
  "conversation": {},
  "message": {},
  "context": {}
}
```

---

# 11. AI Processing Flow

```text
Receive Context
      ↓
Prepare AI Input
      ↓
Call AI Model
      ↓
Parse AI Response
      ↓
Validate Structured Output
      ↓
Check Confidence
      ↓
Return AI Result
```

### Node sequence

```text
1. Execute Workflow Trigger
2. Set / Code - Prepare AI Context
3. AI Model
4. Structured Output Parser
5. Code - Validate Result
6. IF - Valid?
7. Return Result
```

---

# 12. AI Input

The AI should receive:

```text
Customer information
Existing lead information
Recent conversation history
Current customer message
Known requirements
Business rules
Output schema
```

Example:

```json
{
  "current_message": "I need a 3-bedroom apartment in Lekki.",
  "existing_lead": {
    "intent": "BUY"
  },
  "conversation_summary": "Customer is looking for a property in Lagos."
}
```

---

# 13. AI Output

The expected structured output is:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": null,
  "budget_max": null,
  "currency": "NGN",
  "timeline": "UNKNOWN",
  "missing_fields": [
    "budget",
    "timeline"
  ],
  "confidence": 0.94,
  "response": "Thanks! What's your approximate budget and when are you hoping to buy?"
}
```

---

# 14. AI Output Validation

The workflow must validate:

```text
intent
property_type
bedrooms
location
budget
currency
timeline
missing_fields
confidence
response
```

Invalid output must not continue directly to the database.

```text
AI Output
    ↓
Validation
    ↓
Invalid
    ↓
Error Handler / Retry
```

---

# 15. Workflow 3 — Lead Qualification

## Purpose

Determine how valuable or urgent a lead is.

The workflow receives validated lead information.

```text
Lead Data
   ↓
Qualification Rules
   ↓
Calculate Score
   ↓
Classification
   ↓
Save Qualification
```

---

# 16. Qualification Flow

```text
Receive Lead
      ↓
Check Intent
      ↓
Check Requirements
      ↓
Check Budget
      ↓
Check Timeline
      ↓
Calculate Score
      ↓
Classify Lead
      ↓
Save Result
```

---

# 17. Example Qualification

Customer:

```text
3-bedroom apartment
Lekki
₦80M budget
Buying immediately
```

Possible result:

```json
{
  "score": 92,
  "classification": "HOT",
  "reasons": [
    "Clear buying intent",
    "Specific property requirement",
    "Budget provided",
    "Immediate timeline"
  ]
}
```

---

# 18. Qualification Routing

```text
                 Qualification
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
         HOT          WARM         COLD
          │            │            │
          ↓            ↓            ↓
   Sales Alert    Standard     Nurture
                  Follow-up    Workflow
```

---

# 19. HOT Lead Workflow

For a HOT lead:

```text
HOT
 ↓
Save Qualification
 ↓
Assign Sales Agent
 ↓
Create Follow-Up
 ↓
Notify Sales Team
 ↓
Sync to Google Sheets
```

Possible notification channels:

- Email
- Slack
- Microsoft Teams
- Other configured sales channels

The exact notification provider can be decided later.

---

# 20. WARM Lead Workflow

For a WARM lead:

```text
WARM
 ↓
Save Qualification
 ↓
Assign or Queue Lead
 ↓
Create Standard Follow-Up
 ↓
Sync to Google Sheets
```

The sales team may receive a less urgent notification.

---

# 21. COLD Lead Workflow

For a COLD lead:

```text
COLD
 ↓
Save Qualification
 ↓
Add to Nurture / Follow-Up Queue
 ↓
Sync to Google Sheets
```

The system should not treat every low-intent enquiry as a high-priority sales alert.

---

# 22. Workflow 4 — Sales Notification

## Purpose

Notify the sales team when a lead requires attention.

### Trigger

A `lead.qualified` event.

Example:

```json
{
  "event": "lead.qualified",
  "lead_id": "lead_456",
  "classification": "HOT",
  "score": 92
}
```

---

# 23. Sales Notification Flow

```text
Qualification Event
       ↓
Check Classification
       ↓
HOT?
       ↓
YES
       ↓
Get Lead Details
       ↓
Get Assigned Agent
       ↓
Build Notification
       ↓
Send Notification
       ↓
Log Event
```

---

# 24. Sales Notification Example

Example message:

```text
🔥 HOT LEAD

Customer: John Doe
Intent: Buy
Property: 3-bedroom apartment
Location: Lekki
Budget: ₦80M
Timeline: Immediate
Lead Score: 92

Please follow up as soon as possible.
```

Internal lead scores should **not** be exposed to the customer.

---

# 25. Workflow 5 — Google Sheets Synchronization

## Purpose

Maintain an operational view of leads in Google Sheets.

### Flow

```text
Lead Created / Updated
       ↓
n8n
       ↓
Transform Lead Data
       ↓
Google Sheets
```

---

# 26. Google Sheets Columns

Recommended columns:

```text
Lead ID
Customer Name
Email
Phone
Intent
Property Type
Bedrooms
Location
Budget Min
Budget Max
Currency
Timeline
Lead Score
Classification
Lead Status
Assigned Agent
Created At
Updated At
```

---

# 27. Sync Direction

Default:

```text
SQL
 ↓
n8n
 ↓
Google Sheets
```

This is the preferred direction.

If two-way editing is introduced later:

```text
Google Sheets
 ↓
n8n
 ↓
Validate
 ↓
FastAPI
 ↓
SQL
```

The backend remains the authority.

---

# 28. Google Sheets Duplicate Prevention

Use:

```text
Lead ID
```

as the unique reference.

The workflow should:

```text
Search for Lead ID
       ↓
Found?
 ┌─────┴─────┐
YES         NO
 ↓           ↓
Update      Create
```

This prevents duplicate spreadsheet rows.

---

# 29. Workflow 6 — Follow-Up Automation

## Purpose

Ensure qualified leads receive timely follow-up.

Possible follow-up types:

```text
CALL
EMAIL
WHATSAPP
PROPERTY_LISTING
VIEWING
GENERAL_FOLLOW_UP
```

---

# 30. Follow-Up Flow

```text
Lead Qualified
      ↓
Determine Follow-Up Type
      ↓
Create Follow-Up
      ↓
Assign Sales Agent
      ↓
Schedule Follow-Up
      ↓
Wait / Schedule Trigger
      ↓
Check Status
      ↓
Send Reminder
```

---

# 31. Follow-Up Reminder

Example:

```text
Follow-up scheduled
       ↓
Scheduled time reached
       ↓
Is follow-up completed?
       ↓
NO
       ↓
Send reminder
```

The workflow should not repeatedly remind an agent indefinitely.

A maximum retry/reminder policy should be defined.

---

# 32. Follow-Up Escalation

Example:

```text
Reminder 1
   ↓
No completion
   ↓
Reminder 2
   ↓
No completion
   ↓
Escalate to Sales Manager
```

This ensures important leads do not disappear from the pipeline.

---

# 33. Workflow 7 — Error Handling

## Purpose

Provide centralized handling for workflow failures.

Potential failures:

```text
Invalid webhook
AI timeout
AI invalid response
API unavailable
Database unavailable
Google Sheets failure
Notification failure
Authentication failure
Rate limit
```

---

# 34. Error Workflow

```text
Workflow Error
      ↓
Capture Error
      ↓
Capture Request ID
      ↓
Capture Workflow
      ↓
Capture Lead ID
      ↓
Determine Error Type
      ↓
Retry?
 ┌────┴────┐
YES        NO
 ↓          ↓
Retry    Log + Alert
```

---

# 35. Error Logging

Each error should capture useful metadata:

```json
{
  "request_id": "req_123",
  "workflow": "REAL ESTATE - Lead AI Processing",
  "lead_id": "lead_456",
  "error_type": "AI_TIMEOUT",
  "message": "AI provider did not respond.",
  "timestamp": "2026-09-06T12:00:00Z"
}
```

---

# 36. Retry Strategy

Not every error should be retried.

### Retryable

```text
Temporary network error
Temporary API failure
Rate limit
Timeout
```

### Usually not retryable

```text
Invalid input
Invalid credentials
Invalid schema
Missing required data
Business rule violation
```

---

# 37. Retry Limits

Never create infinite retries.

Example:

```text
Attempt 1
 ↓
Wait
 ↓
Attempt 2
 ↓
Wait
 ↓
Attempt 3
 ↓
Fail
 ↓
Error Handler
```

The maximum retry count should be explicitly configured.

---

# 38. Main End-to-End Workflow

The complete customer journey should look like:

```text
CUSTOMER
   │
   ▼
React Chat
   │
   ▼
FastAPI
   │
   ▼
Lead Intake
   │
   ▼
Validate
   │
   ▼
Load Context
   │
   ▼
AI Processing
   │
   ▼
Validate AI Output
   │
   ▼
Update Lead
   │
   ▼
Qualification
   │
   ▼
┌──────────────┬──────────────┬──────────────┐
│              │              │
HOT           WARM           COLD
│              │              │
▼              ▼              ▼
Alert       Follow-up       Nurture
│              │              │
└──────────────┴──────────────┘
               │
               ▼
       Google Sheets Sync
               │
               ▼
          Sales Team
```

---

# 39. Event-Driven Architecture

The workflows should use meaningful events.

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

Example:

```text
lead.qualified
      ↓
Sales Notification
      +
Google Sheets Sync
      +
Follow-Up Creation
```

This reduces tightly coupled workflows.

---

# 40. Webhook Security

FastAPI → n8n webhook requests must be authenticated.

Possible approaches:

```text
API Key
Secret Header
HMAC Signature
Authenticated Service Token
```

The final implementation should select one method.

Do not expose unauthenticated production webhooks for sensitive operations.

---

# 41. Environment Variables

Secrets must not be hard-coded.

Example:

```text
N8N_WEBHOOK_SECRET
AI_API_KEY
DATABASE_URL
GOOGLE_SHEETS_CREDENTIAL
SLACK_CREDENTIAL
```

Credentials should be managed through secure n8n credentials or environment configuration.

Never commit secrets to Git.

---

# 42. Data Transformation

n8n may transform data between services.

Example:

```text
FastAPI Format
      ↓
n8n Transformation
      ↓
AI Format
      ↓
AI Output
      ↓
Backend Format
```

Transformation logic should be documented.

Avoid unnecessary transformations.

---

# 43. n8n and FastAPI Responsibility Boundary

### FastAPI owns

```text
API validation
Business logic
Database access
Authentication/authorization
Core application state
```

### n8n owns

```text
Workflow orchestration
External integrations
Notifications
Scheduled processes
AI orchestration
Operational automation
```

This boundary should remain clear.

---

# 44. n8n and AI Responsibility Boundary

### AI owns

```text
Natural-language understanding
Extraction
Classification
Response generation
```

### n8n owns

```text
Calling AI
Passing context
Handling AI failures
Routing AI output
Triggering next workflow
```

### Backend owns

```text
Validating AI output
Persisting official state
Enforcing business rules
```

---

# 45. Workflow Modularity

Do not build one giant n8n workflow containing everything.

Prefer:

```text
Lead Intake
     ↓
AI Processing
     ↓
Qualification
     ↓
Sales Notification
     ↓
Follow-Up
     ↓
Sheets Sync
```

This makes workflows:

- Easier to debug
- Easier to test
- Easier to modify
- Easier for AI coding assistants to understand
- Easier to reuse

---

# 46. Workflow Inputs and Outputs

Every reusable workflow should have a clearly defined input and output.

Example:

### AI Processing

Input:

```json
{
  "lead_id": "lead_123",
  "message": "I need a house in Lekki.",
  "conversation_history": []
}
```

Output:

```json
{
  "intent": "BUY",
  "property_type": "HOUSE",
  "location": "Lekki",
  "missing_fields": [
    "budget"
  ],
  "response": "What's your approximate budget?"
}
```

---

# 47. Workflow Testing

Each workflow should be tested independently.

### Lead Intake

Test:

```text
Valid request
Missing message
Missing lead ID
Duplicate message
Invalid authentication
```

### AI Processing

Test:

```text
Normal message
Vague message
Missing information
Multiple requirements
Malformed AI response
AI timeout
```

### Qualification

Test:

```text
HOT
WARM
COLD
Boundary scores
Missing budget
Missing timeline
```

### Google Sheets

Test:

```text
Create row
Update row
Duplicate prevention
Google API failure
```

### Notifications

Test:

```text
HOT notification
WARM notification
Invalid recipient
Notification provider failure
```

---

# 48. Observability

Every important workflow should provide traceability.

Use:

```text
request_id
lead_id
conversation_id
message_id
workflow name
execution ID
timestamp
```

This allows debugging across:

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
```

---

# 49. Performance Considerations

The system should avoid unnecessary sequential operations.

For example, after lead data has been saved:

```text
Google Sheets Sync
        │
Sales Notification
        │
Analytics
```

may be executed independently where appropriate.

However, operations that depend on previous results must remain sequential.

---

# 50. Failure Principle

A failure in one secondary integration should not necessarily destroy the lead.

Example:

```text
Lead saved successfully
       ↓
Google Sheets fails
       ↓
Lead remains safe in SQL
       ↓
Sheets sync retried later
```

The system should prioritize preserving core business data.

---

# 51. Workflow Versioning

Major workflow changes should be documented.

Example:

```text
Lead Intake v1
Lead Intake v2
```

When changing a workflow:

```text
Review impact
 ↓
Update specification
 ↓
Test
 ↓
Deploy
 ↓
Monitor
```

Do not make undocumented production changes.

---

# 52. Agentic AI Development Rules

AI coding assistants working on n8n workflows must follow these rules.

### Rule 1

Read:

```text
PRD.md
SYSTEM_ARCHITECTURE.md
TECHNICAL_SPEC.md
API_SPEC.md
DATA_MODEL.md
AI_AGENT_SPEC.md
N8N_WORKFLOW_SPEC.md
```

before making major workflow changes.

### Rule 2

Do not create a new workflow if an existing reusable workflow can handle the requirement.

### Rule 3

Do not bypass FastAPI to modify core SQL data directly unless explicitly designed and documented.

### Rule 4

Do not hard-code credentials.

### Rule 5

Do not create infinite loops.

### Rule 6

Every external API call must have appropriate error handling.

### Rule 7

Every AI output must be validated before becoming authoritative system data.

### Rule 8

Update this document when workflow behavior changes significantly.

---

# 53. MVP Workflow Checklist

Before considering the automation MVP complete:

- [ ] Lead Intake workflow works
- [ ] Webhook authentication works
- [ ] Duplicate message prevention works
- [ ] AI Processing workflow works
- [ ] AI output validation works
- [ ] Lead Qualification works
- [ ] HOT/WARM/COLD routing works
- [ ] Sales notification works
- [ ] Follow-up creation works
- [ ] Google Sheets synchronization works
- [ ] Error workflow works
- [ ] Retry limits are configured
- [ ] Execution logging works
- [ ] Secrets are securely stored
- [ ] Workflows are documented
- [ ] Workflows have been tested with realistic lead messages

---

# 54. Final Architecture Principle

n8n should function as the **orchestration engine**, not as the entire application.

The system should follow:

```text
React
  ↓
FastAPI
  ↓
n8n
  ↓
AI + Integrations
  ↓
FastAPI
  ↓
SQL
```

With:

```text
Google Sheets
      ↑
     n8n
```

as an operational/reporting layer.

The goal is not to create the largest n8n workflow.

The goal is to create a **reliable, modular, observable, and maintainable automation system** that can grow with the business.