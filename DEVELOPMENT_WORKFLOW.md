# DEVELOPMENT WORKFLOW

## 1. Document Purpose

This document defines the development process for the **PrimeHomes Realty Real Estate Lead Bot**.

It explains how developers and AI coding assistants should work on the project from the first code change through testing, review, integration, and completion.

The project contains several interconnected systems:

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
Integrations
```

Because changes in one component can affect other components, development must follow a controlled workflow.

The goal is to make development:

- Organized
- Predictable
- Collaborative
- Testable
- Easy to review
- Easy for AI coding assistants to understand
- Resistant to accidental architectural changes

---

# 2. Core Development Principle

The project should be developed in **small, verifiable increments**.

Use:

```text
Understand
   ↓
Plan
   ↓
Implement
   ↓
Test
   ↓
Review
   ↓
Document
   ↓
Commit
```

Avoid:

```text
Large Prompt
   ↓
Huge Code Change
   ↓
Many Unknown Errors
```

Small changes make problems easier to identify and fix.

---

# 3. Source of Truth

The project documentation is the primary source of truth for implementation decisions.

Before making changes, consult the relevant document.

```text
Product requirement
→ PRD.md

System architecture
→ SYSTEM_ARCHITECTURE.md

Technical implementation
→ TECHNICAL_SPEC.md

API behavior
→ API_SPEC.md

Database structure
→ DATA_MODEL.md

AI behavior
→ AI_AGENT_SPEC.md

n8n workflows
→ N8N_WORKFLOW_SPEC.md

Frontend behavior
→ UI_UX_SPEC.md

Testing
→ TESTING_STRATEGY.md

Build sequence
→ IMPLEMENTATION_PLAN.md
```

Code should follow these documents.

If the code and documentation disagree, the discrepancy should be investigated rather than silently choosing one.

---

# 4. Development Lifecycle

Each feature should move through the following lifecycle:

```text
Requirement
    ↓
Design
    ↓
Task
    ↓
Implementation
    ↓
Unit Test
    ↓
Integration Test
    ↓
Review
    ↓
Documentation
    ↓
Commit
```

For larger features:

```text
Requirement
    ↓
Architecture Review
    ↓
Implementation
    ↓
Testing
    ↓
Integration
    ↓
End-to-End Validation
```

---

# 5. Start With the Requirement

Before writing code, identify:

- What problem are we solving?
- Who is affected?
- What should the system do?
- What should the system NOT do?
- Which component owns the behavior?
- What existing documentation defines the requirement?
- What tests will prove that it works?

Example:

### Requirement

> Customers should be able to send property requirements through the chatbot.

Relevant documents:

```text
PRD.md
UI_UX_SPEC.md
API_SPEC.md
AI_AGENT_SPEC.md
TESTING_STRATEGY.md
```

Affected components:

```text
React
FastAPI
n8n
AI
Database
```

---

# 6. Convert Requirements Into Small Tasks

Do not turn one large requirement into one enormous coding task.

Instead:

```text
Customer Chat
    ↓
Create chat UI
    ↓
Create chat API
    ↓
Create conversation model
    ↓
Create message model
    ↓
Connect UI to API
    ↓
Connect API to n8n
    ↓
Add AI processing
    ↓
Test complete conversation
```

Each task should ideally have a clear beginning and end.

---

# 7. Task Definition Format

Each development task should contain:

```text
Task:
What needs to be built?

Why:
Why is it needed?

Files:
Which files are expected to change?

Dependencies:
What must already exist?

Behavior:
What should happen?

Validation:
How will we know it works?

Tests:
What tests are required?

Documentation:
Does any documentation need updating?
```

Example:

```text
Task:
Implement POST /api/v1/leads.

Why:
Allow the frontend and integrations to create leads.

Dependencies:
Database Lead model.

Behavior:
Validate input and persist the lead.

Validation:
Return HTTP 201 for successful creation.

Tests:
Valid request, invalid request, duplicate request.
```

---

# 8. Work in Vertical Slices

Whenever possible, build a small feature from beginning to end rather than completing one technical layer entirely before touching another.

Example:

```text
Lead Creation Slice

React Form
   ↓
FastAPI Endpoint
   ↓
Validation
   ↓
SQL
   ↓
Response
   ↓
Frontend Confirmation
```

This creates a working feature quickly and exposes integration problems early.

---

# 9. Avoid Building Everything in Isolation

Do not spend too long building:

```text
100% React
```

before checking whether:

```text
React → FastAPI
```

actually works.

Similarly, do not build a large n8n workflow before verifying:

```text
FastAPI → n8n
```

The preferred approach is:

```text
Build
 ↓
Connect
 ↓
Test
 ↓
Expand
```

---

# 10. Backend Development Workflow

For a FastAPI feature:

```text
Requirement
   ↓
Pydantic Schema
   ↓
API Route
   ↓
Service Logic
   ↓
Database
   ↓
Tests
```

The API route should not contain all business logic.

Prefer:

```text
Route
  ↓
Service
  ↓
Repository / Database
```

rather than putting everything into one large route function.

---

# 11. Frontend Development Workflow

For a React feature:

```text
UI Requirement
   ↓
Component
   ↓
State
   ↓
API Service
   ↓
Loading/Error States
   ↓
Tests
```

Example:

```text
ChatInput
   ↓
useChat()
   ↓
api.js
   ↓
FastAPI /chat
```

Components should remain focused on presentation and interaction.

---

# 12. n8n Development Workflow

Each n8n workflow should be developed independently.

Example:

```text
Lead Intake Workflow
```

Development process:

```text
Define Trigger
   ↓
Define Input Schema
   ↓
Build Nodes
   ↓
Add Validation
   ↓
Add Error Handling
   ↓
Test With Fixture
   ↓
Connect To Next Workflow
```

Do not create one enormous n8n workflow containing the entire application.

---

# 13. AI Development Workflow

AI behavior should be developed separately from deterministic application logic.

Use:

```text
Customer Message
    ↓
AI
    ↓
Structured Output
    ↓
Validation
    ↓
Business Logic
```

Do not allow:

```text
Customer Message
    ↓
AI
    ↓
Direct Database Write
```

The AI is an interpreter, not the ultimate authority over application state.

---

# 14. AI Prompt Development

When modifying an AI prompt:

1. Identify the behavior being changed.
2. Update the prompt.
3. Run golden test cases.
4. Run structured-output tests.
5. Run safety tests.
6. Compare results with the previous version.
7. Update the prompt version.
8. Document meaningful behavior changes.

Example:

```text
Prompt v1
   ↓
Test
   ↓
Prompt v2
   ↓
Regression Test
   ↓
Evaluation
```

---

# 15. Database Development Workflow

Database changes must follow:

```text
Requirement
   ↓
DATA_MODEL.md
   ↓
Migration
   ↓
Model
   ↓
Repository/Service
   ↓
Tests
```

Never make undocumented schema changes casually.

If the database model changes significantly, update:

```text
DATA_MODEL.md
API_SPEC.md
TECHNICAL_SPEC.md
TESTING_STRATEGY.md
```

where applicable.

---

# 16. API Contract First

When frontend and backend need to communicate, define the contract first.

Example:

```text
POST /api/v1/chat
```

Define:

- Request structure
- Response structure
- Errors
- Required fields
- Status codes

Then:

```text
Backend implements contract
        +
Frontend consumes contract
```

This allows frontend and backend development to proceed more independently.

---

# 17. API Contract Example

Request:

```json
{
  "conversation_id": "conv_123",
  "message": "I need a 3-bedroom apartment in Lekki."
}
```

Response:

```json
{
  "conversation_id": "conv_123",
  "message": "I'd be happy to help. What is your budget?"
}
```

Both sides should agree on this contract before integration.

---

# 18. Feature Branch Workflow

Use feature branches for meaningful changes.

Example:

```text
main
  │
  └── feature/lead-api
```

Other examples:

```text
feature/react-chat
feature/database-models
feature/n8n-lead-intake
feature/ai-extraction
feature/lead-qualification
feature/google-sheets-sync
```

---

# 19. Branch Naming

Use descriptive names.

Good:

```text
feature/lead-api
feature/chat-interface
feature/ai-extraction
feature/lead-scoring
fix/duplicate-webhook
fix/chat-error-state
test/ai-evaluation
```

Avoid:

```text
test
new
changes
stuff
my-code
```

---

# 20. Commit Strategy

Each commit should represent a logical change.

Examples:

```text
feat: add lead creation endpoint
```

```text
feat: add React chat interface
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

```text
docs: update API specification
```

---

# 21. Keep Commits Small

Prefer:

```text
Commit 1
Add Lead model

Commit 2
Add Lead schema

Commit 3
Add Lead endpoint

Commit 4
Add Lead tests
```

rather than:

```text
Commit
Build entire backend
```

Small commits are easier to:

- Review
- Debug
- Revert
- Understand
- Explain to an AI coding assistant

---

# 22. Pull Request / Review Workflow

Before merging a feature:

```text
Feature Complete
      ↓
Tests Pass
      ↓
Code Review
      ↓
Architecture Check
      ↓
Documentation Check
      ↓
Merge
```

Review should verify:

- Correct behavior
- Architecture alignment
- Error handling
- Tests
- Maintainability
- Security boundaries
- Documentation

---

# 23. Definition of Ready

A task is ready for implementation when:

- Requirement is clear
- Expected behavior is defined
- Dependencies are known
- Relevant documentation is identified
- API/data contracts are known
- Testing approach is understood

If important requirements are unknown, clarify them before large implementation work begins.

---

# 24. Definition of Done

A task is complete when:

- Code works
- Tests pass
- Error handling exists
- Relevant integration works
- Documentation is updated where necessary
- No known critical regression exists
- Code is understandable
- Changes are committed

---

# 25. Testing During Development

Testing should happen continuously.

Use:

```text
Small Change
   ↓
Run Relevant Tests
   ↓
Continue
```

Not:

```text
Build For Two Weeks
   ↓
Run All Tests
   ↓
Discover 50 Problems
```

---

# 26. Test Selection

Not every change requires the entire test suite.

For example:

### React button change

Run:

```text
Frontend unit tests
Component tests
Relevant E2E test
```

### Database change

Run:

```text
Database tests
Backend tests
API tests
Affected integration tests
```

### AI prompt change

Run:

```text
AI evaluation
Golden tests
Structured-output tests
Safety tests
Relevant E2E tests
```

### n8n workflow change

Run:

```text
Workflow tests
Integration tests
Relevant E2E test
```

---

# 27. Regression Testing

Before completing a feature, verify that existing behavior still works.

Example:

Adding:

```text
Rental support
```

must not break:

```text
Buying
Land
Selling
Property enquiry
```

A new feature should expand the system rather than accidentally break existing functionality.

---

# 28. Error-First Development

Developers should consider failure scenarios while implementing a feature.

For every external dependency ask:

```text
What happens if it fails?
```

Examples:

```text
AI unavailable
Database unavailable
n8n unavailable
Google Sheets unavailable
Network timeout
Invalid response
Duplicate webhook
```

The answer should be defined before production use.

---

# 29. Observability During Development

Important operations should be traceable.

Use identifiers such as:

```text
request_id
conversation_id
message_id
lead_id
workflow_execution_id
```

Example:

```text
request_id = req_123
conversation_id = conv_456
message_id = msg_789
lead_id = lead_999
```

This allows developers to follow one customer request through the entire system.

---

# 30. Local Development Workflow

A typical local development session may involve:

```text
Terminal 1
FastAPI

Terminal 2
React

Terminal 3
n8n / Docker

Terminal 4
Database tools / tests
```

The exact terminal arrangement is not important.

The important thing is that all required services are running and their boundaries are understood.

---

# 31. Environment Configuration

Development configuration should be stored through environment variables.

Example:

```text
DATABASE_URL
AI_API_KEY
N8N_WEBHOOK_URL
N8N_API_KEY
GOOGLE_SHEETS_ID
```

Frontend:

```text
VITE_API_BASE_URL
```

Do not hardcode secrets in source code.

---

# 32. Never Commit Secrets

Never commit:

```text
.env
API keys
database passwords
OAuth secrets
service credentials
private tokens
```

Use:

```text
.env.example
```

to document required configuration without exposing real values.

Example:

```text
DATABASE_URL=
AI_API_KEY=
N8N_WEBHOOK_URL=
```

---

# 33. AI Coding Assistant Workflow

The AI coding assistant should be treated as a development collaborator, not as an unrestricted autonomous programmer.

Recommended workflow:

```text
Human
  ↓
Defines Task
  ↓
AI Reads Relevant Docs
  ↓
AI Proposes Approach
  ↓
Human Reviews
  ↓
AI Implements
  ↓
AI Runs Tests
  ↓
Human Reviews Result
```

---

# 34. AI Coding Assistant Context

Before asking the assistant to modify code, provide or make available:

```text
Relevant documentation
Existing code
Expected behavior
Constraints
Tests
```

For example, for a lead API task, the assistant should understand:

```text
API_SPEC.md
DATA_MODEL.md
TECHNICAL_SPEC.md
TESTING_STRATEGY.md
```

It does not need to reread every project document for every tiny change.

---

# 35. AI Coding Assistant Task Prompt Pattern

A useful task format is:

```text
Task:
Implement [specific feature].

Context:
[Relevant project context.]

Read:
- API_SPEC.md
- DATA_MODEL.md

Requirements:
- Requirement 1
- Requirement 2
- Requirement 3

Constraints:
- Do not change architecture.
- Do not modify unrelated files.
- Follow existing patterns.

Tests:
- Add/update relevant tests.

Done when:
- Expected behavior works.
- Tests pass.
```

This reduces unnecessary AI-generated changes.

---

# 36. AI Coding Assistant Change Boundaries

The assistant should not modify unrelated areas.

Example:

If asked:

> "Add the lead creation endpoint."

It should not automatically:

- Redesign the frontend
- Rewrite the database
- Replace FastAPI
- Replace n8n
- Change AI provider
- Rewrite all documentation

unless the task explicitly requires those changes.

---

# 37. Architecture Change Rule

Major architecture changes require deliberate review.

Examples:

```text
FastAPI → another backend
PostgreSQL → another database
React → another frontend framework
n8n → another automation platform
Gemini → another AI provider
```

These are not ordinary code changes.

They affect multiple specifications.

Before making such a change:

```text
Identify impact
    ↓
Update architecture
    ↓
Update technical specifications
    ↓
Update affected contracts
    ↓
Update implementation
    ↓
Update tests
```

---

# 38. Avoid Premature Abstraction

Do not create complicated architecture before the problem requires it.

Start simple.

For example:

```text
chat_service.py
```

is preferable to creating:

```text
12 abstraction layers
```

without a real need.

Complexity should be earned by actual requirements.

---

# 39. Avoid Giant Files

Keep responsibilities separated.

Avoid:

```text
main.py
```

containing:

- All API routes
- Database logic
- AI logic
- Qualification logic
- n8n logic
- Notification logic

Prefer:

```text
routes/
services/
models/
schemas/
db/
core/
```

with clear responsibilities.

---

# 40. Avoid Giant n8n Workflows

Do not create:

```text
ONE HUGE WORKFLOW
```

containing:

```text
Lead intake
AI
Qualification
Notifications
Google Sheets
Follow-up
Error handling
```

Prefer modular workflows:

```text
Lead Intake
AI Processing
Qualification
Notification
Sheets Sync
Follow-up
Error Handling
```

This makes workflows easier to understand and debug.

---

# 41. Documentation Update Workflow

When implementation changes architecture or behavior:

```text
Code Change
   ↓
Identify Affected Docs
   ↓
Update Documentation
   ↓
Review Consistency
```

Examples:

Changing an API:

```text
API_SPEC.md
```

Changing a database field:

```text
DATA_MODEL.md
API_SPEC.md
```

Changing AI behavior:

```text
AI_AGENT_SPEC.md
TESTING_STRATEGY.md
```

Changing workflow behavior:

```text
N8N_WORKFLOW_SPEC.md
TESTING_STRATEGY.md
```

---

# 42. Documentation Consistency Check

At major milestones verify:

```text
PRD
   ↕
Architecture
   ↕
Technical Spec
   ↕
API
   ↕
Database
   ↕
AI
   ↕
n8n
   ↕
UI
   ↕
Tests
   ↕
Implementation
```

These should not contradict one another.

---

# 43. Feature Completion Checklist

Before marking a feature complete:

```text
[ ] Requirement understood
[ ] Relevant documentation reviewed
[ ] Implementation complete
[ ] Validation implemented
[ ] Error handling implemented
[ ] Unit tests added
[ ] Integration tests added where required
[ ] E2E test added where required
[ ] Existing tests pass
[ ] Documentation updated
[ ] No unrelated changes
[ ] Code reviewed
[ ] Commit created
```

---

# 44. Bug Fix Workflow

When a bug is discovered:

```text
Bug
 ↓
Reproduce
 ↓
Identify Root Cause
 ↓
Write Regression Test
 ↓
Fix
 ↓
Run Tests
 ↓
Review
 ↓
Document if necessary
```

Do not simply patch the visible symptom if the underlying problem remains.

---

# 45. Example Bug

Suppose duplicate customer messages create two leads.

Bad approach:

```text
Delete one duplicate after creation.
```

Better approach:

```text
Identify duplicate processing
       ↓
Use message_id / idempotency
       ↓
Prevent duplicate processing
       ↓
Add regression test
```

This protects the system against future occurrences.

---

# 46. AI-Specific Bug Workflow

AI bugs require additional analysis.

Example:

The AI interprets:

> "I want somewhere to rent."

as:

```text
BUY
```

Process:

```text
Identify incorrect classification
        ↓
Add example to evaluation dataset
        ↓
Review prompt/schema
        ↓
Improve AI handling
        ↓
Run golden tests
        ↓
Run regression tests
```

The new test becomes part of the permanent evaluation suite.

---

# 47. Integration Order

When integrating components, connect them gradually.

Preferred:

```text
React
 ↓
FastAPI
```

Then:

```text
FastAPI
 ↓
Database
```

Then:

```text
FastAPI
 ↓
n8n
```

Then:

```text
n8n
 ↓
AI
```

Then:

```text
Qualification
 ↓
Notifications
```

Then:

```text
Google Sheets
 ↓
Follow-ups
```

Finally:

```text
Complete E2E
```

---

# 48. Review Questions

Before accepting a change, ask:

### Product

- Does this solve the intended problem?

### Architecture

- Is the change in the correct component?

### API

- Does it follow the API contract?

### Database

- Does it follow the data model?

### AI

- Is AI output validated?

### n8n

- Is the workflow modular and recoverable?

### Frontend

- Are loading and error states handled?

### Testing

- Is there enough test coverage?

### Documentation

- Do the documents still describe reality?

---

# 49. Development Anti-Patterns

Avoid:

### Coding before understanding the requirement

```text
Guess
 ↓
Code
 ↓
Rewrite
```

### Giant AI prompts

```text
"Build the whole system."
```

### Untested AI output

```text
AI
 ↓
Database
```

### Hardcoded secrets

```text
API_KEY = "actual-secret"
```

### Direct frontend database access

```text
React
 ↓
SQL
```

### Giant n8n workflow

```text
Everything in one workflow
```

### Ignoring failing tests

```text
Test fails
 ↓
Delete test
```

### Documentation drift

```text
Code changes
 ↓
Docs remain outdated
```

---

# 50. Recommended Daily Development Loop

A productive development session should look like:

```text
1. Choose one task
        ↓
2. Read relevant documentation
        ↓
3. Inspect existing code
        ↓
4. Define expected behavior
        ↓
5. Implement smallest change
        ↓
6. Run tests
        ↓
7. Fix issues
        ↓
8. Review changes
        ↓
9. Update documentation if needed
        ↓
10. Commit
```

Then start the next task.

---

# 51. Milestone Review

At the end of each major milestone:

```text
Implementation
     ↓
Testing
     ↓
Documentation Review
     ↓
Architecture Review
     ↓
Demo
     ↓
Next Milestone
```

Example:

### Milestone

Customer chat working.

Verify:

```text
React
 ↓
FastAPI
 ↓
Database
```

before moving into advanced AI automation.

---

# 52. Production Readiness Workflow

Before production:

```text
Feature Complete
      ↓
Full Test Suite
      ↓
AI Evaluation
      ↓
E2E Testing
      ↓
Failure Testing
      ↓
Performance Testing
      ↓
Staging Validation
      ↓
Documentation Review
      ↓
Release
```

---

# 53. Change Impact Analysis

Before changing a component, identify what depends on it.

Example:

Changing the `Lead` model may affect:

```text
Database
 ↓
FastAPI
 ↓
n8n
 ↓
AI
 ↓
React
 ↓
Google Sheets
 ↓
Tests
```

Therefore, database changes should be treated carefully.

A small-looking change can have a large system impact.

---

# 54. Ownership Model

Each layer has a primary responsibility.

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

Google Sheets
→ Operational/reporting surface

Tests
→ Verification
```

A component should not silently take over another component's responsibility.

---

# 55. Final Development Workflow

The complete workflow is:

```text
                 REQUIREMENT
                      ↓
                   DESIGN
                      ↓
                SMALL TASK
                      ↓
              IMPLEMENTATION
                      ↓
                  TESTING
                      ↓
                  REVIEW
                      ↓
               INTEGRATION
                      ↓
              DOCUMENTATION
                      ↓
                   COMMIT
                      ↓
                NEXT TASK
```

For major features:

```text
Requirement
    ↓
Architecture
    ↓
API/Data Contract
    ↓
Implementation
    ↓
Unit Tests
    ↓
Integration
    ↓
AI Evaluation
    ↓
E2E
    ↓
UAT
    ↓
Release
```

---

# 56. Final Principle

The purpose of this workflow is not to make development slow or bureaucratic.

It is designed to make the project easier to build.

The most important principles are:

> **Build small.**

> **Test continuously.**

> **Respect system boundaries.**

> **Keep documentation and code synchronized.**

> **Treat AI as a powerful but fallible component.**

> **Use AI coding assistants with clear constraints and human review.**

> **Fix root causes instead of hiding failures.**

The goal is to build the PrimeHomes Realty Lead Bot as a professional, maintainable software system that can continue to evolve after the initial MVP.