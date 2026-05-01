# Demo Script

1. Activate the local Python environment.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run the sample entrypoint:
   ```bash
   python src/main.py
   ```
4. Observe the saved report path in the console.
5. Run the test suite:
   ```bash
   python -m pytest -q
   ```

This demo shows the Formatter Agent processing shared research state and saving a local Markdown report. It does not perform external search or network calls.
