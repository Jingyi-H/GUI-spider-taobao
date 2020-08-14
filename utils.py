import re
import hashlib
import time
import datetime as dt
import sys
import os

def get_sign(token, t, appKey, data):
    pre_sign = token + '&' + t + '&' + appKey + '&' + data
    sign = hashlib.md5(pre_sign.encode(encoding='UTF-8')).hexdigest()
    return sign

def get_token(cookie):
    cookie2token = re.compile("_m_h5_tk=[\da-z]*")
    token = re.findall(cookie2token, cookie)[0].replace("_m_h5_tk=", "")
    return token

def get_start_time():
    # 起始时间
    start_date = dt.date.today() - dt.timedelta(days=7)
    # 转为毫秒级时间戳
    start_time = int(time.mktime(start_date.timetuple()) * 1000.0)

    return start_time

def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)  # 使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)  # 没打包前的py目录
