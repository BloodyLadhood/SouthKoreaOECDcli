import pandas as pd
import requests
import io
import sys
from datetime import datetime

def scrape_oecd_cli():
    # 웹 데이터 익스플로러가 사용하는 최신 데이터 쿼리 경로입니다.
    # API가 막혔을 때 웹 페이지에서 데이터를 강제로 호출하는 방식입니다.
    url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_CLI@DF_CLI,1.0/KOR.M.LI...AA...H?startPeriod=2015-01&dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 데이터 읽기
        df = pd.read_csv(io.StringIO(response.text))
        
        if df.empty:
            print("웹에서 가져온 데이터가 비어 있습니다.")
            sys.exit(1)

        # 시간순 정렬 및 저장
        if 'TIME_PERIOD' in df.columns:
            df = df.sort_values('TIME_PERIOD')
            df.to_csv("korea_cli_history.csv", index=False)
            
            last_date = df['TIME_PERIOD'].max()
            print(f"✅ 웹 크롤링 성공: {last_date}까지 업데이트 완료")
        else:
            print("데이터 구조가 변경되었습니다. 컬럼을 확인하세요.")
            sys.exit(1)

    except Exception as e:
        print(f"⚠️ 크롤링 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    scrape_oecd_cli()