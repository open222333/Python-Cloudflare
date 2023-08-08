from configparser import ConfigParser
import logging
import json
import os


conf = ConfigParser()
conf.read(os.path.join('conf', 'config.ini'))

'''
; ******log設定******
; 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
; LOG_DISABLE=1

; 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 不關閉
; LOG_FILE_DISABLE=1

; logs路徑 預設 logs
; LOG_PATH=

; 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設 WARNING
; LOG_LEVEL=

; 指定log大小(輸入數字) 單位byte, 與 LOG_DAYS 只能輸入一項 若都輸入 LOG_SIZE優先
; LOG_SIZE=

; 指定保留log天數(輸入數字) 預設7
; LOG_DAYS=
'''

# logs相關參數
# 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
LOG_DISABLE = conf.getboolean('LOG', 'LOG_DISABLE', fallback=False)
# logs路徑 預設 logs
LOG_PATH = conf.get('LOG', 'LOG_PATH', fallback='logs')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = conf.get('LOG', 'LOG_LEVEL', fallback='WARNING')
# 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 關閉
LOG_FILE_DISABLE = conf.getboolean('LOG', 'LOG_FILE_DISABLE', fallback=True)

if LOG_DISABLE:
    logging.disable()

log_setting = {
    'LOG_PATH': LOG_PATH,
    'LOG_DISABLE': LOG_DISABLE,
    'LOG_FILE_DISABLE': LOG_FILE_DISABLE,
    'LOG_LEVEL': LOG_LEVEL,
}

# cloudflare設定json檔路徑 預設值 conf/cloudflare.json
CLOUDFLARE_JSON_PATH = conf.get('SETTING', 'CLOUDFLARE_JSON_PATH', fallback='conf/cloudflare.json')
if os.path.exists(CLOUDFLARE_JSON_PATH):
    with open(CLOUDFLARE_JSON_PATH, 'r') as f:
        CLOUDFLARE_INFO = json.loads(f.read())
else:
    CLOUDFLARE_INFO = []
