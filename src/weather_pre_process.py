import pandas as pd

weather = pd.read_csv('../data/raw/OBS_ASOS_DD_20260825173030.csv', encoding='cp949')

# 1. 컬럼 선택 및 이름 변경
weather_df = weather[['일시', '평균기온(°C)', '일강수량(mm)']].rename(
    columns={
        '일시': 'date',
        '평균기온(°C)': 'temp',
        '일강수량(mm)': 'precip'
    }
)

# 2. 강수량 결측치(비 안 온 날) 0.0으로 대체 (선택 사항)
weather_df['precip'] = weather_df['precip'].fillna(0.0)

# 결과 확인
print(weather_df.head())

weather_df.to_csv(f'../data/pre_processed/weather_250823_260824.csv', index=False, encoding='utf-8-sig')