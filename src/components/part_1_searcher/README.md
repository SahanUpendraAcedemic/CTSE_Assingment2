# Part 1 Searcher Agent

Agent responsibility:
- Produce raw findings for a given research topic into shared state.

Tool implemented:
- `search_tool(query)` placeholder for local search operations.

Input state fields:
- `topic`
- `raw_findings` (optional)
- `logs`

Output state fields:
- `searcher_agent_run`
- `logs`

Tests:
- `src/components/part_1_searcher/tests/test_searcher_agent.py`
- `src/components/part_1_searcher/tests/test_searcher_tools.py`

Student contribution proof:
- Agent node is implemented in `src/components/part_1_searcher/agent.py`
- Tool implementation and tests are isolated inside this folder.
