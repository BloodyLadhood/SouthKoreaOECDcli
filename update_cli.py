import pandas as pd
import requests
import io
from datetime import datetime

def update_korea_cli():
    # OECD의 최신 데이터셋인 DSD_CLI@DF_CLI 경로를 사용하여 2026년 데이터를 타겟팅합니다.
    url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_CLI@DF_CLI,1.0/KOR.M.LI...AA...H?startPeriod=2015-01&dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            
            # 1. 시간순 정렬 (반드시 필요)
            if 'TIME_PERIOD' in df.columns:
                df = df.sort_values('TIME_PERIOD')
            
            # 2. 파일 저장
            df.to_csv("korea_cli_history.csv", index=False)
            
            last_date = df['TIME_PERIOD'].iloc[-1]
            print(f"✅ 갱신 완료: {datetime.now()}")
            print(f"📅 차트 최신 시점: {last_date}") # 여기서 2026년 데이터 확인!
        else:
            print(f"❌ 호출 실패: HTTP {response.status_code}")
    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")

if __name__ == "__main__":
    update_korea_cli()