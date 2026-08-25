import pandas as pd

holiday = pd.read_csv('../data/raw/holiday.csv', encoding='cp949')

# '공휴일' 컬럼만 가져와서 이름을 'date'로 변경 (나머지 컬럼 자동 제거)
holiday = holiday[['공휴일']].rename(columns={'공휴일': 'date'})

# 2026년 공휴일 목록 (대체공휴일 포함)
holidays_2026 = [
    '2026-01-01',  # 신정
    '2026-02-16',  # 설날 연휴
    '2026-02-17',  # 설날
    '2026-02-18',  # 설날 연휴
    '2026-03-01',  # 삼일절
    '2026-03-02',  # 삼일절 대체공휴일
    '2026-05-05',  # 어린이날
    '2026-05-24',  # 부처님오신날
    '2026-05-25',  # 부처님오신날 대체공휴일
    '2026-06-03',  # 제9회 전국동시지방선거
    '2026-06-06',  # 현충일
    '2026-08-15',  # 광복절
    '2026-08-17',  # 광복절 대체공휴일
    '2026-09-24',  # 추석 연휴
    '2026-09-25',  # 추석
    '2026-09-26',  # 추석 연휴
    '2026-10-03',  # 개천절
    '2026-10-05',  # 개천절 대체공휴일
    '2026-10-09',  # 한글날
    '2026-12-25',  # 성탄절
]

# 2026년 DataFrame 생성
df_2026 = pd.DataFrame({'date': holidays_2026})

# 병합 -> 중복 제거 -> 날짜 내림차순(최신순) 정렬
holiday = pd.concat([holiday, df_2026], ignore_index=True)
holiday = (
    holiday.drop_duplicates()
    .sort_values(by='date', ascending=False)
    .reset_index(drop=True)
)

# 문자열 기준 2025년 또는 2026년으로 시작하는 행만 필터링
holiday = holiday[holiday['date'].astype(str).str.startswith(('2025', '2026'))].reset_index(drop=True)

# 확인
# print(holiday.tail())

holiday.to_csv(f'../data/pre_processed/holiday_25_26.csv', index=False, encoding='utf-8-sig')