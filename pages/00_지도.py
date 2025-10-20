# app.py
# Streamlit app: Seoul Top 10 Tourist Spots (EN/KR toggle + category filter + images)

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top 10 Tourist Spots", layout="wide")

# ------------------------------
# 🔤 Language Toggle
# ------------------------------
lang = st.sidebar.radio("🌏 Language / 언어 선택", ["English", "한국어"])

# ------------------------------
# 📊 Data
# ------------------------------
DATA = [
    {
        "name_en": "Gyeongbokgung Palace",
        "name_kr": "경복궁",
        "lat": 37.5779, "lon": 126.9768,
        "emoji": "🏯",
        "category": "History",
        "desc_en": "The main royal palace of the Joseon Dynasty. Famous for the Changing of the Guard and Hanbok experience.",
        "desc_kr": "조선시대 대표 궁궐. 수문장 교대식과 한복 체험이 인기예요.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Gyeongbokgung_Geunjeongjeon_2014.JPG/640px-Gyeongbokgung_Geunjeongjeon_2014.JPG"
    },
    {
        "name_en": "N Seoul Tower (Namsan Tower)",
        "name_kr": "N서울타워 (남산타워)",
        "lat": 37.5512, "lon": 126.9882,
        "emoji": "🗼",
        "category": "View",
        "desc_en": "An iconic observation tower with panoramic views of Seoul. Great for night views and love locks.",
        "desc_kr": "서울 전경을 한눈에! 야경과 사랑의 자물쇠 명소.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/N_Seoul_Tower_2023.jpg/640px-N_Seoul_Tower_2023.jpg"
    },
    {
        "name_en": "Bukchon Hanok Village",
        "name_kr": "북촌한옥마을",
        "lat": 37.5826, "lon": 126.9830,
        "emoji": "🏘️",
        "category": "Culture",
        "desc_en": "A traditional Korean village filled with Hanok houses. Perfect for walks and photos.",
        "desc_kr": "전통 한옥이 모여있는 마을, 골목 산책과 사진 명소.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Bukchon_Hanok_Village_Seoul.jpg/640px-Bukchon_Hanok_Village_Seoul.jpg"
    },
    {
        "name_en": "Myeongdong",
        "name_kr": "명동",
        "lat": 37.5638, "lon": 126.9860,
        "emoji": "🛍️",
        "category": "Shopping",
        "desc_en": "A shopping paradise with street food and cosmetics shops.",
        "desc_kr": "쇼핑과 길거리 음식 천국. 화장품, 패션, 먹거리 체험 추천.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Myeongdong_Night_2023.jpg/640px-Myeongdong_Night_2023.jpg"
    },
    {
        "name_en": "Insadong",
        "name_kr": "인사동",
        "lat": 37.5740, "lon": 126.9849,
        "emoji": "🎎",
        "category": "Culture",
        "desc_en": "A cultural street with tea houses and craft shops. Great for souvenirs.",
        "desc_kr": "전통 공예품과 찻집이 많은 거리. 기념품 사기 좋아요.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Insadong_Street_Seoul.jpg/640px-Insadong_Street_Seoul.jpg"
    },
    {
        "name_en": "Hongdae",
        "name_kr": "홍대",
        "lat": 37.5509, "lon": 126.9246,
        "emoji": "🎵",
        "category": "Nightlife",
        "desc_en": "The youth street with street performances, cafes, and clubs.",
        "desc_kr": "젊음의 거리! 거리공연, 카페, 클럽, 예술 감성 가득.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Hongdae_street.jpg/640px-Hongdae_street.jpg"
    },
    {
        "name_en": "Dongdaemun Design Plaza (DDP)",
        "name_kr": "동대문디자인플라자 (DDP)",
        "lat": 37.5663, "lon": 127.0090,
        "emoji": "🏛️",
        "category": "Design",
        "desc_en": "A futuristic landmark with architecture, fashion, and night lights.",
        "desc_kr": "미래형 건축물과 야경이 멋진 디자인 명소.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Dongdaemun_Design_Plaza_night_view_2015.jpg/640px-Dongdaemun_Design_Plaza_night_view_2015.jpg"
    },
    {
        "name_en": "Lotte World Tower",
        "name_kr": "롯데월드타워",
        "lat": 37.5131, "lon": 127.1024,
        "emoji": "🏙️",
        "category": "View",
        "desc_en": "The tallest building in Korea. Includes a sky tower, mall, and aquarium.",
        "desc_kr": "초고층 전망대, 대형 쇼핑몰, 아쿠아리움까지 한 번에.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Lotte_World_Tower_2017.jpg/640px-Lotte_World_Tower_2017.jpg"
    },
    {
        "name_en": "Changdeokgung Palace & Huwon",
        "name_kr": "창덕궁과 후원",
        "lat": 37.5796, "lon": 126.9911,
        "emoji": "🌿",
        "category": "History",
        "desc_en": "A UNESCO World Heritage site known for its secret garden tours.",
        "desc_kr": "유네스코 세계유산 궁궐, 후원(비원) 투어 추천.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Changdeokgung_Injeongjeon.jpg/640px-Changdeokgung_Injeongjeon.jpg"
    },
    {
        "name_en": "Namdaemun Market",
        "name_kr": "남대문시장",
        "lat": 37.5594, "lon": 126.9770,
        "emoji": "🍢",
        "category": "Shopping",
        "desc_en": "A traditional market with local foods and souvenirs.",
        "desc_kr": "전통시장과 길거리 음식의 천국. 기념품 쇼핑 필수!",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Namdaemun_Market_Seoul_2019.jpg/640px-Namdaemun_Market_Seoul_2019.jpg"
    },
]

df = pd.DataFrame(DATA)

# ------------------------------
# 🎨 Category Filter
# ------------------------------
categories = df["category"].unique().tolist()
selected_cats = st.sidebar.multiselect(
    "🗂️ Select Category / 카테고리 선택",
    options=categories,
    default=categories
)
df_filtered = df[df["category"].isin(selected_cats)]

# ------------------------------
# 🗺️ Map Display
# ------------------------------
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
cluster = MarkerCluster().add_to(m)

for _, row in df_filtered.iterrows():
    name = row["name_en"] if lang == "English" else row["name_kr"]
    desc = row["desc_en"] if lang == "English" else row["desc_kr"]
    popup_html = f"""
        <b>{row['emoji']} {name}</b><br/>
        <img src='{row['img']}' width='200'><br/>
        {desc}
    """
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=name,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(cluster)

st.header("🗺️ " + ("Seoul Top 10 Tourist Spots" if lang == "English" else "서울 인기 관광지 TOP 10"))
st_folium(m, width=1100, height=650)

# ------------------------------
# 🖼️ Image Gallery
# ------------------------------
st.subheader("📸 " + ("Photo Highlights" if lang == "English" else "대표 사진 보기"))
cols = st.columns(3)
for i, (_, row) in enumerate(df_filtered.iterrows()):
    with cols[i % 3]:
        st.image(row["img"], use_container_width=True)
        st.caption(f"{row['emoji']} {row['name_en'] if lang == 'English' else row['name_kr']}")

st.caption("Made with ❤️ using Streamlit + Folium")
