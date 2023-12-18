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
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
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

# 每类衣服的推荐温度范围
clothing_suggestions = {
    "upper": {
        "T恤": (20, 30),
        "衬衫": (15, 25),
        "卫衣": (-10, 25),
        "毛衣": (-10, 20),
        "吊带": (25, 40),
        "POLO衫": (20, 30),
        "连衣裙": (15, 35),
        "风衣": (10, 25),
        "马甲": (15, 25),
        "夹克": (10, 25),
        "皮衣": (10, 25),
        "冲锋衣": (5, 15),
        "防晒衣": (25, 40),
        "羽绒服": (-30, 10),
        "正装外套": None,
        "其他": None
    },
    "bottom": {
        "牛仔裤": (15, 30),
        "裙裤": (15, 35),
        "运动裤": None,
        "背带裤": (15, 25),
        "休闲裤": None,
        "棉裤": (-30, 10),
        "正装裤": None,
        "半身裙": (15, 40),
        "其他": None
    },
    "shoes": {
        "运动鞋": None,
        "凉鞋": (25, 40),
        "板鞋": (10, 35),
        "帆布鞋": (10, 35),
        "靴子": (-30, 10),
        "其他": None
    },
    "bag": {
        "手提包": None,
        "腰包": None,
        "挎包": None,
        "背包": None
    },
    "accessories": {
        "项链": None,
        "帽子": None,
        "围巾": None,
        "耳环": None,
        "头饰": None
    }
}