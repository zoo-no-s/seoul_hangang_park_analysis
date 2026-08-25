import math
import os
import time
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
KEY = os.getenv('KEY')
TYPE = os.getenv('TYPE')
CALL_LIMIT = 1000

# 대상 서비스 설정
SERVICE_NAME = "TbUseDaystatusView"
DIR_NAME = "hangang_park_daily_info"
DATE_COL = "DT"  # 실제 API 응답의 날짜 컬럼명 (필요 시 확인 후 변경)


def fetch_all_daily_data(service_name: str) -> pd.DataFrame:
    """전체 인덱스를 페이징 순회하여 수집"""
    endpoint = f"{BASE_URL}/{KEY}/{TYPE}/{service_name}"

    # 1. 전체 데이터 건수 조회
    res = requests.get(f"{endpoint}/1/1")
    if res.status_code != 200:
        print(f"초기 요청 실패: HTTP {res.status_code}")
        return pd.DataFrame()

    data = res.json()
    if service_name not in data or 'list_total_count' not in data[service_name]:
        print("응답에 데이터가 없거나 형식이 올바르지 않습니다.")
        return pd.DataFrame()

    total_count = data[service_name]['list_total_count']
    pages = math.ceil(total_count / CALL_LIMIT)
    print(f"[{service_name}] 총 {total_count}건 수집 시작 (총 {pages}회 요청)")

    all_rows = []
    for i in range(1, pages + 1):
        start_idx = (i - 1) * CALL_LIMIT + 1
        end_idx = min(i * CALL_LIMIT, total_count)

        page_res = requests.get(f"{endpoint}/{start_idx}/{end_idx}")
        if page_res.status_code == 200:
            rows = page_res.json().get(service_name, {}).get('row', [])
            all_rows.extend(rows)

        time.sleep(0.1)  # 서버 부하 방지용 딜레이

    return pd.DataFrame(all_rows)


def save_by_date(df: pd.DataFrame, dir_name: str, date_col: str):
    """날짜 컬럼을 기준으로 그룹화하여 일별 단일 CSV로 저장/병합"""
    if df.empty:
        print("수집된 데이터가 없습니다.")
        return

    # 날짜 컬럼 존재 여부 확인
    if date_col not in df.columns:
        print(f"에러: '{date_col}' 컬럼이 데이터에 없습니다. (실제 컬럼 목록: {list(df.columns)})")
        return

    save_dir = f"../data/raw/{dir_name}"
    os.makedirs(save_dir, exist_ok=True)

    # 날짜 포맷 정리 (특수문자 제거 후 8자리 YYYYMMDD 확보)
    df['_clean_date'] = df[date_col].astype(str).str.replace(r'[-/.\s]', '', regex=True).str[:8]

    # 날짜별 분할 저장
    for date_val, group in df.groupby('_clean_date'):
        clean_group = group.drop(columns=['_clean_date'])
        file_path = f"{save_dir}/{dir_name}_{date_val}.csv"

        if os.path.exists(file_path):
            # 기존 파일이 있다면 병합 후 중복 행 제거 (스케줄링 시 멱등성 유지)
            existing_df = pd.read_csv(file_path, dtype=str)
            combined_df = pd.concat([existing_df, clean_group.astype(str)]).drop_duplicates()
            combined_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        else:
            clean_group.to_csv(file_path, index=False, encoding='utf-8-sig')

    print(f"\n[성공] '{save_dir}' 경로에 총 {df['_clean_date'].nunique()}개 일자별 파일 적재 완료.")


def main():
    print(f"=== {SERVICE_NAME} 파이프라인 실행 ===")
    df = fetch_all_daily_data(SERVICE_NAME)
    save_by_date(df, DIR_NAME, DATE_COL)


if __name__ == "__main__":
    main()