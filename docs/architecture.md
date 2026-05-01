# Architecture

This local research hub separates four agent components and shared orchestration logic into distinct packages.

- `src/shared/` contains reusable schemas, configuration, and utility helpers.
- `src/orchestration/` contains simple graph and state routing modules for LangGraph-style flow.
- `src/components/part_*` contains student-owned agents, tools, prompts, and tests.

The Formatter Agent is implemented in `src/components/part_4_formatter/` and only formats existing verified state into Markdown or HTML without inventing facts.
