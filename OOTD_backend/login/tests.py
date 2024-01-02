import json
import unittest
from django.test import Client,TestCase
from django.urls import reverse
from django.utils import timezone


# import sys
# import os
# sys.path.append('.')

from login import views as login_views
from login.models import *
from login import controllers
from utils import jwt

class APITestCase(TestCase):
    def setUp(self):
        now = timezone.now()
        self.user = User.objects.create(
            openid="test_openid",
            nickname= "test_nickname",
            age=18,
            addr="北京",
            gender=Gender.FEMALE,
            avatarUrl='',
            avatar=None,
            phone='18811511917',
            intro="test_intro",
            updated=now,
            weather=None)
        self.user.save()

        self.client = Client()

    # 测试修改用户信息
    def test_edit_info(self):
        
        # 数据正确
        data = {
            "nickname": "test_nickname111",
            "age": 19,
            "addr":"天津",
            "gender":"女",
            "avatarUrl":'',
            "phone":'18811511919', 
            "intro":"test_intro111"
        }
        response = self.client.patch(
            reverse(login_views.edit_info), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")
        # print(response.json())
        

        # 数据错误：性别填写格式有误
        data = {
            "nickname": "test_nickname111",
            "age": 12,
            "addr":"天津",
            "gender":Gender.FEMALE,
            "avatarUrl":'',
            "phone":'18811511919', 
            "intro":"test_intro111"
        }
        response = self.client.patch(
            reverse(login_views.edit_info), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid gender")

        # 数据错误：年龄为负数
        data = {
            "nickname": "test_nickname111",
            "age": -1,
            "addr":"天津",
            "gender":"女",
            "avatarUrl":'',
            "phone":'18811511919', 
            "intro":"test_intro111"
        }
        response = self.client.patch(
            reverse(login_views.edit_info), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid age")

        # 数据错误：电话号码长度有误
        data = {
            "nickname": "test_nickname111",
            "age": 12,
            "addr":"天津",
            "gender":"女",
            "avatarUrl":'',
            "phone":'188115119119', 
            "intro":"test_intro111"
        }
        response = self.client.patch(
            reverse(login_views.edit_info), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid phone")

    # 测试获取用户信息
    def test_user(self):
        response = self.client.get(
            reverse(login_views.user), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")
        # print(response.json())

    # 测试获取天气
    def test_get_weather(self):
        response = self.client.get(
            reverse(login_views.get_weather), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")
        # print(response.json())
    

if __name__ == "__main__":
    unittest.main()