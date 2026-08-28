{{ config(materialized='table') }}

WITH join_table AS (
    SELECT * FROM {{ ref('mart_joined_table') }}
)

SELECT DT
        , DSTRCT_TYPE
        , PKLT_NM
        , CONCAT(PSTN_INFO_LAT, ',', PSTN_INFO_LOT) AS coordinate
        , PRK_CNT
        , PRK_CNTOM
        , UTZTN_HR
FROM join_table