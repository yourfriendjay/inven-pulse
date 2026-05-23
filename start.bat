@echo off
echo ==============================================
echo Inven-Pulse Auto Start Script
echo ==============================================

echo [1/3] Installing Dependencies...
python -m pip install -r requirements.txt

echo [2/3] Running Data Pipeline...
python execution/scrape_inven.py
python execution/classify_verbatims.py
python execution/analyze_churn_return.py
python execution/save_to_db.py

echo [3/3] Starting FastAPI Backend Database Server...
start "" http://127.0.0.1:8000/docs
python -m uvicorn server.api:app --host 127.0.0.1 --port 8000 --reload
pause
