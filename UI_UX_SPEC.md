# UI/UX Specification

## 1. Purpose

This document defines the user interface (UI), user experience (UX), frontend behavior, components, screens, states, and interaction patterns for the **Real Estate Lead Bot**.

The frontend will be built using:

```text
React
```

The frontend communicates with the backend through:

```text
React
   ↓
FastAPI
   ↓
n8n / AI / Database
```

The frontend must **not communicate directly with the SQL database**.

---

# 2. Product Experience

The customer should experience the system as a simple conversational real-estate assistant.

The customer should not need to understand:

- FastAPI
- n8n
- AI models
- SQL
- APIs
- Workflows
- Lead scoring

They should simply be able to:

```text
Open chatbot
    ↓
Send message
    ↓
Receive response
    ↓
Answer questions
    ↓
Provide property requirements
    ↓
Submit contact information
    ↓
Receive confirmation
```

---

# 3. Primary User

The primary frontend user is a potential real-estate customer.

Example:

> "Hi, I'm looking for a 3-bedroom apartment in Lekki with a budget of ₦80 million."

The interface should make it easy for the customer to continue the conversation.

---

# 4. Secondary Users

Future versions may include internal users:

### Sales Agent

Can:

- View assigned leads
- View customer information
- View lead requirements
- View conversations
- Manage follow-ups
- Update lead status

### Sales Manager

Can:

- View team leads
- Monitor lead pipeline
- Assign leads
- Monitor sales activity

### Admin

Can:

- Manage users
- Configure system settings
- Manage integrations
- View system activity

These internal interfaces are outside the initial customer-facing MVP unless explicitly added.

---

# 5. MVP Frontend

The MVP should focus on one primary experience:

```text
Customer Chat Interface
```

Optional supporting interface:

```text
Lead Information Form
```

The MVP does not need a complex dashboard.

Avoid building unnecessary screens before the core customer journey works.

---

# 6. Customer Journey

The primary customer journey is:

```text
Landing Page
      ↓
Start Conversation
      ↓
Chat Interface
      ↓
AI Understands Requirement
      ↓
AI Asks Missing Questions
      ↓
Customer Provides Information
      ↓
Lead Becomes Qualified
      ↓
Customer Provides Contact Information
      ↓
Confirmation
```

---

# 7. Main Screens

The initial frontend should contain:

```text
1. Landing / Welcome Screen
2. Chat Screen
3. Contact Information Form
4. Confirmation State
5. Error State
```

---

# 8. Landing / Welcome Screen

## Purpose

Introduce the assistant and encourage the customer to begin.

Example:

```text
PrimeHomes Realty

Find the right property for your needs.

Tell us what you're looking for and
our property assistant will help you get started.

[ Start Chat ]
```

Optional quick-start examples:

```text
Looking for a 3-bedroom apartment in Lekki
Find land in Ibadan
I want to rent a house in Ikeja
```

---

# 9. Chat Screen

The chat screen is the primary interface.

Basic structure:

```text
┌─────────────────────────────────────┐
│ PrimeHomes Realty        ● Online   │
├─────────────────────────────────────┤
│                                     │
│  Assistant:                         │
│  Hello! How can I help you today?  │
│                                     │
│                 Customer:           │
│      I need a 3-bedroom apartment   │
│      in Lekki.                      │
│                                     │
│  Assistant:                         │
│  Great! What's your approximate     │
│  budget?                            │
│                                     │
├─────────────────────────────────────┤
│ Type your message...          [➤]   │
└─────────────────────────────────────┘
```

---

# 10. Chat Components

The React application should use reusable components.

Recommended structure:

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

The exact folder structure may evolve during implementation.

---

# 11. Message Bubble

Each message should clearly indicate who sent it.

### Customer

```text
                 ┌─────────────────────┐
                 │ I need a house in    │
                 │ Lekki.               │
                 └─────────────────────┘
```

### Assistant

```text
┌─────────────────────────────────┐
│ Great! What's your approximate  │
│ budget?                         │
└─────────────────────────────────┘
```

The interface should visually distinguish the two.

---

# 12. Message Types

The frontend should support:

```text
TEXT
SYSTEM
ERROR
```

Future message types:

```text
PROPERTY_CARD
IMAGE
LINK
QUICK_REPLY
FORM
```

For example, a future property result could be displayed as:

```text
┌──────────────────────────┐
│ 3 Bedroom Apartment      │
│ Lekki                    │
│ ₦75,000,000              │
│                          │
│ [View Property]          │
└──────────────────────────┘
```

Only verified property information should be displayed.

---

# 13. Chat Input

The input should:

- Allow text entry
- Support Enter to send
- Support a Send button
- Prevent empty messages
- Disable sending while appropriate
- Show loading state when processing

Example:

```text
┌──────────────────────────────────┐
│ Type your message...       Send  │
└──────────────────────────────────┘
```

---

# 14. Empty Message Validation

If the user attempts to send:

```text
""
```

the frontend should not send the request.

Instead, it should prevent submission.

The backend must also validate the message.

Frontend validation is for user experience.

Backend validation is for system correctness.

---

# 15. Typing Indicator

While waiting for the AI response:

```text
Assistant is typing...
```

or:

```text
● ● ●
```

The user should understand that the system is processing their message.

---

# 16. Loading State

When a message is being processed:

```text
Customer message
      ↓
Loading
      ↓
Assistant response
```

The UI should:

- Show a loading indicator
- Prevent accidental duplicate submission
- Keep existing messages visible

---

# 17. Error State

If the API fails:

```text
Something went wrong.

We couldn't process your message right now.
Please try again.

[ Try Again ]
```

Do not expose:

```text
API error stack traces
Database errors
n8n execution errors
AI provider errors
Internal server details
```

to customers.

---

# 18. Network Failure

If the user's internet connection fails:

```text
Unable to connect.

Please check your internet connection
and try again.
```

The user should not lose the conversation unnecessarily.

---

# 19. Backend API Integration

The frontend communicates with FastAPI.

Example:

```text
POST /api/v1/chat
```

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
  "message_id": "msg_456",
  "response": "Great! What's your approximate budget?"
}
```

The exact API contract must remain aligned with:

```text
API_SPEC.md
```

---

# 20. API Service Layer

React should not scatter API calls throughout components.

Prefer:

```text
React Component
      ↓
API Service
      ↓
FastAPI
```

Example conceptual service:

```text
services/
└── api.js
```

Responsibilities:

- Send requests
- Handle responses
- Handle errors
- Add authentication when required
- Manage API base URL

---

# 21. Environment Configuration

The API URL should not be hard-coded throughout the application.

Example:

```text
VITE_API_BASE_URL=http://localhost:8000
```

Production will use a configured production URL.

The frontend should access configuration through environment variables.

---

# 22. Conversation State

The frontend should maintain:

```text
conversation_id
messages
loading
error
connection status
```

Example:

```javascript
{
  conversationId: "conv_123",
  messages: [],
  isLoading: false,
  error: null
}
```

The backend remains the authoritative source for persisted conversation data.

---

# 23. Message State

Each message may contain:

```text
id
sender
content
timestamp
status
```

Possible status values:

```text
SENDING
SENT
FAILED
```

Example:

```json
{
  "id": "msg_123",
  "sender": "customer",
  "content": "I need a house in Lekki.",
  "status": "SENT"
}
```

---

# 24. Failed Message

If a message fails:

```text
I need a house in Lekki.

        Failed to send

             [Retry]
```

The user should be able to retry.

---

# 25. Lead Information Form

When enough information has been collected, the system may request contact information.

Example:

```text
Almost done!

Where can our property team reach you?

Name
[________________]

Email
[________________]

Phone
[________________]

[ Submit ]
```

---

# 26. Contact Form Validation

### Name

Required when the form is presented.

### Email

Validate basic email format.

### Phone

Validate acceptable phone format.

The backend must independently validate all submitted values.

---

# 27. Lead Summary

Before final submission, the user may see a summary:

```text
Your Property Search

Property: Apartment
Bedrooms: 3
Location: Lekki
Budget: ₦80M
Intent: Buy

Contact:
John Doe
john@example.com
+2348012345678

[Submit Request]
```

This gives the customer an opportunity to verify the information.

---

# 28. Editable Information

If the user sees an incorrect requirement, they should be able to correct it.

Example:

```text
Bedrooms: 3
[Edit]
```

This can return them to the conversation rather than requiring a completely new lead.

---

# 29. Confirmation Screen

After successful lead submission:

```text
Thank you!

Your property request has been received.

A member of the PrimeHomes Realty team
will follow up with you shortly.

[Start New Search]
```

The system should not promise a specific response time unless the business has defined one.

---

# 30. Customer-Facing Information

The customer may see:

```text
Their own requirements
Their conversation
Verified property information
Confirmation messages
Next steps
```

The customer should not see:

```text
Lead score
Internal qualification reasons
Sales notes
Internal agent comments
System IDs
Workflow execution information
```

---

# 31. Responsive Design

The frontend must work on:

```text
Desktop
Tablet
Mobile
```

The chat interface should be designed mobile-first.

Example:

```text
Mobile
┌──────────────────────┐
│ PrimeHomes           │
├──────────────────────┤
│                      │
│ Chat messages        │
│                      │
│                      │
├──────────────────────┤
│ Type message...  ➤   │
└──────────────────────┘
```

---

# 32. Accessibility

The interface should follow basic accessibility principles.

Requirements:

- Keyboard navigation
- Visible focus states
- Accessible buttons
- Proper form labels
- Readable text
- Sufficient contrast
- Screen-reader-friendly structure
- Meaningful error messages

Do not rely only on color to communicate status.

---

# 33. UX Writing

Customer-facing language should be:

- Clear
- Friendly
- Professional
- Short
- Helpful
- Human

Avoid technical language.

Bad:

> "Your POST request returned HTTP 422."

Better:

> "Please check the information you entered and try again."

---

# 34. Quick Reply Options

Where useful, the AI may provide selectable options.

Example:

```text
When are you looking to buy?

[Immediately]

[Within 1 month]

[Within 3 months]

[Just researching]
```

Quick replies should be optional enhancements.

The system must still support normal text input.

---

# 35. Conversation Restart

The user should have an option to start a new conversation.

Example:

```text
[Start New Search]
```

Starting a new conversation should not automatically delete historical records.

The backend should create a new conversation ID.

---

# 36. Session Persistence

If appropriate, the frontend may persist the active conversation identifier locally.

Example:

```text
localStorage
```

However, persistent customer information should be handled carefully.

The backend/database remains the authoritative source.

---

# 37. Security Boundary

The React application should never contain:

```text
Database credentials
AI API keys
n8n credentials
Google credentials
Private service tokens
```

The frontend communicates with the backend.

```text
React
 ↓
FastAPI
 ↓
Services
```

Secrets remain server-side.

---

# 38. Frontend State Management

The MVP should avoid unnecessary complexity.

Simple React state may be sufficient for:

```text
messages
loading
error
conversation ID
form state
```

A dedicated state-management library should only be introduced if application complexity requires it.

---

# 39. Component Principles

React components should be:

- Small
- Reusable
- Focused
- Predictable
- Easy to test

Avoid creating one giant component such as:

```text
App.jsx
```

containing the entire application.

---

# 40. Suggested Component Tree

```text
App
 │
 ├── Header
 │
 └── ChatPage
      │
      ├── ChatWindow
      │    ├── MessageList
      │    │    └── MessageBubble
      │    │
      │    └── TypingIndicator
      │
      └── ChatInput
```

When a contact form is required:

```text
ChatPage
   │
   ├── ChatWindow
   │
   └── ContactForm
```

---

# 41. Frontend Error Handling

The frontend should handle:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
429 Rate Limited
500 Server Error
502 Service Error
503 Service Unavailable
```

The UI should convert technical errors into user-friendly messages.

---

# 42. API Request Lifecycle

Example:

```text
User clicks Send
       ↓
Validate input
       ↓
Set loading = true
       ↓
POST /api/v1/chat
       ↓
FastAPI
       ↓
n8n / AI
       ↓
FastAPI response
       ↓
Add assistant message
       ↓
Set loading = false
```

If failure:

```text
API Error
   ↓
Set error
   ↓
Show friendly message
   ↓
Allow Retry
```

---

# 43. Performance

The frontend should:

- Avoid unnecessary re-renders
- Keep components focused
- Avoid loading large libraries unnecessarily
- Lazy-load future complex pages where appropriate
- Optimize assets
- Keep the initial chat experience fast

Do not optimize prematurely.

Measure first when performance becomes a concern.

---

# 44. Design System

The application should eventually define reusable:

```text
Typography
Spacing
Buttons
Inputs
Cards
Messages
Alerts
Forms
Icons
```

A simple consistent design is better than adding many visual effects.

---

# 45. Visual Design Principle

The interface should communicate:

```text
Trust
Clarity
Professionalism
Simplicity
```

The objective is not to create a visually complicated application.

A beautiful UI does not automatically mean the underlying system is good.

The frontend must make the reliable backend system easy for customers to use.

---

# 46. Frontend Testing

The React application should test:

### Components

```text
MessageBubble renders correctly
ChatInput accepts text
ChatInput prevents empty messages
TypingIndicator appears during loading
ErrorMessage displays correctly
ContactForm validates fields
```

### User flows

```text
Start conversation
Send message
Receive response
Handle loading
Handle API failure
Retry failed message
Submit contact information
View confirmation
Start new conversation
```

---

# 47. API Integration Testing

Test:

```text
React
 ↓
FastAPI
```

with:

- Valid request
- Invalid request
- Slow response
- API timeout
- Server error
- Empty response
- Malformed response

---

# 48. Browser Testing

The MVP should be tested on common browsers.

At minimum:

```text
Chrome
Edge
Firefox
Safari where available
```

And on:

```text
Mobile
Tablet
Desktop
```

---

# 49. UI States Checklist

Every major component should consider:

```text
DEFAULT
LOADING
SUCCESS
EMPTY
ERROR
DISABLED
```

For example, Send button:

```text
Default → Send
Loading → Sending...
Disabled → Cannot send
```

---

# 50. Frontend Environment

Recommended initial structure:

```text
frontend/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── utils/
│   ├── App.jsx
│   └── main.jsx
│
├── .env
├── package.json
└── README.md
```

Never commit secrets in `.env`.

Use:

```text
.env.example
```

for safe configuration documentation.

---

# 51. Agentic AI Coding Rules

Any AI coding assistant working on the React frontend must follow these rules.

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
UI_UX_SPEC.md
```

before making major architectural changes.

### Rule 2

Do not create frontend functionality that contradicts the API contract.

### Rule 3

Do not connect React directly to SQL.

### Rule 4

Do not put API secrets in frontend code.

### Rule 5

Reuse existing components before creating duplicates.

### Rule 6

Do not introduce a large state-management library without a clear requirement.

### Rule 7

Do not invent backend endpoints.

If an endpoint is needed:

```text
Document requirement
        ↓
Update API_SPEC.md
        ↓
Implement FastAPI endpoint
        ↓
Implement frontend integration
```

### Rule 8

Customer-facing messages must not expose internal system information.

### Rule 9

Update this document when major UX behavior changes.

---

# 52. Definition of Done

The frontend MVP is ready when:

- [ ] React application starts successfully
- [ ] Landing page works
- [ ] Chat interface works
- [ ] Customer can send messages
- [ ] Messages display correctly
- [ ] Loading state works
- [ ] Error state works
- [ ] Retry works
- [ ] Conversation ID is handled correctly
- [ ] FastAPI integration works
- [ ] Contact form works
- [ ] Form validation works
- [ ] Confirmation screen works
- [ ] Mobile layout works
- [ ] Basic accessibility is implemented
- [ ] No secrets are exposed
- [ ] API contract matches `API_SPEC.md`
- [ ] Frontend tests cover critical flows

---

# 53. Future UI Features

The following can be added later:

```text
Property search results
Property cards
Property images
Map integration
Viewing booking
Customer dashboard
Saved properties
Sales agent chat
Document upload
Authentication
Notifications
Lead status tracking
```

These should not delay the core MVP.

---

# 54. Complete Frontend Architecture

```text
                    CUSTOMER
                       │
                       ▼
                 ┌───────────┐
                 │  React UI │
                 └─────┬─────┘
                       │
                       │ HTTP / JSON
                       ▼
                 ┌───────────┐
                 │  FastAPI  │
                 └─────┬─────┘
                       │
                       ▼
                     n8n
                       │
              ┌────────┼─────────┐
              ▼        ▼         ▼
             AI       SQL    Integrations
```

The frontend is responsible for the **experience**.

FastAPI is responsible for the **application/API layer**.

n8n is responsible for **orchestration**.

AI is responsible for **natural-language intelligence**.

SQL is responsible for **persistent application data**.

---

# 55. Final UX Principle

The customer should experience the product as simple:

```text
"Tell us what you need."
          ↓
"We understand your requirements."
          ↓
"Let's collect what is missing."
          ↓
"We'll connect you with the right team."
```

Behind this simple experience is the complete system:

```text
React
+
FastAPI
+
n8n
+
AI
+
SQL
+
Sales Workflow
```

The complexity belongs inside the system.

The customer experience should remain simple.