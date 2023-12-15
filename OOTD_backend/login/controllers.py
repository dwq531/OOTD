from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import User,Gender
import json
import requests
import os
from configparser import ConfigParser

def get_user(openid):
    try:
        u = User.objects.get(openid=openid)
        return u, True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False


def create_user(openid, nickname="匿名用户", age=18, addr="北京", gender=Gender.FEMALE, avatarUrl='', phone='', intro="该用户未填写个人简介"):
    try:
        now = timezone.now()
        u = User.objects.create(
            openid=openid,
            nickname=nickname,
            age=age,
            addr=addr,
            gender=gender,
            avatarUrl=avatarUrl,
            avatar=None,
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
    try:
        # 获取配置文件的路径
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config/settings.ini')
        # 以 utf-8 编码打开文件
        with open(config_path, 'r', encoding='utf-8') as file:
            config_text = file.read()

        # 创建 ConfigParser 并加载配置
        config = ConfigParser()
        config.read_string(config_text)
        # 获取值
        appid = config.get('WECHAT', 'APPID')
        secret = config.get('WECHAT', 'SECRET')
        
        response = requests.get("https://api.weixin.qq.com/sns/jscode2session?appid=" + appid + "&secret=" +  secret + "&js_code="
                                +code+
                                "&grant_type=authorization_code")
        dic_res = json.loads(response.text)
        print(dic_res)
        if(dic_res.get('openid')):
            return dic_res
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")

        
 
