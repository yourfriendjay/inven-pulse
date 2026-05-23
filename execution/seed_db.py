"""
Seed the SQLite database with realistic Korean gaming community data.
This ensures the SaaS dashboard has meaningful data to display immediately.
"""
import os
import sys
import sqlite3
import random
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from server.db import get_db_connection, init_db

SEED_DATA = [
    # === Lost Ark (로스트아크) ===
    {"post_id": "la_001", "game_name": "lostark", "title": "레이드 숙제 피로도 진짜 선 넘었다;;", "author": "모코코전사", "view_count": 18500, "upvotes": 2100, "content_snippet": "일단 숙제 너무 많고 딜사이클 너무 꼬여서 피로도가 엄청남. 캐릭 6개 돌리는데 주말 내내 걸림. 접음.", "category": "Combat_Mechanics", "sentiment_score": -0.85, "reasoning": "레이드 반복 숙제의 피로감과 접겠다는 의사 표현. 이탈 위험 높음.", "churn_risk": 1, "churn_trigger": "접음", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "la_002", "game_name": "lostark", "title": "그래픽 최적화 갓패치 인정합니다", "author": "아크메이지", "view_count": 9200, "upvotes": 780, "content_snippet": "배경 퀄리티랑 스킬 이펙트는 진짜 이번이 역대급. 프레임 드랍도 많이 고쳐짐. 갓패치.", "category": "Graphics_Optimization", "sentiment_score": 0.82, "reasoning": "그래픽 및 최적화 개선에 대한 순수 호평. 복귀 유저 유입 가능성.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "갓패치"},
    {"post_id": "la_003", "game_name": "lostark", "title": "에스더 가격 미쳤냐 400만원이면 차를 사지", "author": "무과금유저", "view_count": 32000, "upvotes": 4500, "content_snippet": "가챠 확률 이게 맞냐? 300만원 쓰고 천장이라니 계정 정리합니다. 에스더 무기 시스템 최악.", "category": "Monetization", "sentiment_score": -0.95, "reasoning": "최상위 장비의 과금 천장에 극도의 불만. 계정 정리 언급으로 이탈 확정적.", "churn_risk": 1, "churn_trigger": "계정 팔", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "la_004", "game_name": "lostark", "title": "신규 레이드 카멘 2관문 재밌긴 하다", "author": "레이더", "view_count": 11000, "upvotes": 620, "content_snippet": "패턴 자체는 역대급으로 재밌음. 근데 보상이 너무 짜서 문제. 재미는 인정하는데 보상을 좀...", "category": "Combat_Mechanics", "sentiment_score": 0.25, "reasoning": "전투 콘텐츠 자체에는 긍정적이나 보상 불만이 감성을 중화시킴.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "la_005", "game_name": "lostark", "title": "6개월만에 복귀했는데 할만하네", "author": "연어전사", "view_count": 7800, "upvotes": 890, "content_snippet": "연어 복귀했는데 생각보다 할만하다. 신규 콘텐츠도 괜찮고 복귀 보상도 짭짤함.", "category": "Other", "sentiment_score": 0.65, "reasoning": "장기 이탈 후 복귀한 유저의 긍정적 반응. 리텐션 시그널.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "연어"},
    {"post_id": "la_006", "game_name": "lostark", "title": "밸런스 패치 언제 하냐 기공사 죽었다", "author": "기공장인", "view_count": 14200, "upvotes": 1350, "content_snippet": "기공사 너프 이후로 파티 못 잡음. 밸런스 패치 안 하면 진짜 접는다. 직업 밸런스 최악.", "category": "Combat_Mechanics", "sentiment_score": -0.72, "reasoning": "특정 직업 너프 후 파티 매칭 어려움 호소. 이탈 가능성 시사.", "churn_risk": 1, "churn_trigger": "접음", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "la_007", "game_name": "lostark", "title": "이번 업데이트 서버 안정성 좋아졌다", "author": "핑체커", "view_count": 5500, "upvotes": 420, "content_snippet": "예전에 렉 심했는데 이번 점검 이후로 확실히 안정적. 거래소도 빨라짐.", "category": "Server_Stability", "sentiment_score": 0.55, "reasoning": "서버 안정성 개선에 대한 긍정적 피드백.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "la_008", "game_name": "lostark", "title": "스킨 가격 왜 이렇게 비싸냐 ㅋㅋ", "author": "패션왕", "view_count": 8900, "upvotes": 670, "content_snippet": "스킨 하나에 3만원은 좀... 다른 게임은 절반 가격인데. 그냥 기본 스킨 씀.", "category": "Monetization", "sentiment_score": -0.45, "reasoning": "스킨 가격에 대한 불만이나 이탈까지는 아닌 수준.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},

    # === Throne and Liberty (TL) ===
    {"post_id": "tl_001", "game_name": "tl", "title": "배틀패스 효율성 미쳤다 갓엔씨", "author": "엔씨바라기", "view_count": 24000, "upvotes": 2800, "content_snippet": "배틀패스 효율성 미쳤다. 이 정도면 혜자 아님? 돈 쓸 맛 나네. 충성유저 됨.", "category": "Monetization", "sentiment_score": 0.88, "reasoning": "배틀패스의 높은 효율에 극찬. 과금 만족도가 리텐션으로 직결.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "충성"},
    {"post_id": "tl_002", "game_name": "tl", "title": "가챠 확률 공지 다시 해라 장난하냐?", "author": "무과금전사", "view_count": 38000, "upvotes": 4200, "content_snippet": "가챠 확률 이게 맞냐? 300만원 쓰고 천장이라니 계정 정리하고 뜹니다. 환불 요청함.", "category": "Monetization", "sentiment_score": -0.92, "reasoning": "과금 확률에 대한 극도의 불만. 환불 및 계정 정리 언급.", "churn_risk": 1, "churn_trigger": "환불", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "tl_003", "game_name": "tl", "title": "변신 시스템 컨셉은 좋은데 밸런스가...", "author": "변신러버", "view_count": 15600, "upvotes": 1100, "content_snippet": "변신 시스템 자체는 혁신적인데 특정 변신이 너무 사기라서 PvP가 망가짐.", "category": "Combat_Mechanics", "sentiment_score": -0.35, "reasoning": "혁신적 시스템에 긍정적이나 밸런스 불균형에 불만.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "tl_004", "game_name": "tl", "title": "TL 그래픽 언리얼5 체감 실화냐", "author": "그래픽덕후", "view_count": 21000, "upvotes": 1900, "content_snippet": "진짜 그래픽 미쳤다. UE5 체감 확실히 됨. 배경 디테일이 역대급. 스크린샷 찍는 맛이 있음.", "category": "Graphics_Optimization", "sentiment_score": 0.91, "reasoning": "언리얼5 기반 그래픽 품질에 극찬. 시각적 만족도 최상.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "추천"},
    {"post_id": "tl_005", "game_name": "tl", "title": "서버 대기열 3천명 골든타임에 이게 뭐냐", "author": "대기열전사", "view_count": 29000, "upvotes": 3100, "content_snippet": "주말 골든타임인데 대기열 3천명에 서버 팅김. 렉도 심하고 스킬 안 나감. 스트레스 장난 아님.", "category": "Server_Stability", "sentiment_score": -0.88, "reasoning": "서버 불안정성에 대한 극도의 불만. 스트레스 키워드 포착.", "churn_risk": 1, "churn_trigger": "스트레스", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "tl_006", "game_name": "tl", "title": "TL 시작함 추천 빌드 알려주세요", "author": "뉴비TL", "view_count": 8900, "upvotes": 340, "content_snippet": "친구 추천으로 TL 시작함. 초반 스토리 재밌고 전투감 좋은데 빌드를 모르겠음.", "category": "Other", "sentiment_score": 0.60, "reasoning": "신규 유저 유입 확인. 초반 경험에 긍정적.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "시작함"},
    {"post_id": "tl_007", "game_name": "tl", "title": "거점전 밸런스 완전 붕괴됨 ㅋㅋ", "author": "PvP전문가", "view_count": 17500, "upvotes": 1450, "content_snippet": "거점전에서 특정 직업만 뛰어다니는 거 보면 밸런스가 얼마나 망가졌는지 체감됨.", "category": "Combat_Mechanics", "sentiment_score": -0.62, "reasoning": "PvP 콘텐츠의 직업 밸런스 붕괴에 대한 불만.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},

    # === Black Desert (검은사막) ===
    {"post_id": "bd_001", "game_name": "black", "title": "이번 거점전 서버 팅기고 난리남", "author": "흑정령기사", "view_count": 13500, "upvotes": 1100, "content_snippet": "거점전 중 서버 팅김. 렉 너무 심해서 스킬이 안 나감. 점검 좀 제대로 해라.", "category": "Server_Stability", "sentiment_score": -0.78, "reasoning": "대규모 PvP 중 서버 불안정성 호소. 인프라 개선 요구.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "bd_002", "game_name": "black", "title": "사막 사냥터 리뉴얼 갓패치다", "author": "사냥꾼", "view_count": 11200, "upvotes": 950, "content_snippet": "사냥터 리뉴얼 이후로 효율도 좋아지고 재미도 올라감. 갓패치 인정. 복귀할 만함.", "category": "Combat_Mechanics", "sentiment_score": 0.72, "reasoning": "사냥 콘텐츠 리뉴얼에 대한 호평. 복귀 유인 효과.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "갓패치"},
    {"post_id": "bd_003", "game_name": "black", "title": "펄 가격 또 올랐네 ㅋㅋ 진짜 돈독 올랐다", "author": "무과금생존기", "view_count": 22000, "upvotes": 2800, "content_snippet": "펄 가격 또 올림? 이미 스킨도 비싼데 편의 아이템까지 과금 필수. 노잼 돈먹는 하마.", "category": "Monetization", "sentiment_score": -0.82, "reasoning": "지속적인 과금 가격 인상에 대한 강한 불만. 노잼 키워드 포착.", "churn_risk": 1, "churn_trigger": "노잼", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "bd_004", "game_name": "black", "title": "리마스터 그래픽 체감 확실히 좋아졌다", "author": "스크린샷러", "view_count": 9800, "upvotes": 720, "content_snippet": "리마스터 적용하니까 그래픽이 확 달라짐. 특히 물 반사랑 그림자가 예술.", "category": "Graphics_Optimization", "sentiment_score": 0.78, "reasoning": "리마스터 그래픽 품질 향상에 만족. 시각적 경험 개선 확인.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "bd_005", "game_name": "black", "title": "강화 시스템 스트레스 받아서 접으려고 합니다", "author": "강화실패전문", "view_count": 19500, "upvotes": 2200, "content_snippet": "펜 도전 15번째 실패함. 장비 다 날아가고 은화도 없음. 스트레스 받아서 계정 처분 고민 중.", "category": "Monetization", "sentiment_score": -0.90, "reasoning": "강화 실패의 반복적 스트레스. 계정 처분 언급으로 이탈 위험 매우 높음.", "churn_risk": 1, "churn_trigger": "처분", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "bd_006", "game_name": "black", "title": "검은사막 7주년 이벤트 혜자네", "author": "이벤트헌터", "view_count": 16000, "upvotes": 1300, "content_snippet": "7주년 이벤트 보상 꽤 괜찮음. 연어들도 복귀할 만한 수준. 할만하다.", "category": "Other", "sentiment_score": 0.58, "reasoning": "기념 이벤트 보상에 긍정적. 복귀 유저 유입 가능성.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "할만하다"},
    {"post_id": "bd_007", "game_name": "black", "title": "신규 클래스 도사 밸런스 사기 아니냐", "author": "도사메인", "view_count": 14800, "upvotes": 1050, "content_snippet": "도사 출시 이후로 PvP 밸런스 완전 붕괴. 원콤 당하는 거 정상임? 너프 해라.", "category": "Combat_Mechanics", "sentiment_score": -0.55, "reasoning": "신규 클래스의 과도한 성능에 대한 불만. PvP 밸런스 지적.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},

    # === Aion 2 (아이온 2) ===
    {"post_id": "a2_001", "game_name": "aion2", "title": "아이온2 공중 전투 트레일러 보셨나요?", "author": "천족전사", "view_count": 28500, "upvotes": 1950, "content_snippet": "비행 시스템이랑 공중 전투 액션이 전작보다 훨씬 역동적임. 언리얼5 체감 확실히 납니다. 기대 폭발.", "category": "Combat_Mechanics", "sentiment_score": 0.85, "reasoning": "공중 전투 액션과 언리얼 엔진 5 그래픽에 대한 높은 기대감.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 1, "loyalty_trigger": "추천"},
    {"post_id": "a2_002", "game_name": "aion2", "title": "BM 어떻게 나올지가 제일 걱정이네", "author": "린저씨아님", "view_count": 31200, "upvotes": 2400, "content_snippet": "게임 잘 만들어놔도 리니지식 가챠나 뽑기 BM 그대로 가져오면 출시하자마자 망겜 소리 들을 듯.", "category": "Monetization", "sentiment_score": -0.65, "reasoning": "개발사의 기존 과금 모델에 대한 불신과 우려.", "churn_risk": 1, "churn_trigger": "망겜", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "a2_003", "game_name": "aion2", "title": "이번 시연회 그래픽 최적화 퀄리티", "author": "테스터", "view_count": 17800, "upvotes": 1200, "content_snippet": "시연회 플레이해봤는데 배경 그래픽은 미쳤습니다. 다만 다수 유저 몰릴 때 프레임 드랍이 좀 있음.", "category": "Graphics_Optimization", "sentiment_score": 0.40, "reasoning": "그래픽 자체는 호평이나 최적화(프레임 드랍) 이슈가 혼재함.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},
    {"post_id": "a2_004", "game_name": "aion2", "title": "오토나 작업장 서버 관리 제대로 할까", "author": "봇사냥꾼", "view_count": 12400, "upvotes": 850, "content_snippet": "초반에 오토 작업장들 판치면 대기열 3천명 걸리고 서버 터질텐데 제대로 대응해줬으면 좋겠다.", "category": "Server_Stability", "sentiment_score": -0.30, "reasoning": "서버 관리 및 불법 프로그램 대응에 대한 우려성 피드백.", "churn_risk": 0, "churn_trigger": "", "loyalty_signal": 0, "loyalty_trigger": ""},
]

def seed():
    init_db()
    conn = get_db_connection()
    c = conn.cursor()

    # Generate scraped_at dates spread over last 84 days
    now = datetime.now()

    # Loop 8 times to multiply the data for a denser dashboard
    for loop_idx in range(8):
        for i, post in enumerate(SEED_DATA):
            # Days spread over 12 weeks
            days_ago = random.randint(0, 84)
            hours_ago = random.randint(0, 23)
            scraped_at = now - timedelta(days=days_ago, hours=hours_ago)
            
            # Make unique ID
            unique_post_id = f"{post['post_id']}_{loop_idx}"

            try:
                c.execute('''
                    INSERT OR REPLACE INTO posts
                    (post_id, game_name, title, url, author, view_count, upvotes,
                     content_snippet, category, sentiment_score, reasoning,
                     churn_risk, churn_trigger, loyalty_signal, loyalty_trigger, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    unique_post_id, post['game_name'], post['title'],
                    f"https://inven.co.kr/board/{post['game_name']}/{unique_post_id}",
                    post['author'], post['view_count'], post['upvotes'],
                    post['content_snippet'], post['category'], post['sentiment_score'],
                    post['reasoning'], post['churn_risk'], post['churn_trigger'],
                    post['loyalty_signal'], post['loyalty_trigger'],
                    scraped_at.strftime('%Y-%m-%d %H:%M:%S')
                ))
            except Exception as e:
                print(f"Error: {e}")

    conn.commit()
    
    # Verify
    c.execute("SELECT game_name, COUNT(*) as cnt FROM posts GROUP BY game_name")
    rows = c.fetchall()
    for r in rows:
        print(f"  {r['game_name']}: {r['cnt']} posts")
    
    total = sum(r['cnt'] for r in rows)
    print(f"\n✅ Database seeded with {total} total posts.")
    conn.close()

if __name__ == "__main__":
    seed()
