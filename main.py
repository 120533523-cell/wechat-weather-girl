import requests
import os
from datetime import datetime

def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": os.getenv("APP_ID"),
        "secret": os.getenv("APP_SECRET")
    }
    res = requests.get(url, params=params).json()
    return res.get("access_token")

def get_weather():
    url = "https://devapi.qweather.com/v7/weather/now"
    params = {
        "location": os.getenv("CITY"),
        "key": os.getenv("WEATHER_KEY")
    }
    res = requests.get(url, params=params).json()
    if res["code"] != "200":
        return None
    now = res["now"]
    temp = now["temp"]
    text = now["text"]
    tip = ""
    t = int(temp)
    if t < 0:
        tip = "今天超冷，多穿衣服别冻着～"
    elif t < 10:
        tip = "有点冷，注意保暖哦"
    elif t < 20:
        tip = "温度舒服，穿外套刚刚好"
    elif t < 28:
        tip = "天气暖暖的，很舒服～"
    else:
        tip = "有点热，注意防晒多喝水"

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "city": "你所在的城市",
        "weather": text,
        "temp": temp,
        "tip": tip
    }

def send(access_token, data):
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    body = {
        "touser": os.getenv("OPENID"),
        "template_id": os.getenv("TEMPLATE_ID"),
        "data": {
            "date": {"value": data["date"]},
            "city": {"value": data["city"]},
            "weather": {"value": data["weather"]},
            "temp": {"value": data["temp"]},
            "tip": {"value": data["tip"]}
        }
    }
    r = requests.post(url, json=body)
    print(r.json())

if __name__ == "__main__":
    token = get_access_token()
    weather = get_weather()
    if token and weather:
        send(token, weather)
