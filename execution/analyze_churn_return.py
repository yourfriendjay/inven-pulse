import os
import json

TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp')
INPUT_FILE = os.path.join(TMP_DIR, 'classified_data.json')
OUTPUT_FILE = os.path.join(TMP_DIR, 'analyzed_results.json')

# Markers from Directive 03
CHURN_MARKERS = ["계정 팔", "처분", "회수", "삭제", "접음", "환불", "숙제너무", "노잼", "망겜", "스트레스"]
LOYALTY_MARKERS = ["연어", "복귀", "갓패치", "할만하다", "배틀패스", "충성", "시작함", "추천"]

def detect_signals(text):
    text_c = text.replace(" ", "").lower()
    
    churn_risk = False
    loyalty_signal = False
    churn_trigger = ""
    loyalty_trigger = ""
    
    for marker in CHURN_MARKERS:
        if marker in text_c:
            churn_risk = True
            churn_trigger = f"Found marker: {marker}"
            break
            
    for marker in LOYALTY_MARKERS:
        if marker in text_c:
            loyalty_signal = True
            loyalty_trigger = f"Found marker: {marker}"
            break

    return churn_risk, loyalty_signal, churn_trigger, loyalty_trigger

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    analyzed_data = []
    
    for post in data:
        text = post.get('content_snippet', '') if post.get('content_snippet') else post.get('title', '')
        
        churn_risk, loyalty, churn_trigger, loyalty_trigger = detect_signals(text)
        
        post['churn_risk'] = churn_risk
        post['loyalty_signal'] = loyalty
        post['churn_trigger'] = churn_trigger
        post['loyalty_trigger'] = loyalty_trigger
        
        analyzed_data.append(post)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(analyzed_data, f, ensure_ascii=False, indent=2)

    print(f"Analyzed {len(analyzed_data)} posts for Churn/Loyalty. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
