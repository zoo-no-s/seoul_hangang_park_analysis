{{ config(materialized='table') }}

WITH daily_info AS (
    SELECT * FROM {{ ref('stg_park_daily_info') }}
),
park_master AS (
    SELECT * FROM {{ ref('stg_park_master') }}
),
holiday AS (
    SELECT * FROM {{ ref('stg_holiday') }}
),
weather AS (
    SELECT * FROM {{ ref('stg_weather') }}
)

SELECT i.DSTRCT_TYPE AS DSTRCT_CODE
        , i.PKLT_NM
        , i.PRK_CNTOM
        , i.UTZTN_HR
        , i.DT
        , m.*
        , CASE
            WHEN h.date IS NOT NULL THEN TRUE
            ELSE FALSE
        END AS is_holiday
        , w.temp
        , w.precip
FROM daily_info AS i
LEFT JOIN park_master AS m
ON i.PKLT_NM = m.PKLT_TYPE
LEFT JOIN holiday AS h
ON i.DT = h.date
LEFT JOIN weather AS w
ON i.DT = w.date