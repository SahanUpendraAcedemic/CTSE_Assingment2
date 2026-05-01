# Part 2 Fact Checker Agent

Agent responsibility:
- Verify candidate claims in shared state and mark which claims are trusted.

Tool implemented:
- `validate_claims(claims)` placeholder for claim verification.

Input state fields:
- `raw_findings`
- `verified_claims`
- `rejected_claims`
- `logs`

Output state fields:
- `fact_checker_agent_run`
- `verified_claims`
- `rejected_claims`
- `logs`

Tests:
- `src/components/part_2_fact_checker/tests/test_fact_checker_agent.py`
- `src/components/part_2_fact_checker/tests/test_fact_checker_tools.py`

Student contribution proof:
- Agent node is implemented in `src/components/part_2_fact_checker/agent.py`
- Tool implementation and tests are isolated inside this folder.
