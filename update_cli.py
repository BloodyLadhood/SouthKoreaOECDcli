import pandas as pd
import requests
import io
from datetime import datetime

def update_korea_cli():
    # OECD API URL (Korea CLI)
    url = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI,4.0/KOR.M.LI...AA...H?dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        
        # MoM(전월 대비 증감) 계산 로직 추가 가능
        # df['MoM'] = df['Value'].pct_change()
        
        # 파일로 저장
        df.to_csv("korea_cli_history.csv", index=False)
        print(f"갱신 완료: {datetime.now()}")
    else:
        print("데이터 호출 실패")

if __name__ == "__main__":
    update_korea_cli()