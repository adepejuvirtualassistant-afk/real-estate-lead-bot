# n8n Workflows

n8n is the workflow orchestration layer.

## Structure (target)

```text
n8n/
├── workflows/
│   ├── RE-LEAD-01-lead-intake.json
│   ├── RE-LEAD-02-ai-processing.json
│   ├── RE-LEAD-03-sales-notification.json
│   ├── RE-LEAD-04-follow-up.json
│   ├── RE-LEAD-05-google-sheets-sync.json
│   └── RE-LEAD-99-error-handler.json
└── README.md
```

## Principles

- n8n orchestrates; it is not the sole source of truth for core application state.
- Prefer modular workflows over one giant workflow.
- Credentials are managed inside n8n (never committed).
- See `docs/N8N_WORKFLOW_SPEC.md`.
