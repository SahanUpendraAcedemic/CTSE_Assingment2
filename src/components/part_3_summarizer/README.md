# Part 3 Summarizer Agent

Agent responsibility:
- Generate exactly 3 executive-summary bullets from `verified_claims` in shared state.
- Preserve LangGraph-style state compatibility by accepting and returning `ResearchState`.
- Avoid research, web APIs, paid APIs, cloud APIs, and unsupported fact invention.
- Exclude `rejected_claims`, duplicated rejected text, and explicitly unverified claims.

Tool implemented:
- `validate_summary_quality(summary, *, verified_claims=None, rejected_claims=None)` validates:
  - exactly 3 bullets
  - `- ` bullet formatting
  - grounding in verified claims when provided
  - absence of rejected claim text
  - safe False return for invalid input

Input state fields:
- `topic`
- `verified_claims`
- `rejected_claims`
- `logs`

Output state fields:
- `summary`
- `logs`

Local-only behavior:
- The agent is deterministic Python and does not import or call web clients, OpenAI, Anthropic, or other cloud APIs.
- The prompt in `prompts.py` documents constraints for a future Ollama/local SLM adapter, but the current agent does not call a model.
- If fewer than 3 verified claims are available, safe state-only bullets are used instead of invented facts.

Tests:
- `src/components/part_3_summarizer/tests/test_summarizer_agent.py`
- `src/components/part_3_summarizer/tests/test_summarizer_tools.py`

Student contribution proof:
- Summarizer agent, prompt contract, custom validation tool, tests, and this README are implemented inside `src/components/part_3_summarizer/`.
- This folder is isolated from other student components except for shared imports from `src.shared.schemas.research_state`.

Run Part 3 tests:
```bash
python -m pytest src/components/part_3_summarizer/tests -q
```
