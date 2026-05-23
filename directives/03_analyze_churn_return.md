# Directive 03: Churn & Loyalty Driver Detection

**Goal:** Identify if a classified verbatim strongly signals that a user is about to quit (Churn) or is highly engaged/returning (Loyalty), primarily benchmarking against NCSoft's Aion 2 positioning.

## Input Context
- Read the structured data from `.tmp/classified_data.json` produced by `02_classify_verbatims.md`.
- Focus on posts with explicit opinions or complaints (usually high `upvotes`).

## Detection Rules (Korean Context)

**1. Linguistic Markers for Churn (이탈 징후):**
- Account liquidation: `"계정 팔고 뜹니다"`, `"템 처분"`, `"회수"` (Selling accounts/items).
- Uninstalling: `"삭제 완료"`, `"접음"`, `"환불"` (Uninstalled, quit, refunded).
- Frustration targets: `"숙제 너무 많다"`, `"노잼"`, `"가챠 천장 못찍겠다"`, `"운빨 망겜"` (Too much daily grind, boring, bad gacha luck).
- **Target Flagging:** If a post meets these criteria, assign `churn_risk: true` and summarize the `churn_trigger` (e.g., "Grind burnout").

**2. Linguistic Markers for Loyalty (리텐션 징후):**
- Returning users: `"연어 짓"`, `"복귀 유저인데"`, `"갓패치"` (Returning player, god-tier patch).
- Social endorsement: `"친구 꼬셔서 시작함"`, `"길드 모집"`, `"오랜만에 할만하다"` (Recruiting friends/guilds, finally fun again).
- Commitment: `"배틀패스 샀다"`, `"과금 할맛 난다"` (Bought the pass, willingly paying).
- **Target Flagging:** If a post meets these criteria, assign `loyalty_signal: true` and summarize the `loyalty_trigger` (e.g., "Good QoL patch").

## Output Requirements
- Maintain all existing metadata (`post_id`, `sentiment_score`, `category`, etc.).
- Append `churn_risk` (boolean), `churn_trigger` (string), `loyalty_signal` (boolean), `loyalty_trigger` (string).
- Save the final augmented data to `.tmp/analyzed_results.json`.
- Do NOT commit this output file.
