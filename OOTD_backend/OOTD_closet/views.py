from django.http import JsonResponse
from utils.jwt import login_required
from utils.fashion_compatibility_mcn.revision import preprocess, score, generate_outfit
from .models import Clothes, DailyOutfit, ReplaceOutfit
import json
from django.utils import timezone
from .models import Type
import datetime
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
            print("Invalid arguments")
            return JsonResponse({"message": "Invalid arguments"}, status=402)

        new_clothes = form.save(commit=False)
        new_clothes.user = request.user
        new_clothes.clothes_ID = Clothes.clothesid + 1
        Clothes.clothesid += 1
        uploaded_file = request.FILES['file']
        new_clothes.clothes_picture_url = 'clothes/' + \
            f'{new_clothes.clothesid}_clothes.jpg'
        new_clothes.clothes_picture.save(
            new_clothes.clothes_picture_url, uploaded_file)
        new_clothes.save()

        return JsonResponse({"clothesid": new_clothes.clothesid, "message": "Clothes added to the closet successfully"}, status=200)

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
            if len(content['name']) > 32:
                return JsonResponse({"message": "Invalid nickname"}, status=400)
            else:
                clothes.name = content['name']

        if (content.get('Mtype')):
            if content['Mtype'] == '上装':
                clothes.clothes_main_type = Type.UPPER
            elif content['Mtype'] == '下装':
                clothes.clothes_main_type = Type.BOTTOM
            elif content['Mtype'] == '鞋':
                clothes.clothes_main_type = Type.SHOES
            elif content['Mtype'] == '包':
                clothes.clothes_main_type = Type.BAG
            elif content['Mtype'] == '首饰':
                clothes.clothes_main_type = Type.ACCESSORIES
            else:
                return JsonResponse({"message": "Invalid gender"}, status=400)

        if (clothes.get('Dtype')):
            if len(content['Dtype']) > 32:
                return JsonResponse({"message": "Invalid Dtype"}, status=400)
            else:
                clothes.clothes_detail_type = content['Dtype']

        clothes.save()
        clothes.updated = timezone.now()

        return JsonResponse({"clothes_ID": clothes.clothes_ID, "pictureUrl": clothes.clothes_picture_url, "update": clothes.updated, "message": "ok"}, status=200)

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
            # 删除原来的图片
            Clothes.clothes_picture.delete(save=False)
            Clothes.clothes_picture_url = 'avatars/' + \
                f'{Clothes.clothesid}_avatar.jpg'
            Clothes.clothes_picture.save(
                Clothes.clothes_picture_url, uploaded_file)

            return JsonResponse({"avatarUrl": Clothes.clothes_picture_url, "updated": Clothes.updated, "message": "ok"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

# 获取衣服列表


@login_required
def get_clothes(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        clothes = Clothes.objects.filter(user=user)
        clothes_list = []
        for cloth in clothes.iterator():
            clothes_list.append({
                "id": cloth.clothes_ID,
                "name": cloth.clothes_name,
                "Mtype": cloth.clothes_main_type,
                "Dtype": cloth.clothes_detail_type,
                "pictureUrl": cloth.clothes_picture_url
            })
        return JsonResponse({"clothes": clothes_list, "message": "ok"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)


# 添加穿搭
@login_required
def add_outfit(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    user = request.user
    dailyoutfit = None
    try:
        dailyoutfit = DailyOutfit.objects.get(user=user, date_worn=datetime.date.today())
    except DailyOutfit.DoesNotExist:
        dailyoutfit = DailyOutfit.objects.create(user=user)
    content = json.loads(request.body)
    clothes_ID = content.get("id")
    clothes = None
    try:
        clothes = Clothes.objects.get(clothes_ID=clothes_ID)
    except Clothes.DoesNotExist:
        return JsonResponse({"message": "Clothes not found"}, status=400)
    try:
        old_clothes = dailyoutfit.clothes.get(clothes_main_type=clothes.clothes_main_type)
        dailyoutfit.clothes.remove(old_clothes)
    except Clothes.DoesNotExist:
        pass
    dailyoutfit.clothes.add(clothes)
    dailyoutfit.save()
    response = []
    for clothit in dailyoutfit.clothes.iterator():
        response.append({
            "id": clothit.clothes_ID,
            "name": clothit.clothes_name,
            "Mtype": clothit.clothes_main_type,
            "Dtype": clothit.clothes_detail_type,
            "pictureUrl": clothit.clothes_picture_url})
    return JsonResponse({"clothes": response, "message": "ok"}, status=200)


# 删除穿搭
@login_required
def remove_outfit(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    user = request.user
    dailyoutfit = None
    try:
        dailyoutfit = DailyOutfit.objects.get(user=user, date_worn=datetime.date.today())
    except DailyOutfit.DoesNotExist:
        return JsonResponse({"message": "Outfit not found"}, status=400)
    content = json.loads(request.body)
    clothes_ID = content.get("id")
    clothes = None
    try:
        clothes = dailyoutfit.clothes.get(clothes_ID=clothes_ID)
    except Clothes.DoesNotExist:
        return JsonResponse({"message": "Clothes not found"}, status=400)
    dailyoutfit.clothes.remove(clothes)
    dailyoutfit.save()
    response = []
    for clothit in dailyoutfit.clothes.iterator():
        response.append({
            "id": clothit.clothes_ID,
            "name": clothit.clothes_name,
            "Mtype": clothit.clothes_main_type,
            "Dtype": clothit.clothes_detail_type,
            "pictureUrl": clothit.clothes_picture_url})
    return JsonResponse({"clothes":response,"message": "ok"}, status=200)

# 获取穿搭
@login_required
def get_outfit(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    user = request.user
    try:
        dailyoutfit = DailyOutfit.objects.get(user=user, date_worn=datetime.date.today())
    except DailyOutfit.DoesNotExist:
        return JsonResponse({"clothes": '', "message": "Outfit not found"}, status=201)
    clothes = dailyoutfit.clothes.all()
    clothes_list = []
    for cloth in clothes:
        clothes_list.append({
            "id": cloth.clothes_ID,
            "name": cloth.clothes_name,
            "Mtype": cloth.clothes_main_type,
            "Dtype": cloth.clothes_detail_type,
            "pictureUrl": cloth.clothes_picture_url
        })
    return JsonResponse({"clothes": clothes_list, "message": "ok"}, status=200)

# 穿搭评分
@login_required
def score(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        dailyoutfit = DailyOutfit.objects.get(
            user=user, date_worn=datetime.date.today())
        if dailyoutfit is None:
            return JsonResponse({"message": "Outfit not found"}, status=400)
        paths = path = {'upper': [], 'bottom': [],
                        'shoes': [], 'bag': [], 'accessory': []}
        for clothit in dailyoutfit.clothes.iterator():
            path[clothit.clothes_main_type].append(clothit.clothes_picture_url)
        all_list = []
        all_path = {'upper': [], 'bottom': [],
                    'shoes': [], 'bag': [], 'accessory': []}
        clothes = Clothes.objects.filter(user=user)
        for clothit in clothes.iterator():
            # 根据天气筛选衣服种类

            all_list.append(clothit)
            all_path[clothit.clothes_main_type].append(
                clothit.clothes_picture_url)
        model = preprocess()
        rate, replace, best_score, best_img_path, img_idx = score(
            path, model, all_path)
        response = []
        replace_outfit = ReplaceOutfit.objects.get(user=user)
        if replace:
            replace_outfit.clothes.clear()
            replace_outfit.rate = rate
            for i in img_idx:
                replace_outfit.clothes.add(all_list[i])
                response.append({
                    "id": all_list[i].clothes_ID,
                    "name": all_list[i].clothes_name,
                    "Mtype": all_list[i].clothes_main_type,
                    "Dtype": all_list[i].clothes_detail_type,
                    "pictureUrl": all_list[i].clothes_picture_url})
            replace_outfit.save()
        return JsonResponse({"rate": rate, "have_better": replace, "best_score": best_score, "replace": response, "message": "ok"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

# 替换成推荐穿搭
@login_required
def replace(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        replace_outfit = ReplaceOutfit.objects.get(user=user)
        if replace_outfit is None or replace_outfit.clothes is None:
            return JsonResponse({"message": "Outfit not found"}, status=400)
        dailyoutfit = DailyOutfit.objects.get(
            user=user, date_worn=datetime.date.today())
        dailyoutfit.clothes.clear()
        dailyoutfit.rate = replace_outfit.rate
        response = []
        for clothit in replace_outfit.clothes.iterator():
            dailyoutfit.clothes.add(clothit)
            response.append({
                "id": clothit.clothes_ID,
                "name": clothit.clothes_name,
                "Mtype": clothit.clothes_main_type,
                "Dtype": clothit.clothes_detail_type,
                "pictureUrl": clothit.clothes_picture_url})
        dailyoutfit.save()
        return JsonResponse({"rate": replace_outfit.rate, "clothes": response, "message": "ok"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

# 生成推荐穿搭


@login_required
def generate(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        dailyoutfit = DailyOutfit.objects.get(
            user=user, date_worn=datetime.date.today())
        if dailyoutfit is None:
            dailyoutfit = DailyOutfit.objects.create(user=user)
        clothes = Clothes.objects.filter(user=user)
        path = {'upper': [], 'bottom': [],
                'shoes': [], 'bag': [], 'accessory': []}
        clist = []
        for clothit in clothes.iterator():
            # 根据天气筛选衣服种类

            path[clothit.clothes_main_type].append(clothit.clothes_picture_url)
            clist.append(clothit)
        model = preprocess()
        best_score, best_img_path, img_idx = generate_outfit(path, model)
        response = []
        dailyoutfit.clothes.clear()
        for i in img_idx:
            dailyoutfit.clothes.add(clist[i])
            response.append({
                "id": clist[i].clothes_ID,
                "name": clist[i].clothes_name,
                "Mtype": clist[i].clothes_main_type,
                "Dtype": clist[i].clothes_detail_type,
                "pictureUrl": clist[i].clothes_picture_url})
        dailyoutfit.save()
        return JsonResponse({"rate": best_score, "clothes": response, "message": "ok"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)
