from django.contrib import admin
from .models import Clothes, DailyOutfit, ReplaceOutfit
# Register your models here.
admin.site.register(Clothes)
admin.site.register(DailyOutfit)
admin.site.register(ReplaceOutfit)