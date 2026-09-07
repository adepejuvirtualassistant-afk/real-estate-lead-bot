# Database

PostgreSQL is the **system of record**.

## Structure (target)

```text
database/
├── migrations/          # Alembic or equivalent migration files
├── seeds/               # Optional seed data for development
├── schema/              # Reference SQL or ER diagrams if needed
└── README.md
```

## Core Tables (from DATA_MODEL.md)

- customers
- sales_agents
- leads
- conversations
- messages
- lead_qualifications
- follow_ups
- lead_events

## Principles

- All schema changes go through migrations.
- Google Sheets is **not** the primary database.
- See `docs/DATA_MODEL.md`.
