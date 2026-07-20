import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import time
import secrets
import random
import requests

EAPI_KEY = b"e82ckenh8dichen8"

def eapi_encrypt(url: str, body: dict):
    text = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
    message = f"nobody{url}use{text}md5forencrypt"
    digest = hashlib.md5(message.encode()).hexdigest()
    data = f"{url}-36cd479b6b5-{text}-36cd479b6b5-{digest}"
    cipher = AES.new(EAPI_KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return encrypted.hex().upper()

def get_headers() :
    timestamp = str(int(time.time() * 1000))
    device_id = secrets.token_hex(16).upper()
    return {
        "Referer": "https://music.163.com/",
        "Cookie": (
            f"osver=android; "
            f"appver=8.7.01; "
            f"os=android; "
            f"deviceId={device_id}; "
            f"channel=netease; "
            f"requestId={timestamp}_{random.randint(0, 999):04d}; "
            f"__remember_me=true"
        ),
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36 NeteaseMusic/8.7.01",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }

def search(keyword,limit,page,timeout=5):
    try:
        api_path = "/api/cloudsearch/pc"
        body = {
            "s": keyword,
            "type": 1,
            "limit": limit,
            "total": "true",
            "offset": (page - 1) * limit
        }
        params = eapi_encrypt(api_path, body)
        response = requests.post(
            "https://music.163.com/eapi/cloudsearch/pc",
            headers=get_headers(),
            data={
                "params": params
            },
            timeout=timeout
        )
        return response.json()
    except:
        return None
    
def lyric(id,timeout=5):
    try:
        api_path="/api/song/lyric"
        body={
            "id": id,
            "os": "linux",
            "lv": -1,
            "kv": -1,
            "tv": -1
        }
        params = eapi_encrypt(api_path, body)
        response = requests.post(
            "https://music.163.com/eapi/song/lyric",
            headers=get_headers(),
            data={
                "params": params
            },
            timeout=timeout
        )
        return response.json()
    except:
        return None
    
    #1434354649

def playlist(id, timeout=5):
    try:
        api_path = "/api/v6/playlist/detail"
        body = {
            "s": "0",
            "id": str(id),
            "n": "1000",
            "t": "0"
        }
        params = eapi_encrypt(api_path, body)
        response = requests.post(
            "https://music.163.com/eapi/v6/playlist/detail",
            headers=get_headers(),
            data={"params": params},
            timeout=timeout,
        )
        return response.json()
    except:
        return None