import pandas as pd
import glob
import re

park_master = pd.read_csv('../data/raw/hangang_park_master.csv')

# 주차장 마스터 정보 정리
# 필요없는 컬럼 삭제
drop_cols = ['ADDR', 'BZENTY_TEL', 'OPER_BGNG_PRD', 'OPER_END_PRD']
park_master = park_master.drop(columns=drop_cols)
# 컬럼 정수형 변환
int_cols = [
    'PRK_CNT', 'PWDBS_PRK_CNT', 'PRD_PRK_CNT', 
    'EXMPTN_HR', 'BSC_HR', 'BSC_CRG', 
    'INTR_HR', 'INTR_CRG', 'PRVDY_CRG', 
    'WKLY_CRG', 'NGHT_CRG', 'PRD_AMT'
]
# 존재하는 컬럼만 지정하여 일괄 변환
dtype_dict = {col: 'int64' for col in int_cols if col in park_master.columns}
park_master = park_master.astype(dtype_dict)
# 저장
park_master.to_csv('../data/pre_processed/park_master.csv', index=False, encoding='utf-8-sig')

# 주차장 일별 정보
# 1. 대상 폴더 및 조회할 기간 설정 (YYYYMMDD 형식)
data_dir = "../data/raw/hangang_park_daily_info"
start_date = "20250823"
end_date = "20260824"

# 2. 폴더 내 모든 일별 CSV 파일 목록 가져오기
file_list = glob.glob(f"{data_dir}/hangang_park_daily_info_*.csv")

target_dfs = []

# 3. 파일명에서 날짜 추출 후 기간 내 파일만 필터링
for file_path in file_list:
    # 파일명에서 8자리 숫자(날짜) 추출
    match = re.search(r'(\d{8})\.csv$', file_path)
    if match:
        file_date = match.group(1)
        
        # 시작일 ~ 종료일 사이인지 확인
        if start_date <= file_date <= end_date:
            df = pd.read_csv(file_path)
            target_dfs.append(df)

# 4. 하나의 DataFrame으로 병합
if target_dfs:
    daily_combined_df = pd.concat(target_dfs, ignore_index=True)
    print(f"병합 완료: 총 {len(target_dfs)}개 파일 / {daily_combined_df.shape[0]:,}개 행")
else:
    print(f"{start_date} ~ {end_date} 기간에 해당하는 파일이 없습니다.")

daily_combined_df.to_csv(f'../data/pre_processed/park_daily_info_{start_date}_{end_date}.csv', index=False, encoding='utf-8-sig')