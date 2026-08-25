import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
KEY = os.getenv('KEY')
TYPE = os.getenv('TYPE')

SERVICE_NAME = "TbUseDaystatusView"
DIR_NAME = "hangang_park_daily_info"
DATE_COL = "DT"  # 실제 사용 중인 날짜 컬럼명

def fetch_recent_data(fetch_limit: int = 1000) -> pd.DataFrame:
    """최신 N건의 데이터만 빠르게 조회 (스케줄러 전용)"""
    endpoint = f"{BASE_URL}/{KEY}/{TYPE}/{SERVICE_NAME}/1/{fetch_limit}"
    res = requests.get(endpoint)
    
    if res.status_code == 200:
        data = res.json()
        rows = data.get(SERVICE_NAME, {}).get('row', [])
        return pd.DataFrame(rows)
    else:
        print(f"API 호출 실패: HTTP {res.status_code}")
        return pd.DataFrame()

def sync_daily_files(df: pd.DataFrame):
    """가져온 최신 데이터를 해당 날짜 파일에 중복 없이 병합 (Upsert)"""
    if df.empty or DATE_COL not in df.columns:
        print("동기화할 데이터가 없습니다.")
        return

    save_dir = f"../data/raw/{DIR_NAME}"
    os.makedirs(save_dir, exist_ok=True)

    df['_clean_date'] = df[DATE_COL].astype(str).str.replace(r'[-/.\s]', '', regex=True).str[:8]

    for date_val, group in df.groupby('_clean_date'):
        clean_group = group.drop(columns=['_clean_date'])
        file_path = f"{save_dir}/{DIR_NAME}_{date_val}.csv"

        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path, dtype=str)
            # 기존 파일과 새 데이터를 합친 후 중복 행 제거
            combined_df = pd.concat([existing_df, clean_group.astype(str)]).drop_duplicates()
            combined_df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"[{date_val}] 기존 파일 갱신 완료 (총 {len(combined_df)}건)")
        else:
            clean_group.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"[{date_val}] 신규 일자 파일 생성 완료 ({len(clean_group)}건)")

if __name__ == "__main__":
    print("=== 일일 스케줄러 동기화 시작 ===")
    recent_df = fetch_recent_data(fetch_limit=1000)
    sync_daily_files(recent_df)
    print("=== 동기화 종료 ===")