# Inven-Pulse

Inven-Pulse is an autonomous market research tool designed to scrape, classify, and analyze gaming community sentiment from Inven (Korea's largest gaming forum). It acts as a bespoke analytical instrument ("Researcher-as-Maker"), specifically providing comparative intelligence against upcoming major titles like NCSoft's Aion 2.

## 3-Layer Architecture
This repository follows a strict 3-Layer Architecture separation of concerns:
1. **Directives (`directives/`)**: SOPs in Markdown defining goals, expected inputs, and outputs.
2. **Orchestration**: Managed dynamically by the AI agent context.
3. **Execution (`execution/`)**: Deterministic, reliable Python scripts (e.g. Scraper, Classifier, Exporter).

## Setup
1. Copy `.env.example` to `.env` and fill in your keys.
2. Install dependencies (e.g. `pip install -r requirements.txt`).
3. Run the orchestrator or individual scripts within `execution/`.

> **Note:** Do NOT commit your `.env`, `credentials.json`, or anything in `.tmp/`.
