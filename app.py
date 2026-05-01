import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정 #
st.set_page_config(page_title="Korea CLI & Export Monitor", layout="wide")

st.title("📈 대한민국 경기선행지수(CLI) 실시간 모니터링")
st.write("OECD API로부터 자동 수집된 데이터를 분석합니다.")

# 데이터 로드
try:
    df = pd.read_csv("korea_cli_history.csv")
    
    # 시간순 정렬 및 MoM 계산
    df = df.sort_values('TIME_PERIOD')
    
    # 컬럼명이 'Value'가 아닌 'OBS_VALUE'이므로 이를 반영하여 수정 [핵심 수정 부분]
    df['MoM'] = df['OBS_VALUE'].diff() # 전월 대비 증감액
    
    # 최신 데이터 요약
    latest_val = df.iloc[-1]['OBS_VALUE']
    latest_mom = df.iloc[-1]['MoM']
    
    col1, col2 = st.columns(2)
    col1.metric("최신 CLI (Absolute)", f"{latest_val:.2f}")
    col2.metric("전월 대비 변동 (MoM)", f"{latest_mom:.4f}", delta=f"{latest_mom:.4f}")

    # 차트 그리기
    st.subheader("CLI 지수 및 MoM 추이")
    # y축 데이터명을 'OBS_VALUE'로 변경
    fig = px.line(df, x='TIME_PERIOD', y='OBS_VALUE', title='Korea CLI (Absolute Trend)')
    st.plotly_chart(fig, use_container_width=True)
    
    fig_mom = px.bar(df, x='TIME_PERIOD', y='MoM', title='CLI MoM (Change Speed)')
    st.plotly_chart(fig_mom, use_container_width=True)

except FileNotFoundError:
    st.error("아직 korea_cli_history.csv 파일이 생성되지 않았습니다. GitHub Actions가 데이터를 수집할 때까지 잠시만 기다려주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")