import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="World MBTI Distribution", page_icon="🌍", layout="wide")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 선택
st.title("🌍 World MBTI Type Distribution Explorer")
st.markdown("**Select a country to explore its MBTI type distribution.**")

country = st.selectbox("Choose a country", sorted(df["Country"].unique()))

# 선택한 국가 데이터 필터링
selected = df[df["Country"] == country].iloc[0, 1:]  # Country 제외
data = pd.DataFrame({
    "MBTI": selected.index,
    "Percentage": selected.values
}).sort_values("Percentage", ascending=False)

# 색상 지정 (1등: 빨강, 나머지: 회색 그라데이션)
colors = ["#FF4B4B"] + [f"rgba(180,180,180,{0.9 - i*0.04})" for i in range(len(data)-1)]

# Plotly 그래프 생성
fig = px.bar(
    data,
    x="MBTI",
    y="Percentage",
    text="Percentage",
)

# 색상 직접 지정
for i, bar in enumerate(fig.data[0].y):
    fig.data[0].marker.color = colors

# 그래프 스타일 조정
fig.update_traces(
    texttemplate="%{text:.2%}",
    textposition="outside",
    marker_line_color="rgba(0,0,0,0.2)",
    marker_line_width=1.2
)
fig.update_layout(
    title=f"🇨🇴 {country} MBTI Distribution",
    xaxis_title="MBTI Type",
    yaxis_title="Percentage",
    yaxis_tickformat=".0%",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=14),
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 하단 설명
st.markdown(
    """
    ---
    📊 **Tip:** Hover over bars to see exact values.  
    🧠 Data Source: MBTI Distribution by Country
    """
)
