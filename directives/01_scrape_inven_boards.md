# Directive 01: Scrape Inven Boards

**Goal:** Collect "Hot/Recommended" posts from 3 major MMORPG boards on Inven to benchmark player sentiment against Aion 2.

**Target URLs (my=chu for Hot Posts):**
1. Lost Ark (`game_id`: lostark): `https://lostark.inven.co.kr/board/lostark/4811?my=chu`
2. Throne and Liberty (`game_id`: tl): `https://tl.inven.co.kr/board/tl/6086?my=chu`
3. Black Desert (`game_id`: black): `https://black.inven.co.kr/board/black/3584?my=chu`

## Rules and Edge Handling

**1. Data Schema (Output: `BoardItem`)**
For each post, extract:
- `post_id` (String)
- `game_name` (String, e.g., 'Lost Ark')
- `title` (String)
- `url` (String)
- `author` (String)
- `view_count` (Integer)
- `upvotes` (Integer)
- `content_snippet` (String, requires detailed scrape)

**2. Anti-Bot / Throttling (Crucial)**
- Inven uses strict IP blocks for frequent scraping.
- Execution scripts must use standard `requests` + `BeautifulSoup4`.
- A dynamic `User-Agent` (from `.env` or `fake_useragent`) is required.
- Maintain a `Session()` scope for the duration of the script.
- Insert a randomized `time.sleep(1.0, 3.0)` between any HTTP requests.

**3. Hybrid Cost Optimization (The "Top 3" Rule)**
- First pass: Scrape the list page to get `title`, `author`, `view_count`, `upvotes`, and `url`.
- Sort the gathered list by `upvotes` in descending order.
- Second pass: ONLY visit the `url` for the Top 3 highly-upvoted posts to extract the actual body text into `content_snippet`. All other items in the batch stay with an empty snippet or are discarded.

## Execution Requirements
**Script to execute:** `execution/scrape_inven.py`
**Input variables:** Run periodically (e.g., daily).
**Outputs:** Save raw JSON output into `.tmp/raw_scraped_data.json` so the next pipeline (Classification) can pick it up. Do NOT commit the output.
