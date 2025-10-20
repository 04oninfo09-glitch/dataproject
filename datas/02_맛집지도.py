# app.py
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="서울 구별 맛집 추천 🍽️", layout="wide")

st.title("서울 구별 맛집 추천 — 찐맛집만 골라왔음 ✨")
st.caption("구를 선택하면 해당 구의 추천 맛집을 보여줘요. 지도에서 Top10도 확인 가능! 📍")

# --- 데이터: Top10 예시(간단 정보 포함) ---
# (실사용 시엔 API/DB로 대체 권장)
data = [
    {
        "name": "Jungsik (정식당)",
        "gu": "강남구",
        "lat": 37.5164,
        "lon": 127.0479,
        "desc": "모던 한식 파인다이닝 — 데이트/기념일 최적 🥂",
        "people": "연인 / 친구",
        "size": "2~4명",
        "emoji": "🍽️✨",
        "source": "https://guide.michelin.com"
    },
    {
        "name": "Tosokchon Samgyetang (토속촌 삼계탕)",
        "gu": "종로구",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "전통 삼계탕 명가 — 부모님 모시기 굿 👵👴",
        "people": "가족 / 연인",
        "size": "2~6명",
        "emoji": "🥣🌿",
        "source": "https://tripadvisor.com"
    },
    {
        "name": "Gwangjang Market (광장시장)",
        "gu": "종로구",
        "lat": 37.5704,
        "lon": 126.9993,
        "desc": "스트리트 푸드 천국 — 친구들이랑 술안주 투어 굿 🍢",
        "people": "친구 / 가족",
        "size": "2~6명",
        "emoji": "🌯🔥",
        "source": "https://tripadvisor.com"
    },
    {
        "name": "Mingles (밍글스)",
        "gu": "강남구",
        "lat": 37.5131,
        "lon": 127.0350,
        "desc": "컨템포러리 한식 — 고급스런 코스 경험 🥂",
        "people": "연인 / 가족",
        "size": "2~4명",
        "emoji": "🍷🍱",
        "source": "https://eater.com"
    },
    {
        "name": "Balwoo Gongyang (발우공양)",
        "gu": "종로구",
        "lat": 37.5700,
        "lon": 126.9848,
        "desc": "사찰 음식 기반의 건강식 — 힐링 코스 🧘‍♀️",
        "people": "가족 / 혼밥",
        "size": "1~4명",
        "emoji": "🥢🍵",
        "source": "https://eater.com"
    },
    {
        "name": "Myeongdong Kyoja (명동교자)",
        "gu": "중구",
        "lat": 37.5609,
        "lon": 126.9860,
        "desc": "칼국수 레전드 — 가성비 데이트/친구OK 🍜",
        "people": "친구 / 연인",
        "size": "2~4명",
        "emoji": "🍜💛",
        "source": "https://tripadvisor.com"
    },
    {
        "name": "Noryangjin Fish Market (노량진 수산시장)",
        "gu": "동작구",
        "lat": 37.5128,
        "lon": 126.9410,
        "desc": "싱싱한 해산물 직구 후 즉석 회식 👍",
        "people": "친구 / 가족",
        "size": "3~8명",
        "emoji": "🐟🦐",
        "source": "https://eater.com"
    },
    {
        "name": "Hangaram Hanjeongsik (한가람 한정식)",
        "gu": "종로구",
        "lat": 37.5739,
        "lon": 126.9768,
        "desc": "전통 한정식 — 격식있는 자리에 추천 🙌",
        "people": "가족 / 비즈니스",
        "size": "2~8명",
        "emoji": "🥂🍚",
        "source": "https://willflyforfood.net"
    },
    {
        "name": "Onjium (온지음)",
        "gu": "용산구",
        "lat": 37.5296,
        "lon": 126.9806,
        "desc": "전통+모던 한식 퓨전 — 특별한 날 추천 🎉",
        "people": "연인 / 가족",
        "size": "2~4명",
        "emoji": "🍱🌸",
        "source": "https://eater.com"
    },
    {
        "name": "Jokbal Alley (족발 골목 — 예시)",
        "gu": "마포구",
        "lat": 37.5509,
        "lon": 126.9180,
        "desc": "야식의 끝판왕 — 술친구 소환각 🍺",
        "people": "친구",
        "size": "2~6명",
        "emoji": "🍖🍺",
        "source": "https://willflyforfood.net"
    },
]

df = pd.DataFrame(data)

# --- 사이드바: 구 선택 ---
gus = ["전체"] + sorted(df['gu'].unique().tolist())
selected_gu = st.sidebar.selectbox("구 선택 (필터)", gus)

# --- 메인: 리스트 표시 ---
st.subheader("추천 맛집 리스트")
if selected_gu != "전체":
    filtered = df[df['gu'] == selected_gu]
else:
    filtered = df

for _, row in filtered.iterrows():
    st.markdown(f"### {row['emoji']} {row['name']} — {row['gu']}")
    st.write(f"**설명:** {row['desc']}")
    st.write(f"**어울리는 사람 유형:** {row['people']}  •  **추천 인원:** {row['size']}")
    st.write(f"[출처 정보 보기]({row['source']})")
    st.divider()

# --- Folium 지도: Top10 마커 표시 ---
st.subheader("서울 주요 맛집 Top 10 지도 🗺️")
# 초기 지도 중심: 서울 중심
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles="OpenStreetMap")

# 사용자 선택한 구를 강조해서 줌하는 옵션
if selected_gu != "전체" and len(filtered) > 0:
    # 중심을 해당 구의 첫 장소로
    center = [filtered.iloc[0]['lat'], filtered.iloc[0]['lon']]
    m = folium.Map(location=center, zoom_start=13, tiles="OpenStreetMap")

# 마커 추가 (Top10)
for i, r in df.iterrows():
    popup_html = f"""
    <b>{r['emoji']} {r['name']}</b><br/>
    {r['desc']} <br/>
    <b>어울리는 사람:</b> {r['people']} • <b>추천 인원:</b> {r['size']}<br/>
    <a href="{r['source']}" target="_blank">출처 보기</a>
    """
    folium.Marker(
        location=[r['lat'], r['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{r['name']} — {r['gu']}",
        icon=folium.Icon(color="red" if i == 0 else "blue", icon="cutlery", prefix="fa")
    ).add_to(m)

# 지도 렌더
st_data = st_folium(m, width=900, height=500)

# --- 하단: 노트 및 팁 ---
st.markdown("---")
st.markdown("""
**팁**  
- 예약이 필요한 곳(Jungsik, Mingles 등)은 사전 예약 추천! 📅  
- 시장(광장시장, 노량진 등)은 줄과 붐빔을 각오해라... 근데 그게 매력임 😆  
- 데이터를 더 업데이트해서 동적 검색(메뉴, 가격대, 예약링크 등)을 넣어볼래? 그럼 DB 연결해줄게! 💾
""")

st.caption("데이터 출처(예시): MICHELIN, Tripadvisor, Eater, 여행 블로그 등(간단 표본). 실제 앱에선 최신화 권장.")
