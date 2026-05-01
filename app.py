import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Korea CLI & Export Monitor", layout="wide")

st.title("📈 대한민국 경기선행지수(CLI) 실시간 모니터링")
st.write("OECD API로부터 자동 수집된 데이터를 분석합니다.")

# 데이터 로드
try:
    df = pd.read_csv("korea_cli_history.csv")
    
    # 시간순 정렬 및 MoM 계산
    df = df.sort_values('TIME_PERIOD')
    df['MoM'] = df['Value'].diff() # 전월 대비 증감액
    
    # 최신 데이터 요약
    latest_val = df.iloc[-1]['Value']
    latest_mom = df.iloc[-1]['MoM']
    
    col1, col2 = st.columns(2)
    col1.metric("최신 CLI (Absolute)", f"{latest_val:.2f}")
    col2.metric("전월 대비 변동 (MoM)", f"{latest_mom:.4f}", delta=f"{latest_mom:.4f}")

    # 차트 그리기
    st.subheader("CLI 지수 및 MoM 추이")
    fig = px.line(df, x='TIME_PERIOD', y='Value', title='Korea CLI (Absolute)')
    st.plotly_chart(fig, use_container_width=True)
    
    fig_mom = px.bar(df, x='TIME_PERIOD', y='MoM', title='CLI MoM (Relative Speed)')
    st.plotly_chart(fig_mom, use_container_width=True)

except FileNotFoundError:
    st.error("아직 korea_cli_history.csv 파일이 생성되지 않았습니다. GitHub Actions를 먼저 실행해주세요.")