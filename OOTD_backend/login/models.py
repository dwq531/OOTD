from django.db import models

# Create your models here.
class User(models.Model):
    """
    用户
    """
    openid=models.CharField(max_length=32,default='',verbose_name="标识id")
    nickname=models.CharField(max_length=32,default="anonymous",verbose_name="用户昵称")
    age=models.IntegerField(default=18,verbose_name="年龄")
    addr=models.CharField(max_length=127,default='none',verbose_name="所处地")
    gender=models.CharField(max_length=1,choices=(
        ('M', 'Male'),
        ('F', 'Female')),default='F',verbose_name="性别")
    avatarUrl=models.CharField(max_length=255,default='/',verbose_name="头像url")
    phone=models.CharField(max_length=15,default='none',verbose_name="手机号码")
    intro=models.TextField(max_length=255,default='none',verbose_name="个人简介")
    updated=models.DateTimeField(auto_now=True, verbose_name="更新时间")