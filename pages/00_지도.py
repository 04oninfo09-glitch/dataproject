# File: streamlit_seoul_top10_app.py
# Streamlit app (single-file) to display Top 10 Seoul tourist spots popular with foreigners
# - Designed to run on Streamlit Cloud (Streamlit Community Cloud)
# - Includes an embedded folium map using streamlit_folium
# How to run locally:
# 1) create a virtualenv, install packages from requirements.txt
# 2) streamlit run streamlit_seoul_top10_app.py

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top 10 (for Foreign Visitors)", layout="wide")

st.title("🇰🇷 Seoul — Top 10 Tourist Spots Loved by Foreign Visitors")
st.markdown("간단한 설명: 서울의 외국인 방문객에게 인기 있는 대표 관광지 10곳을 지도에 표시합니다. 마커를 클릭하면 간단한 설명과 추천 포인트를 확인할 수 있어요.")

# Data: Top 10 attractions (name, lat, lon, brief description)
# Coordinates chosen for central, well-known points of each attraction.
DATA = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.5779,
        "lon": 126.9768,
        "emoji": "🏯",
        "desc": "Joseon 왕조의 대표 궁궐. 수문장 교대식(Changing of the Guard)과 한복 체험 포인트가 인기예요."
    },
    {
        "name": "N Seoul Tower (N서울타워, Namsan)",
        "lat": 37.5512,
        "lon": 126.9882,
        "emoji": "🗼",
        "desc": "서울을 한눈에 내려다볼 수 있는 전망대. 밤 야경과 사랑의 자물쇠로 유명합니다."
    },
    {
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "lat": 37.5826,
        "lon": 126.9830,
        "emoji": "🏘️",
        "desc": "전통 한옥이 모여있는 마을. 골목 산책과 사진 찍기 좋습니다."
    },
    {
        "name": "Myeongdong (명동)",
        "lat": 37.5638,
        "lon": 126.9860,
        "emoji": "🛍️",
        "desc": "쇼핑과 길거리 음식의 메카. 화장품 쇼핑과 다양한 길거리 먹거리 체험 추천."
    },
    {
        "name": "Insadong (인사동)",
        "lat": 37.5740,
        "lon": 126.9849,
        "emoji": "🎎",
        "desc": "전통 공예품과 찻집이 많은 문화 거리. 기념품 사기 좋습니다."
    },
    {
        "name": "Hongdae (홍대/홍익대거리)",
        "lat": 37.5509,
        "lon": 126.9246,
        "emoji": "🎵",
        "desc": "젊음의 거리, 스트리트 퍼포먼스와 카페, 클럽이 밀집한 곳. 밤문화와 예술 문화를 즐기세요."
    },
    {
        "name": "Dongdaemun Design Plaza (동대문디자인플라자, DDP)",
        "lat": 37.5663,
        "lon": 127.0090,
        "emoji": "🏛️",
        "desc": "미래지향적 건축물과 야간 조명이 멋진 DDP. 패션시장과 연계해 쇼핑도 가능."
    },
    {
        "name": "Lotte World Tower & Mall (롯데월드타워)",
        "lat": 37.5131,
        "lon": 127.1024,
        "emoji": "🏙️",
        "desc": "초고층 전망대와 대형 쇼핑몰, 아쿠아리움 등 복합문화공간. 강동/송파 지역의 랜드마크."
    },
    {
        "name": "Changdeokgung Palace & Huwon (창덕궁)",
        "lat": 37.5796,
        "lon": 126.9911,
        "emoji": "🌿",
        "desc": "유네스코 세계유산에 등록된 궁궐과 비원(후원). 가이드 투어를 추천합니다."
    },
    {
        "name": "Namdaemun Market (남대문시장)",
        "lat": 37.5594,
        "lon": 126.9770,
        "emoji": "🍢",
        "desc": "전통 시장 문화 체험과 길거리 음식 맛보기. 기념품 쇼핑하기 좋아요."
    }
]

# Convert to DataFrame
df = pd.DataFrame(DATA)

# Sidebar controls
st.sidebar.header("설정")
show_list = st.sidebar.checkbox("리스트 보기 (선택해서 지도에 표시)", value=True)
selected = None
if show_list:
    selection = st.sidebar.multiselect("지도에 표시할 관광지 선택", options=df['name'].tolist(), default=df['name'].tolist())
    df_map = df[df['name'].isin(selection)].reset_index(drop=True)
else:
    df_map = df.copy()

# Create base folium map centered on Seoul
seoul_center = [37.5665, 126.9780]
zoom_start = 12
m = folium.Map(location=seoul_center, zoom_start=zoom_start, control_scale=True)

# Add marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add markers
for _, row in df_map.iterrows():
    popup_html = f"<b>{row['emoji']} {row['name']}</b><br/>{row['desc']}"
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['name'],
        icon=folium.Icon(icon='info-sign')
    ).add_to(marker_cluster)

# Option: draw heatmap or lines? (kept simple)

# Display map in Streamlit
st.subheader("지도 (클릭하면 관광지 정보 보기)")
map_height = st.sidebar.slider("지도 높이 (px)", min_value=400, max_value=900, value=650)
st_data = st_folium(m, width=1100, height=map_height)

# Show table of selected spots
if st.checkbox("선택 항목 목록 보기", value=False):
    st.subheader("선택된 관광지 목록")
    st.dataframe(df_map[['name','emoji','lat','lon','desc']].rename(columns={'emoji':'이모지','desc':'설명'}))

# Provide download link for CSV
@st.cache_data
def df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv_data = df_to_csv(df_map)
st.download_button(label="CSV으로 내보내기", data=csv_data, file_name="seoul_top10_spots.csv", mime='text/csv')

st.markdown("---")
st.caption("Tip: Streamlit Cloud에 배포하려면 이 파일과 requirements.txt를 GitHub 저장소에 업로드한 뒤 Streamlit Community Cloud에 연동하세요.")

# -------------------------
# Below is a requirements.txt section for convenience. Save this as a separate file named `requirements.txt`
# -------------------------

# requirements.txt
# (Copy the lines below into a file named `requirements.txt` in the same repo.)

# ---------- requirements.txt START ----------
# streamlit and mapping libraries
# Note: streamlit-folium provides the st_folium component used to render folium maps inside Streamlit.
streamlit>=1.20.0
folium>=0.14.0
streamlit-folium>=0.11.0
pandas>=1.4.0
# ---------- requirements.txt END ----------
