from django.db import models
from django.core.files.base import ContentFile
import requests
class Gender(models.TextChoices):
    MALE = 'M', '男'
    FEMALE = 'F', '女'

class Weather(models.Model):
    icon = models.CharField(max_length=255, default='', verbose_name="天气图标")
    text = models.CharField(max_length=255, default='', verbose_name="天气描述")
    temperature = models.CharField(max_length=10, default='', verbose_name="温度")

# Create your models here.
class User(models.Model):
    """
    用户
    """
    openid=models.CharField(max_length=32,default='',verbose_name="标识id")
    nickname=models.CharField(max_length=32,default="anonymous",verbose_name="用户昵称")
    age=models.IntegerField(default=18,verbose_name="年龄")
    addr=models.CharField(max_length=127,default='北京',verbose_name="所处地")
    gender=models.CharField(max_length=1,choices=Gender.choices,default=Gender.FEMALE,verbose_name="性别")
    avatarUrl=models.CharField(max_length=255,default='/',verbose_name="头像url")   # 在服务器上的 url
    avatar=models.ImageField(upload_to='images/')   # 指定头像储存的目录
    phone=models.CharField(max_length=15,default='none',verbose_name="手机号码")
    intro=models.TextField(max_length=255,default='none',verbose_name="个人简介")
    updated=models.DateTimeField(auto_now=True, verbose_name="更新时间")
    weather = models.ForeignKey(Weather, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="天气")
    
    def save_image_from_url(self):
        response = requests.get(self.avatarUrl)
        if response.status_code == 200:
            self.avatarUrl = 'avatars/' + f'{self.openid}_avatar.jpg'
            self.avatar.save(self.avatarUrl, ContentFile(response.content))
        else:
            # TODO 将 None 替换为默认头像
            self.avatarUrl = None
            self.avatar = None