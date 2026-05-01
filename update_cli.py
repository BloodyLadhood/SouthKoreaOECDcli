import pandas as pd
import requests
import io

def diagnose_oecd_data():
    # 현재 유효할 것으로 판단되는 세 가지 주요 경로를 모두 테스트합니다.
    test_urls = {
        "Legacy(구형)": "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI,4.0/KOR.M.LI...AA...H?dimensionAtObservation=AllDimensions&format=csvfilewithlabels",
        "New(신형-DSD_CLI)": "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_CLI@DF_CLI,1.0/KOR.M.LI...AA...H?dimensionAtObservation=AllDimensions&format=csvfilewithlabels",
        "Global(전체)": "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI,1.0/KOR.M.LI...AA...H?dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    }

    for name, url in test_urls.items():
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                last_date = df['TIME_PERIOD'].max()
                print(f"✅ {name} 경로 연결 성공! | 최신 데이터 시점: {last_date}")
            else:
                print(f"❌ {name} 경로 실패 (상태 코드: {response.status_code})")
        except Exception as e:
            print(f"⚠️ {name} 경로 오류 발생: {e}")

if __name__ == "__main__":
    diagnose_oecd_data()