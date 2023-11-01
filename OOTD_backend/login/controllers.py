from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import User
import json
import http.client


def get_user(openid):
    try:
        u = User.objects.get(openid=openid)
        return u, True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False


def create_user(openid, nickname="匿名用户", age=18, addr='', gender='F', avatarUrl='', phone='', intro="该用户未填写个人简介"):
    try:
        now = timezone.now()
        u = User.objects.create(
            openid=openid,
            nickname=nickname,
            age=age,
            addr=addr,
            gender=gender,
            avatarUrl=avatarUrl,
            phone=phone,
            intro=intro,
            updated=now
        )
        u.save()
        return u,True
    except Exception as e:
        print(e)
        return "errors",False

# 给微信API发送code2session请求
def get_openid(code):

    conn = http.client.HTTPSConnection(
        "https://api.weixin.qq.com")
    headers = {'Content-type': 'application/json'}
    data = {"appid": "wxe695d8ed64cfbc63", "appSecret": "6a4d7088e79a482b8efaf77bedc14625",
            "js_code": code, "grant_type": "authorization_code"}
    payload = json.dumps(data)
    conn.request("GET", "/sns/jscode2session", payload, headers)
    response = conn.getresponse()
    json_res = response.json()
    conn.close()
    if(json_res.get('openid')):
        return json_res
    else:
        return False
    
 
