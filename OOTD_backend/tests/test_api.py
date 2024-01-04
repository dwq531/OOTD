import json
import unittest

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone



import sys
import os
sys.path.append('..')

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
            "gender":Gender.FEMALE,
            "avatarUrl":'',
            "phone":'18811511919', 
            "intro":"test_intro111"
        }
        response = self.client.patch(
            reverse(login_views.edit_info), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data
            )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['message'], 'Internal Server Error')
        print(response.json())
        

        # 数据错误：年龄为负数
        # data = {
        #     "nickname": "test_nickname111",
        #     "age": -1,
        #     "addr":"天津",
        #     "gender":Gender.FEMALE,
        #     "avatarUrl":'',
        #     "phone":'18811511919', 
        #     "intro":"test_intro111"
        # }
        # response = self.client.patch(
        #     reverse(login_views.edit_info), 
        #     headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
        #     data=data
        #     )
        # self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json()['message'], 'Invalid age')


if __name__ == "__main__":
    unittest.main()