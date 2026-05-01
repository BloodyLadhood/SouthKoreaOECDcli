import pandas as pd
import requests
import io
from datetime import datetime

def update_korea_cli():
    # 1. OECD API URL 수정 (전체 기간을 가져오도록 더 포괄적인 주소 사용)
    # 2026년 4월 현재 데이터까지 모두 포함할 수 있도록 쿼리를 확장했습니다.
    url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI,4.0/KOR.M.LI...AA...H?startPeriod=2015-01&dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        
        # 2. 정렬 로직 강화 (시간순으로 제대로 정렬되어야 MoM 계산이 정확함)
        if 'TIME_PERIOD' in df.columns:
            df = df.sort_values('TIME_PERIOD')
        
        # 3. 파일로 저장
        df.to_csv("korea_cli_history.csv", index=False)
        
        # 4. 제대로 가져왔는지 데이터 날짜 확인 출력
        last_date = df['TIME_PERIOD'].iloc[-1] if 'TIME_PERIOD' in df.columns else "알 수 없음"
        print(f"갱신 완료: {datetime.now()}")
        print(f"최신 데이터 시점: {last_date}") # 여기서 2026년 근처인지 확인 가능!
    else:
        print(f"데이터 호출 실패: {response.status_code}")

if __name__ == "__main__":
    update_korea_cli()