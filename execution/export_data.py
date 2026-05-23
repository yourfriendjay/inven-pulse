import os
import json
import pandas as pd

TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp')
INPUT_FILE = os.path.join(TMP_DIR, 'analyzed_results.json')
OUTPUT_FILE = os.path.join(TMP_DIR, 'FINAL_DASHBOARD_DATA.csv')

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("No data to export.")
        return

    df = pd.DataFrame(data)
    
    # Select columns as per Directive 04
    columns_desired = [
        "game_name", "title", "category", "sentiment_score", 
        "churn_risk", "loyalty_signal", "reasoning", "url", 
        "upvotes", "view_count"
    ]
    
    # Only keep columns that actually exist in the dataframe
    cols = [c for c in columns_desired if c in df.columns]
    df = df[cols]
    
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"Exported data to CSV successfully: {OUTPUT_FILE}")
    print("This file acts as a fallback or dashboard backend deliverables representation.")

if __name__ == "__main__":
    main()
