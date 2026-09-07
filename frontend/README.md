# Frontend (React)

React application for the customer chat interface and sales dashboard.

## Structure (target)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow/
│   │   ├── MessageList/
│   │   ├── MessageBubble/
│   │   ├── ChatInput/
│   │   ├── TypingIndicator/
│   │   ├── ContactForm/
│   │   ├── LeadSummary/
│   │   └── ErrorMessage/
│   ├── pages/
│   │   ├── Home/
│   │   ├── Chat/
│   │   └── Confirmation/
│   ├── services/
│   │   └── api.js
│   ├── hooks/
│   │   └── useChat.js
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── vite.config.js
└── README.md
```

## Local Development

```bash
cd frontend
npm install
npm run dev
```

## Principles

- Frontend is presentation and interaction only.
- All backend communication goes through the API service layer.
- No direct database, n8n, or AI provider access from the browser.
- See `docs/UI_UX_SPEC.md`.
