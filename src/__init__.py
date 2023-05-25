from configparser import ConfigParser
import os


config = ConfigParser()
config.read(os.path.join('.config', 'config.ini'))

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

LOG_PATH = config.get('LOG', 'LOG_PATH', fallback='logs')
LOG_LEVEL = config.get('LOG', 'LOG_LEVEL', fallback='WARNING')
LOG_DISABLE = config.getboolean('LOG', 'LOG_DISABLE', fallback=False)
LOG_FILE_DISABLE = config.getboolean('LOG', 'LOG_FILE_DISABLE', fallback=False)
LOG_SIZE = config.get('LOG', 'LOG_SIZE', fallback=None)
LOG_DAYS = config.getint('LOG', 'LOG_DAYS', fallback=7)

CLOUDFLARE_EMAIL = config.get('CLOUDFLARE', 'CLOUDFLARE_EMAIL', fallback=None)
CLOUDFLARE_KEY = config.get('CLOUDFLARE', 'CLOUDFLARE_KEY', fallback=None)
CLOUDFLARE_TOKEN = config.get('CLOUDFLARE', 'CLOUDFLARE_TOKEN', fallback=None)


log_setting = {
    'LOG_PATH': LOG_PATH,
    'LOG_DISABLE': LOG_DISABLE,
    'LOG_FILE_DISABLE': LOG_FILE_DISABLE,
    'LOG_LEVEL': LOG_LEVEL,
    'LOG_DAYS': LOG_DAYS
}

if LOG_SIZE:
    log_setting['LOG_SIZE'] = LOG_SIZE
