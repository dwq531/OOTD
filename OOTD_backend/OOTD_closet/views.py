from django.http import JsonResponse
from utils.jwt import login_required
from .models import Clothes
import json
from django.utils import timezone
from .models import Type
from django import forms
from django.shortcuts import get_object_or_404

class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['clothes_name', 'clothes_main_type', 'clothes_detail_type']

@login_required
def add_clothes(request):
    """
    添加衣服
    """
    if request.method == "POST":
        form = ClothesForm(request.POST)
        if not form.is_valid():
            # print("Invalid arguments")
            return JsonResponse({"message": "Invalid arguments"}, status=400)
        
        new_clothes = form.save(commit=False)
        new_clothes.user = request.user
        new_clothes.clothesid = Clothes.clothesid + 1
        Clothes.clothesid += 1
        new_clothes.save()
        
        return JsonResponse({"clothesid":new_clothes.clothesid, "message": "Clothes added to the closet successfully"}, status=201)
    
    elif request.method == "GET":
        form = ClothesForm()
        return JsonResponse({"message": "empty"}, status=200)
    
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

"""
@login_required
def add_clothes(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        # print(request.body)
        content = json.loads(request.body)
        
        clothes_ID = Clothes.clothesid + 1
        Clothes.clothesid += 1
        clothes_name = content.get("name")
        clothes_main_type = content.get("Mtype")
        clothes_detail_type = content.get("Dtype")
        # clothes_picture_url = content.get("pictureUrl")

        new_clothes = Clothes(
            clothes_ID = clothes_ID,
            clothes_name = clothes_name,
            clothes_main_type = clothes_main_type,
            clothes_detail_type = clothes_detail_type,
            # clothes_picture_url = clothes_picture_url,
        )
        # new_clothes.save_image_from_url()
        uploaded_file = request.FILES['file'] 
        user = request.user
        new_clothes.user = user
        # print(Clothes.clothes_picture_url)
        new_clothes.clothes_picture_url = 'clothes/' + f'{new_clothes.clothesid}_clothes.jpg'
        new_clothes.clothes_picture.save(new_clothes.clothes_picture_url, uploaded_file)
        new_clothes.save()
        new_clothes.updated = timezone.now()

        return JsonResponse({"message": "Clothes added to the closet successfully"}, status=201)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)
"""

@login_required
def edit_clothes(request):
    """
    修改衣服信息
    """
    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)
        
    try:
        content = json.loads(request.body)
        clothes_id = content.get('clothes_ID', None)
        clothes_id = int(clothes_id)
        # 在数据库中查找相应的 Clothes 对象
        clothes = Clothes.objects.get(clothes_ID=clothes_id)
        if (content.get('pictureUrl')):
            clothes.clothes_picture_url = content['pictureUrl']
            clothes.save_image_from_url()
            if clothes.clothes_picture is None:
                return JsonResponse({"message": "Invalid avatarUrl"}, status=400)
        
        if (clothes.get('name')):
            if len(content['name'])>32:
                return JsonResponse({"message": "Invalid nickname"}, status=400)
            else:
                clothes.name = content['name']

        if (content.get('Mtype')):
            if content['Mtype']=='上装':
                clothes.clothes_main_type = Type.UPPER
            elif content['Mtype']=='下装':
                clothes.clothes_main_type = Type.BOTTOM
            elif content['Mtype']=='鞋':
                clothes.clothes_main_type = Type.SHOES
            elif content['Mtype']=='包':
                clothes.clothes_main_type = Type.BAG
            elif content['Mtype']=='首饰':
                clothes.clothes_main_type = Type.ACCESSORIES
            else:
                return JsonResponse({"message": "Invalid gender"}, status=400)
        
        if (clothes.get('Dtype')):
            if len(content['Dtype'])>32:
                return JsonResponse({"message": "Invalid Dtype"}, status=400)
            else:
                clothes.clothes_detail_type = content['Dtype']

        clothes.save()
        clothes.updated = timezone.now()
        
        return JsonResponse({"clothes_ID":clothes.clothes_ID, "pictureUrl":clothes.clothes_picture_url, "update":clothes.updated, "message": "ok"}, status=200)
        
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

@login_required
def upload_file(request):
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES['file'] 
            Clothes = request.user
            print(Clothes.clothes_picture_url)
            #删除原来的图片
            Clothes.clothes_picture.delete(save=False)
            Clothes.clothes_picture_url = 'avatars/' + f'{Clothes.clothesid}_avatar.jpg'
            Clothes.clothes_picture.save(Clothes.clothes_picture_url, uploaded_file)

            return JsonResponse({"avatarUrl":Clothes.clothes_picture_url, "updated": Clothes.updated,"message": "ok"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)