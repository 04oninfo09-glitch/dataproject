# app.py
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

# 페이지 기본 설정
st.set_page_config(page_title="서울 맛집 추천 🍽️", layout="wide")

# 타이틀
st.title("서울 맛집 추천 — 구별·가격·유형까지 완벽 가이드 ✨")
st.caption("서울의 찐맛집을 구, 가격, 사람유형별로 골라보자! 💡")

# --- 예시 데이터 (맛집 12개) ---
data = [
    {"name": "Jungsik (정식당)", "gu": "강남구", "price": 150000,
     "lat": 37.5164, "lon": 127.0479, "desc": "모던 한식 파인다이닝 — 기념일엔 여기지 🥂",
     "people": "데이트", "size": "2명", "emoji": "🍽️✨", "source": "https://guide.michelin.com"},
    {"name": "Mingles (밍글스)", "gu": "강남구", "price": 130000,
     "lat": 37.5131, "lon": 127.0350, "desc": "컨템포러리 한식 — 감성 한가득 💫",
     "people": "데이트", "size": "2~4명", "emoji": "🍷🍱", "source": "https://eater.com"},
    {"name": "Tosokchon Samgyetang (토속촌 삼계탕)", "gu": "종로구", "price": 20000,
     "lat": 37.5796, "lon": 126.9770, "desc": "전통 삼계탕 명가 — 부모님과 함께 👵👴",
     "people": "가족모임", "size": "3~6명", "emoji": "🥣🌿", "source": "https://tripadvisor.com"},
    {"name": "Gwangjang Market (광장시장)", "gu": "종로구", "price": 15000,
     "lat": 37.5704, "lon": 126.9993, "desc": "길거리 음식 천국 — 친구들이랑 먹방 투어 🍢",
     "people": "소규모모임", "size": "2~5명", "emoji": "🌯🔥", "source": "https://tripadvisor.com"},
    {"name": "Balwoo Gongyang (발우공양)", "gu": "종로구", "price": 60000,
     "lat": 37.5700, "lon": 126.9848, "desc": "사찰 음식 기반 건강식 — 힐링 모드 🧘‍♀️",
     "people": "소규모모임", "size": "2~4명", "emoji": "🥢🍵", "source": "https://eater.com"},
    {"name": "Myeongdong Kyoja (명동교자)", "gu": "중구", "price": 12000,
     "lat": 37.5609, "lon": 126.9860, "desc": "칼국수 레전드 — 친구끼리 가성비 데이트 🍜",
     "people": "소규모모임", "size": "2~4명", "emoji": "🍜💛", "source": "https://tripadvisor.com"},
    {"name": "Noryangjin Fish Market (노량진 수산시장)", "gu": "동작구", "price": 40000,
     "lat": 37.5128, "lon": 126.9410, "desc": "싱싱한 해산물 직구 — 회식도 OK 👍",
     "people": "단체모임", "size": "4~10명", "emoji": "🐟🦐", "source": "https://eater.com"},
    {"name": "Hangaram Hanjeongsik (한가람 한정식)", "gu": "종로구", "price": 80000,
     "lat": 37.5739, "lon": 126.9768, "desc": "격식 있는 한정식 — 상견례나 부모님 모임 👨‍👩‍👧‍👦",
     "people": "가족모임", "size": "3~8명", "emoji": "🥂🍚", "source": "https://willflyforfood.net"},
    {"name": "Onjium (온지음)", "gu": "용산구", "price": 100000,
     "lat": 37.5296, "lon": 126.9806, "desc": "전통+모던 퓨전 한식 — 감성폭발 🎉",
     "people": "데이트", "size": "2~3명", "emoji": "🍱🌸", "source": "https://eater.com"},
    {"name": "Jokbal Alley (족발 골목)", "gu": "마포구", "price": 30000,
     "lat": 37.5509, "lon": 126.9180, "desc": "야식의 끝판왕 — 술친구 소환각 🍺",
     "people": "소규모모임", "size": "3~5명", "emoji": "🍖🍺", "source": "https://willflyforfood.net"},
    {"name": "Baekje Samgyetang (백제삼계탕)", "gu": "서초구", "price": 25000,
     "lat": 37.4932, "lon": 127.0130, "desc": "건강 보양식 — 부모님 효도 코스 👵",
     "people": "가족모임", "size": "3~6명", "emoji": "🍗🌿", "source": "https://tripadvisor.com"},
    {"name": "Mapo Galmaegi (마포갈매기)", "gu": "마포구", "price": 35000,
     "lat": 37.5522, "lon": 126.9544, "desc": "고기 구워먹기 딱! — 단체 회식 코스 🍖",
     "people": "단체모임", "size": "4~10명", "emoji": "🔥🥩", "source": "https://eater.com"},
]

df = pd.DataFrame(data)

# --- 구 선택창 ---
st.markdown("### 📍 구 선택하기")
gus = ["전체"] + sorted(df['gu'].unique().tolist())
selected_gu = st.selectbox("서울의 구를 골라보자 👇", gus, key="gu_selector")

# --- 가격대 선택창 ---
st.markdown("### 💰 가격대 선택 (1인 기준)")
price_ranges = ["전체", "0~50,000원", "50,000~100,000원", "100,000원 이상"]
selected_price = st.selectbox("가격대를 골라보자 💵", price_ranges, key="price_selector")

# 가격대 필터링
if selected_price == "0~50,000원":
    df = df[df["price"] <= 50000]
elif selected_price == "50,000~100,000원":
    df = df[(df["price"] > 50000) & (df["price"] <= 100000)]
elif selected_price == "100,000원 이상":
    df = df[df["price"] > 100000]

# 구 필터링
if selected_gu != "전체":
    df = df[df["gu"] == selected_gu]

# --- 탭 설정 (함께하는 사람 유형별) ---
st.markdown("### 👥 함께하는 사람 유형별 추천")
tabs = st.tabs(["💞 데이트", "👨‍👩‍👧‍👦 가족모임", "🍻 소규모모임", "🎉 단체모임"])
categories = ["데이트", "가족모임", "소규모모임", "단체모임"]

for i, tab in enumerate(tabs):
    with tab:
        subset = df[df["people"] == categories[i]]
        if subset.empty:
            st.info("해당 조건에 맞는 맛집이 아직 없어요 😅")
        else:
            for _, row in subset.iterrows():
                st.markdown(f"### {row['emoji']} {row['name']} — {row['gu']}")
                st.write(f"**설명:** {row['desc']}")
                st.write(f"**1인 평균 가격:** 약 {row['price']:,}원")
                st.write(f"**추천 인원:** {row['size']}")
                st.write(f"[출처 보기]({row['source']})")
                st.divider()

# --- Folium 지도 ---
st.subheader("🗺️ 서울 주요 맛집 지도")
if len(df) == 0:
    st.warning("조건에 맞는 맛집이 없습니다 😢")
else:
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="OpenStreetMap")

    for i, r in df.iterrows():
        popup_html = f"""
        <b>{r['emoji']} {r['name']}</b><br/>
        {r['desc']}<br/>
        💰 가격: {r['price']:,}원<br/>
        👥 유형: {r['people']} • 인원: {r['size']}<br/>
        <a href="{r['source']}" target="_blank">출처 보기</a>
        """
        folium.Marker(
            location=[r["lat"], r["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{r['name']} — {r['gu']}",
            icon=folium.Icon(color="red" if r["price"] > 100000 else "blue", icon="cutlery", prefix="fa")
        ).add_to(m)

    st_folium(m, width=900, height=500)

# --- 하단 안내 ---
st.markdown("---")
st.markdown("""
**🍴 꿀팁**  
- 💞 *데이트 맛집*은 조용하고 분위기 좋은 곳 위주!  
- 👨‍👩‍👧‍👦 *가족모임*은 좌식 or 룸이 있는 곳 추천!  
- 🍻 *소규모모임*은 접근성+가성비 굿!  
- 🎉 *단체모임*은 예약 필수, 단체석 있는 곳 중심!
""")

st.caption("데이터 출처: MICHELIN, Tripadvisor, Eater 등 (예시용)")
