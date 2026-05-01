import pandas as pd
import requests
import io
from datetime import datetime

def update_korea_cli():
    # 파라미터를 최소화하여 OECD가 보유한 최신 데이터를 통째로 가져오는 주소입니다.
    # 최신 규격(DSD_CLI) 경로
url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_CLI@DF_CLI,1.0/KOR.M.LI...AA...H?dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            
            # 중복 제거 및 시간순 정렬로 데이터 무결성 확보
            if 'TIME_PERIOD' in df.columns:
                df = df.drop_duplicates(subset=['TIME_PERIOD'])
                df = df.sort_values('TIME_PERIOD')
            
            # 새롭게 파일을 생성하여 저장
            df.to_csv("korea_cli_history.csv", index=False)
            
            last_date = df['TIME_PERIOD'].max()
            print(f"✅ 새 파일 생성 완료: {datetime.now()}")
            print(f"📅 최신 데이터 확인: {last_date}")
        else:
            print(f"❌ 호출 실패: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 오류: {e}")

if __name__ == "__main__":
    update_korea_cli()