import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
KEY = os.getenv('KEY')
TYPE = os.getenv('TYPE')

URL = f'{BASE_URL}/{KEY}/{TYPE}'

# 1. 전체 개수 조회
temp_res = requests.get(f'{URL}/TbParkingInfoView/1/1')

if temp_res.status_code == 200:
    data = temp_res.json()
    data_size = data['TbParkingInfoView']['list_total_count']
    
    # 2. 전체 데이터 조회
    res = requests.get(f'{URL}/TbParkingInfoView/1/{data_size}')
    
    if res.status_code == 200:
        rows = res.json()['TbParkingInfoView']['row']
        pd.DataFrame(rows).to_csv(f'../data/raw/hangang_park_master.csv', index=False, encoding='utf-8-sig')