# Directive 04: Export to Cloud Services

**Goal:** Provide the user and researchers with actionable deliverables. Specifically, export the unstructured `.tmp/analyzed_results.json` into a readable, beautifully formatted Google Sheet (or CSV for now) serving as the "Dashboard Backend."

## Input Context
- Read the enriched JSON data from `.tmp/analyzed_results.json`.

## Rules for Export Data Transformation

**1. Output Formatting (Deliverables vs Intermediates)**
- Local `.tmp/` files are only for intermediates. Deliverables must be cloud-based (e.g., Google Sheets, Google Drive CSV).
- Create a Pandas DataFrame (or similar) from the JSON.
- Filter invalid records (e.g., posts where LLM failed to parse).

**2. Columns for the final Deliverable Output:**
`[Date / Time] | [Game] | [Title] | [Feature/Category] | [Sentiment (-1 to 1)] | [Churn Risk] | [Loyalty Signal] | [Reasoning (Glass Box)] | [Link]`

**3. Execution & Authorization:**
- Use credentials stored via `.env` or `credentials.json` (handled in Python scripts `execution/export_google_sheets.py`).
- If Google credentials are not yet set up, save the final output as `.tmp/FINAL_DASHBOARD_DATA.csv` and report to the user (self-anneal: update directive if API scopes fail).

## Self-Recovery / Annealing
- If the Google API hits a quota or throws an Auth Error: Do NOT block the pipeline completely. 
- Fallback: Write the output locally to `.tmp/dashboard_fallback.csv`, then notify the user that auth needs fixing.
