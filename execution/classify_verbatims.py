import os
import json
import time
from dotenv import load_dotenv

# Optional: Using OpenAI. In a real environment, you'd likely use the openai package.
# Here we mock the LLM logic or use a simple API wrapper if the key is available.
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv()

TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp')
INPUT_FILE = os.path.join(TMP_DIR, 'raw_scraped_data.json')
OUTPUT_FILE = os.path.join(TMP_DIR, 'classified_data.json')

def call_llm_classification(client, post):
    """Call LLM to classify the post. Returns category, sentiment, and reasoning."""
    # If no content snippet, use the title.
    text_to_analyze = post.get('content_snippet', '')
    if not text_to_analyze or text_to_analyze.startswith('['):
        text_to_analyze = post.get('title', '')
        
    prompt = f"""
    Analyze the following user post from a Korean gaming community:
    "{text_to_analyze}"
    
    Classify it into one of these categories: Combat_Mechanics, Monetization, Graphics_Optimization, Server_Stability, Other.
    Assign a sentiment score between -1.0 (Very Negative) and 1.0 (Very Positive).
    Provide a 1-sentence reasoning for the classification.
    
    Respond STRICTLY in JSON format:
    {{"category": "category_name", "sentiment_score": 0.5, "reasoning": "explain why"}}
    """
    
    # MOCK LOGIC for safety if no API key is provided, ensuring pipeline works out of the box.
    if not client or not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'sk-your-openai-key-here':
        return mock_classification(text_to_analyze)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a specialized game market research assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        result = json.loads(response.choices[0].message.content)
        return {
            'category': result.get('category', 'Other'),
            'sentiment_score': float(result.get('sentiment_score', 0.0)),
            'reasoning': result.get('reasoning', '')
        }
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return {'category': 'Other', 'sentiment_score': 0.0, 'reasoning': f'Error: {str(e)}'}

def mock_classification(text):
    """Fallback mock logic if no API key."""
    text_lower = text.lower()
    category = "Other"
    sentiment = 0.0
    reasoning = "Neutral discussion."
    
    if any(w in text_lower for w in ['과금', '가챠', '천장', '돈', '패스']):
        category = "Monetization"
        sentiment = -0.8
        reasoning = "과금과 확률을 부정적으로 언급함."
    elif any(w in text_lower for w in ['밸런스', '사기', '너프', '직업']):
        category = "Combat_Mechanics"
        sentiment = -0.5
        reasoning = "특정 직업의 밸런스 패치에 불만."
    elif any(w in text_lower for w in ['서버', '대기열', '점검', '렉']):
        category = "Server_Stability"
        sentiment = -0.9
        reasoning = "서버 렉이나 점검에 대한 불만."
    elif any(w in text_lower for w in ['그래픽', '프레임', '최적화']):
        category = "Graphics_Optimization"
        sentiment = 0.5
        reasoning = "그래픽이나 최적화 상태 언급."
    return {'category': category, 'sentiment_score': sentiment, 'reasoning': reasoning}

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    client = None
    if OpenAI and os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'sk-your-openai-key-here':
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    else:
        print("Using Mock LLM Classification (No valid OPENAI_API_KEY found)")

    classified_data = []
    print(f"Classifying {len(data)} posts...")
    
    for i, post in enumerate(data):
        # We focus primarily on posts that got detailed snippets or high upvotes
        classification = call_llm_classification(client, post)
        
        # Merge dictionaries
        enriched_post = {**post, **classification}
        classified_data.append(enriched_post)
        
        if (i+1) % 10 == 0:
            print(f" Processed {i+1} / {len(data)}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(classified_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully classified {len(classified_data)} posts. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
