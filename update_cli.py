import pandas as pd
import requests
import io
from datetime import datetime

def update_korea_cli():
    # OECD의 새로운 데이터 규격(DSD_CLI)을 사용하는 최신 URL입니다.
    # 2026년 현재까지의 데이터를 포함할 수 있도록 경로를 수정했습니다.
    url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_CLI@DF_CLI,1.0/KOR.M.LI...AA...H?startPeriod=2015-01&dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    
    try:
        # API 호출 시 타임아웃을 설정하여 안정성을 높입니다.
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            
            # 1. 시간순 정렬 (차트가 제대로 그려지기 위한 필수 단계)
            if 'TIME_PERIOD' in df.columns:
                df = df.sort_values('TIME_PERIOD')
            
            # 2. 파일 저장 (Streamlit이 읽어갈 파일)
            df.to_csv("korea_cli_history.csv", index=False)
            
            last_date = df['TIME_PERIOD'].iloc[-1]
            print(f"✅ 갱신 완료: {datetime.now()}")
            print(f"📅 차트 업데이트 시점: {last_date}") # 2026년 데이터가 뜨는지 확인하세요!
        else:
            print(f"❌ 호출 실패: HTTP {response.status_code} (OECD 서버 응답 없음)")
    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")

if __name__ == "__main__":
    update_korea_cli()