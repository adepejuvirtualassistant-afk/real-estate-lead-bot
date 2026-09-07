# Documentation

This folder contains the approved foundational documents for the **Real Estate Lead Bot** (PrimeHomes Realty Lead Management System).

These documents are the **source of truth** for implementation. Code must follow them.

## Core Documents

| File | Description |
|------|-------------|
| [PRD.md](PRD.md) | Product Requirements Document – what the product must do |
| [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) | High-level system components and boundaries |
| [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) | Detailed technical implementation rules |
| [API_SPEC.md](API_SPEC.md) | API contracts and endpoints |
| [DATA_MODEL.md](DATA_MODEL.md) | Database schema, entities, and relationships |
| [AI_AGENT_SPEC.md](AI_AGENT_SPEC.md) | AI responsibilities, prompts, safety rules |
| [N8N_WORKFLOW_SPEC.md](N8N_WORKFLOW_SPEC.md) | n8n workflow design and responsibilities |
| [UI_UX_SPEC.md](UI_UX_SPEC.md) | Frontend and user experience requirements |
| [TESTING_STRATEGY.md](TESTING_STRATEGY.md) | Testing approach and quality gates |
| [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | Phased build order |
| [BUILD_TASKS.md](BUILD_TASKS.md) | Small executable development tasks |
| [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) | How developers and AI assistants should work |
| [TASK.md](TASK.md) | Live task tracker (current status) |

## Rules

- Do not change architecture or major contracts without updating the relevant documents.
- When code and documentation disagree, investigate rather than silently choosing one.
- Prefer updating documentation in the same PR as the code change when behavior changes.
