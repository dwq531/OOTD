from django.db import models

# Create your models here.
class Clothes(models.Model):
    """
    衣服
    """
    clothes_name = models.CharField(max_lenghth=32,default='',verbose_name="衣服名字")
    clothes_main_type = models.CharField(max_lenghth=32,default='',verbose_name="衣服主要类型")
    coat_type = models.CharField(max_lenghth=32,default='',verbose_name="外套类型")
    dress_type = models.CharField(max_lenghth=32,default='',verbose_name="裙子类型")
    upper_type = models.CharField(max_lenghth=32,default='',verbose_name="上衣类型")
    pants_type = models.CharField(max_lenghth=32,default='',verbose_name="裤装类型")
    skirt_type = models.CharField(max_lenghth=32,default='',verbose_name="半身裙类型")
    shoes_type = models.CharField(max_lenghth=32,default='',verbose_name="鞋子类型")
    bag_type = models.CharField(max_lenghth=32,default='',verbose_name="包包类型")
    accessories_type = models.CharField(max_lenghth=32,default='',verbose_name="配饰类型")
