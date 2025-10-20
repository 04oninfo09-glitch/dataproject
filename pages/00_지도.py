# app.py
# Streamlit app: Foreign visitors' favorite Seoul tourist spots Top 10
# How to run: streamlit run app.py

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top 10 (for Foreign Visitors)", layout="wide")

st.title("🇰🇷 Seoul — Top 10 Tourist Spots Loved by Foreign Visitors")
st.markdown(
    "서울을 방문한 외국인들이 가장 많이 찾는 명소 10곳을 소개합니다. "
    "지도를 클릭하면 간단한 설명과 추천 포인트를 볼 수 있어요!"
)

# ✅ 데이터: 외국인에게 인기 있는 서울 관광지 10곳
DATA = [
    {"name": "Gyeongbokgung Palace (경복궁)", "lat": 37.5779, "lon": 126.9768, "emoji": "🏯",
     "desc": "조선시대 대표 궁궐. 수문장 교대식과 한복 체험이 인기예요."},
    {"name": "N Seoul Tower (N서울타워, Namsan)", "lat": 37.5512, "lon": 126.9882, "emoji": "🗼",
     "desc": "서울 전경이 한눈에! 야경과 사랑의 자물쇠 명소."},
    {"name": "Bukchon Hanok Village (북촌한옥마을)", "lat": 37.5826, "lon": 126.9830, "emoji": "🏘️",
     "desc": "전통 한옥이 모여있는 마을, 골목 산책과 사진 명소."},
    {"name": "Myeongdong (명동)", "lat": 37.5638, "lon": 126.9860, "emoji": "🛍️",
     "desc": "쇼핑과 길거리 음식 천국. 화장품, 패션, 먹거리 체험 추천."},
    {"name": "Insadong (인사동)", "lat": 37.5740, "lon": 126.9849, "emoji": "🎎",
     "desc": "전통 공예품과 찻집이 많은 거리. 기념품 사기 좋아요."},
    {"name": "Hongdae (홍대)", "lat": 37.5509, "lon": 126.9246, "emoji": "🎵",
     "desc": "젊음의 거리! 거리공연, 카페, 클럽, 예술 감성 가득."},
    {"name": "Dongdaemun Design Plaza (DDP, 동대문디자인플라자)", "lat": 37.5663, "lon": 127.0090, "emoji": "🏛️",
     "desc": "미래형 건축물과 야경이 멋진 디자인 명소."},
    {"name": "Lotte World Tower (롯데월드타워)", "lat": 37.5131, "lon": 127.1024, "emoji": "🏙️",
     "desc": "초고층 전망대, 대형 쇼핑몰, 아쿠아리움까지 한 번에."},
    {"name": "Changdeokgung Palace & Huwon (창덕궁)", "lat": 37.5796, "lon": 126.9911, "emoji": "🌿",
     "desc": "유네스코 세계유산 궁궐, 후원(비원) 투어 추천."},
    {"name": "Namdaemun Market (남대문시장)", "lat": 37.5594, "lon": 126.9770, "emoji": "🍢",
     "desc": "전통시장과 길거리 음식의 천국. 기념품 쇼핑 필수!"}
]

df = pd.DataFrame(DATA)

# 🎚️ 사이드바
st.sidebar.header("지도 설정")
show_list = st.sidebar.checkbox("표시할 관광지 선택", value=True)
if show_list:
    selected = st.sidebar.multiselect(
        "지도에 표시할 장소", options=df["name"], default=df["name"]
    )
    df_map = df[df["name"].isin(selected)]
else:
    df_map = df

# 🗺️ 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, control_scale=True)
cluster = MarkerCluster().add_to(m)

for _, row in df_map.iterrows():
    popup_html = f"<b>{row['emoji']} {row['name']}</b><br/>{row['desc']}"
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row["name"],
        icon=folium.Icon(icon="info-sign", color="blue")
    ).add_to(cluster)

# 🖥️ 지도 표시
map_height = st.sidebar.slider("지도 높이 (px)", 400, 900, 650)
st_data = st_folium(m, width=1100, height=map_height)

# 📋 관광지 목록 보기
if st.checkbox("관광지 목록 보기", value=False):
    st.dataframe(df_map[["name", "emoji", "lat", "lon", "desc"]])

# 💾 CSV 다운로드
@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

csv = to_csv(df_map)
st.download_button("CSV로 내보내기", csv, "seoul_top10.csv", "text/csv")

st.caption("📍 Made with Streamlit & Folium — Seoul Top 10 Tourist Spots for Foreign Visitors")
