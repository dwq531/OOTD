from django.db import models
from django.core.files.base import ContentFile
import requests
from  login.models  import User

# Create your models here.

class Type(models.TextChoices):
    UPPER = 'upper','上装'
    BOTTOM = 'bottom','下装'
    SHOES = 'shoes','鞋'
    BAG = 'bag','包'
    ACCESSORIES = 'accessories','首饰'

class Clothes(models.Model):
    """
    衣服
    """
    clothesid = 0
    clothes_ID = models.IntegerField(default=0,verbose_name="衣服id")
    clothes_name = models.CharField(max_length=32,default='',verbose_name="衣服名字")
    clothes_main_type = models.CharField(max_length=32,choices=Type.choices,default=Type.UPPER,verbose_name="衣服主要类型")
    clothes_detail_type = models.CharField(max_length=32,default='',verbose_name="衣服细分类型")
    clothes_picture_url=models.CharField(max_length=255,default='/',verbose_name="衣服图片url")   # 在服务器上的 url
    clothes_picture = models.ImageField(upload_to='images/')   # 指定衣服储存的目录
    clothes_used_time = models.IntegerField(default=0,verbose_name="衣服使用次数")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_clothes = models.ManyToManyField(User,related_name='user_clothes',blank=True)
    
    def save_image_from_url(self):
        response = requests.get(self.clothes_picture_url)
        if response.status_code == 200:
            self.clothes_picture_url = 'clothes/' + f'{self.clothesid}_clothes.jpg'
            self.clothes_picture.save(self.clothes_picture_url, ContentFile(response.content))
        else:
            # TODO 将 None 替换为默认
            self.clothes_picture_url = None
            self.clothes_picture = None

class DailyOutfit(models.Model):
    """
    每日搭配
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dailyoutfit',verbose_name="用户")
    clothes = models.ManyToManyField(Clothes,related_name='dailyoutfit',verbose_name="搭配的衣服")
    date_worn = models.DateField(auto_now_add=True,verbose_name="日期")
    rate = models.IntegerField(default=0,verbose_name="评分")
    

class ReplaceOutfit(models.Model):
    """
    评分后推荐替换成的搭配
    只存储最新的一套
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='replaceoutfit',verbose_name="用户")
    clothes = models.ForeignKey(Clothes,verbose_name="待替换的衣服")
    rate = models.IntegerField(default=0,verbose_name="评分")