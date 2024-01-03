import json
import os
import unittest
from django.test import Client,TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.files import File

import login.views as login_views
from OOTD_closet import views as OOTD_closet_views
from OOTD_closet.models import *
from utils import jwt
from login.models import *

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

        # 上衣1
        #with open("D:\\SoftwareEngineering\\OOTD\\OOTD_backend\\media\\images\\clothes\\上衣1.jpg", "rb") as image_file:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/images/clothes/上衣1.jpg")), "rb") as image_file:
            django_file = File(image_file)
            self.upper1 = Clothes.objects.create(
                user=self.user,
                clothes_name="上衣1",
                clothes_main_type=Type.UPPER,
                clothes_detail_type="T恤",
                clothes_picture_url=f'avatars/{"上衣1"}.jpg'
            )
            self.upper1.clothes_picture.save(self.upper1.clothes_picture_url, django_file)
            self.upper1.save()
            
        
        # # 上衣2
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/images/clothes/上衣2.jpg")), "rb") as image_file:
            django_file = File(image_file)
            self.upper2 = Clothes.objects.create(
                user=self.user,
                clothes_name="上衣2",
                clothes_main_type=Type.UPPER,
                clothes_detail_type="T恤",
                clothes_picture_url=f'avatars/{"上衣2"}.jpg'
            )
            self.upper2.clothes_picture.save(self.upper2.clothes_picture_url, django_file)
            self.upper2.save()

        # # 裤子
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/images/clothes/裤子1.jpg")), "rb") as image_file:
            django_file = File(image_file)
            self.bottom = Clothes.objects.create(
                user=self.user,
                clothes_name="裤子1",
                clothes_main_type=Type.BOTTOM,
                clothes_detail_type="牛仔裤",
                clothes_picture_url=f'avatars/{"上衣1"}.jpg'
            )
            self.bottom.clothes_picture.save(self.bottom.clothes_picture_url, django_file)
            self.bottom.save()

        # # 鞋子
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/images/clothes/鞋.jpg")), "rb") as image_file:
            django_file = File(image_file)
            self.shoes = Clothes.objects.create(
                user=self.user,
                clothes_name="鞋",
                clothes_main_type=Type.SHOES,
                clothes_detail_type="帆布鞋",
                clothes_picture_url=f'avatars/{"鞋"}.jpg'
            )
            self.shoes.clothes_picture.save(self.shoes.clothes_picture_url, django_file)
            self.shoes.save()


        # # 帽子
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/images/clothes/帽子.jpg")), "rb") as image_file:
            django_file = File(image_file)
            self.cap = Clothes.objects.create(
                user=self.user,
                clothes_name="帽子",
                clothes_main_type=Type.ACCESSORIES,
                clothes_detail_type="帽子",
                clothes_picture_url=f'avatars/{"帽子"}.jpg'
            )
            self.cap.clothes_picture.save(self.cap.clothes_picture_url, django_file)
            self.cap.save()

        self.client = Client()

    # 测试编辑衣服
    def test_edit_clothes(self): 
        # 数据正确
        data = {
            'clothes_name': '蓝色卫衣',
            'clothes_main_type': '上衣',
            'clothes_detail_type': 'T恤'
        }

        form = OOTD_closet_views.ClothesForm(data=data)
        self.assertTrue(form.is_valid())

        url = reverse(OOTD_closet_views.edit_clothes, kwargs={'clothes_id': self.upper1.pk})
        
        
        response = self.client.post(
            path=url,
            headers={'Authorization': jwt.generate_jwt({"openid": self.user.openid})},
            data=form.data,
            content_type="application/x-www-form-urlencoded"
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Clothes edited successfully")
 
    # 测试获取衣服列表信息
    def test_get_clothes(self):
        response = self.client.get(
            reverse(OOTD_closet_views.get_clothes), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")


    # 测试搭配相关的全部功能
    def test_outfit(self):
        # add_outfit
        # 添加上衣1
        data = {
            'id':self.upper2.pk
        }
        response = self.client.post(
            reverse(OOTD_closet_views.add_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

        # 添加裤子
        data = {
            'id':self.bottom.pk
        }
        response = self.client.post(
            reverse(OOTD_closet_views.add_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

        # 添加鞋子
        data = {
            'id':self.shoes.pk
        }
        response = self.client.post(
            reverse(OOTD_closet_views.add_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")
        # print(response.json())

        # 添加帽子
        data = {
            'id':self.cap.pk
        }
        response = self.client.post(
            reverse(OOTD_closet_views.add_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

        # 数据错误:
        data = {
            'id':-2
        }
        response = self.client.post(
            reverse(OOTD_closet_views.add_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Clothes not found")

        # remove_outfit
        data = {
            'id':self.cap.pk
        }
        response = self.client.post(
            reverse(OOTD_closet_views.remove_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

        data = {
            'id':-1
        }
        response = self.client.post(
            reverse(OOTD_closet_views.remove_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], "Clothes not found")

        # get_outfit
        response = self.client.get(
            reverse(OOTD_closet_views.get_outfit), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

    ######################################
        # 获取天气
        response = self.client.get(
            reverse(login_views.get_weather), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

        # score
        response = self.client.post(
            reverse(OOTD_closet_views.score), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

"""
    
    ##############################
    def test_score(self):
        data = {
            'id':'',
            'score':''
        }
        response = self.client.post(
            reverse(OOTD_closet_views.score), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

        # 数据错误:outfit not found
        # 数据错误:score not found

    ##############################
    def test_generate(self):
        response = self.client.get(
            reverse(OOTD_closet_views.generate), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")
    
    ##############################
    def test_replace(self):
        data = {
            'id':''
        }
        response = self.client.post(
            reverse(OOTD_closet_views.replace), 
            headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
            data=data,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "ok")

        # 数据错误:outfit not found
        # 数据错误:clothes not found
"""
    ##############################
    # def get_score(self):
    #     response = self.client.get(
    #         reverse(OOTD_closet_views.get_score), 
    #         headers={'Authorization':  jwt.generate_jwt({"openid": self.user.openid})},
    #         content_type="application/json"
    #         )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['message'], "ok")


if __name__ == "__main__":
    unittest.main()