import os
import sys
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from server.db import get_db_connection

app = FastAPI(title="Inven-Pulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/api/dashboard/stats")
async def get_stats(game: str = None, days: int = 7):
    """KPI card data: total posts, avg sentiment, churn count, loyalty count."""
    conn = get_db_connection()
    c = conn.cursor()

    where = " WHERE scraped_at >= datetime('now', 'localtime', ?)"
    params = [f'-{days} days']
    if game:
        where += " AND game_name = ?"
        params.append(game)

    c.execute(f"SELECT COUNT(*) as total FROM posts{where}", params)
    total = c.fetchone()["total"]

    c.execute(f"SELECT AVG(sentiment_score) as avg_s FROM posts{where}", params)
    avg_s = c.fetchone()["avg_s"] or 0.0

    c.execute(f"SELECT COUNT(*) as cnt FROM posts{where} {'AND' if where else 'WHERE'} churn_risk = 1", params)
    churn = c.fetchone()["cnt"]

    c.execute(f"SELECT COUNT(*) as cnt FROM posts{where} {'AND' if where else 'WHERE'} loyalty_signal = 1", params)
    loyalty = c.fetchone()["cnt"]

    conn.close()
    return {
        "total_posts": total,
        "avg_sentiment": round(avg_s, 2),
        "churn_count": churn,
        "loyalty_count": loyalty,
    }


@app.get("/api/dashboard/logs")
async def get_logs(game: str = None, limit: int = 20, days: int = 7):
    """Audit trail rows for the table."""
    conn = get_db_connection()
    c = conn.cursor()

    where = " WHERE scraped_at >= datetime('now', 'localtime', ?)"
    params = [f'-{days} days']
    if game:
        where += " AND game_name = ?"
        params.append(game)

    params.append(limit)
    c.execute(f"SELECT * FROM posts{where} ORDER BY upvotes DESC LIMIT ?", params)
    rows = c.fetchall()
    conn.close()

    logs = []
    for r in rows:
        signal = "Neutral ⚪"
        if r["churn_risk"]:
            signal = "Churn 🔴"
        elif r["loyalty_signal"]:
            signal = "Loyalty 🟢"
        elif r["sentiment_score"] and r["sentiment_score"] > 0.3:
            signal = "Positive 🟢"
        elif r["sentiment_score"] and r["sentiment_score"] < -0.3:
            signal = "Risk 🟡"

        logs.append({
            "post_id": r["post_id"],
            "game_name": r["game_name"],
            "title": r["title"],
            "category": r["category"] or "Other",
            "score": round(r["sentiment_score"] or 0, 2),
            "upvotes": r["upvotes"],
            "text": (r["content_snippet"] or "")[:120],
            "reasoning": r["reasoning"] or "",
            "signal": signal,
            "url": r["url"],
        })

    return logs


@app.get("/api/dashboard/sentiment-trend")
async def get_sentiment_trend(game: str = None, days: int = 7):
    """Category-level average sentiment for the chart."""
    conn = get_db_connection()
    c = conn.cursor()

    where = " WHERE scraped_at >= datetime('now', 'localtime', ?)"
    params = [f'-{days} days']
    if game:
        where += " AND game_name = ?"
        params.append(game)

    c.execute(f"""
        SELECT category, AVG(sentiment_score) as avg_score, COUNT(*) as cnt
        FROM posts{where}
        GROUP BY category
    """, params)
    rows = c.fetchall()
    conn.close()

    return [{"category": r["category"], "avg_score": round(r["avg_score"], 2), "count": r["cnt"]} for r in rows]


# --- Serve the Frontend ---

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Mount static assets (CSS, JS) under /css and /js
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")


@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
