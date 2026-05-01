# Local Smart Research Hub

A local, LangGraph-orchestrated multi-agent research system using Ollama-compatible local SLMs. This repository separates four student-owned components and shared orchestration code so each part is easy to identify, grade, and maintain.

## Student contribution

- `src/components/part_1_searcher/` — Searcher Agent
- `src/components/part_2_fact_checker/` — Fact Checker Agent
- `src/components/part_3_summarizer/` — Summarizer Agent
- `src/components/part_4_formatter/` — Formatter Agent (this component)

## Running locally

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   python -m pytest -q
   ```
4. Run the local demonstration entrypoint:
   ```bash
   python -m src.main
   ```

## Structure

- `src/shared/` — shared schemas, settings, and utility helpers
- `src/orchestration/` — LangGraph-style orchestration and state routing
- `src/components/` — four student components with isolated agent logic and tests
- `outputs/` — saved reports and intermediate local artifacts
- `logs/` — runtime observability logs
- `docs/` — architecture and contribution documentation
