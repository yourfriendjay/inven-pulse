# Directive 02: Classify Verbatims

**Goal:** Transform unstructured gaming verbatims (the `.tmp/raw_scraped_data.json`) into structured, multi-dimensional feature data using LLM logic.

## Input Context
- Retrieve data from `.tmp/raw_scraped_data.json` produced by `01_scrape_inven_boards.md`.
- Read only the posts that have a `content_snippet` (i.e., the Top 3 posts) or meaningful long titles. 

## Classification Rules (The "Inven-Pulse" Framework)
An LLM (e.g., using `OPENAI_API_KEY` from `.env`) will evaluate each post's content and assign:
1. **Primary Feature Category**
   - `Combat_Mechanics`: Mentions of class balance, skill animations, raid difficulty, TTK (Time to Kill).
   - `Monetization`: Mentions of cash shop, gacha probability, P2W (Pay to Win), battle pass efficiency.
   - `Graphics_Optimization`: Mentions of UE5, frame drops, stuttering, art style, UI/UX.
   - `Server_Stability`: Mentions of lag, disconnects, queues, maintenance.
   - `Other`: General discussion, off-topic, or unrecognizable.

2. **Sentiment Score**
   - Assign a score from `-1.0` (Highly Negative) to `+1.0` (Highly Positive).
   - `0.0` represents Neutral or purely informational posts.

3. **Reasoning Audit Log (Glass Box)**
   - The LLM must provide a 1-sentence explanation of *why* it assigned the feature and sentiment (e.g., "The user complained about the low probability of weapon enhancement, thus Monetization/Negative").

## Output Requirements
- Maintain all original metadata (`post_id`, `game_name`, `title`, `url`, `upvotes`).
- Append the new fields: `category`, `sentiment_score`, `reasoning`.
- Save the results as `.tmp/classified_data.json`.
- Do NOT commit this file.
