from django.http import JsonResponse
from utils.jwt import login_required
from utils.fashion_compatibility_mcn.revision import preprocess, evaluate, generate_outfit
from .models import Clothes, DailyOutfit, ReplaceOutfit,clothing_suggestions
import json
from django.utils import timezone
from .models import Type
import datetime
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed
#import logging

#logger = logging.getLogger(__name__)

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
        # print(form)
        if not form.is_valid():
            print("Invalid arguments")
            return JsonResponse({"message": "Invalid arguments"}, status=402)
        
        new_clothes = form.save(commit=False)
        new_clothes.user = request.user
        # new_clothes.clothes_ID = Clothes.clothesid + 1
        # Clothes.clothesid += 1
        uploaded_file = request.FILES['file']
        new_clothes.save()
        new_clothes.clothes_picture_url = 'clothes/' + \
            f'{new_clothes.pk}_clothes.jpg'
        print(new_clothes.pk)
        new_clothes.clothes_picture.save(
            new_clothes.clothes_picture_url, uploaded_file)
        new_clothes.save()
        return JsonResponse({"clothesid": new_clothes.pk, "message": "Clothes added to the closet successfully"}, status=200)

    elif request.method == "GET":
        form = ClothesForm()
        return JsonResponse({"message": "empty"}, status=200)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

@login_required
def delete_clothes(request):
    """
    删除衣服
    """
    if request.method == "POST":
        content = json.loads(request.body)
        clothes_ID = content.get("id")
        # print(clothes_ID)
        Clothes.objects.get(pk=clothes_ID).delete()
        return JsonResponse({"message": "Clothes deleted successfully"}, status=200)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

@login_required
def edit_clothes(request,clothes_id):
    """
    编辑衣服
    """
    if request.method == "POST":
        form = ClothesForm(request.POST)
        # print(form.modified_data)
        if not form.is_valid():
            print("Invalid arguments")
            return JsonResponse({"message": "Invalid arguments"}, status=402)
        
        clothes = get_object_or_404(Clothes, pk=clothes_id)
        clothes.clothes_name = form.cleaned_data['clothes_name']
        clothes.clothes_main_type = form.cleaned_data['clothes_main_type']
        clothes.clothes_detail_type = form.cleaned_data['clothes_detail_type']
        uploaded_file = request.FILES['file'] 
        clothes.clothes_picture.delete(save=False)
        clothes.clothes_picture_url = 'clothes/' + f'{clothes.clothesid}_clothes.jpg'
        clothes.clothes_picture.save(clothes.clothes_picture_url, uploaded_file)
        clothes.save()
        return JsonResponse({"message": "Clothes edited successfully"}, status=200)
    
    elif request.method == "GET":
        form = ClothesForm()
        return JsonResponse({"message": "empty"}, status=200)
    
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

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
                "id": cloth.pk,
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
    #print(request.body)  # 打印请求体内容
    content = json.loads(request.body)
    # print(content)
    clothes_ID = content.get("id")
    clothes = None
    
    # print(clothes_ID)
    try:
        clothes = Clothes.objects.get(pk=clothes_ID)
    except Clothes.DoesNotExist:
        return JsonResponse({"message": "Clothes not found"}, status=400)
    
    try: 
        old_clothes = dailyoutfit.clothes.get(clothes_main_type=clothes.clothes_main_type)
        dailyoutfit.clothes.remove(old_clothes)
    except Clothes.DoesNotExist:
        pass
    
    dailyoutfit.clothes.add(clothes)
    dailyoutfit.rate = 0
    dailyoutfit.save()
    response = []
    
    for clothit in dailyoutfit.clothes.iterator():
        response.append({
            "id": clothit.pk,
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
        clothes = dailyoutfit.clothes.get(pk=clothes_ID)
    except Clothes.DoesNotExist:
        return JsonResponse({"message": "Clothes not found"}, status=400)
    dailyoutfit.clothes.remove(clothes)
    dailyoutfit.rate = 0
    dailyoutfit.save()
    response = []
    for clothit in dailyoutfit.clothes.iterator():
        response.append({
            "id": clothit.pk,
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
            "id": cloth.pk,
            "name": cloth.clothes_name,
            "Mtype": cloth.clothes_main_type,
            "Dtype": cloth.clothes_detail_type,
            "pictureUrl": cloth.clothes_picture_url
        })
    return JsonResponse({"clothes": clothes_list,"rate":dailyoutfit.rate ,"message": "ok"}, status=200)

# 穿搭评分
@login_required
def score(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    user = request.user
    try:
        dailyoutfit = DailyOutfit.objects.get(user=user, date_worn=datetime.date.today())
    except DailyOutfit.DoesNotExist:
        return JsonResponse({"message": "Outfit not found"}, status=400)
    path = {'upper': 'upper_mean', 'bottom': 'bottom_mean',
                    'shoes': 'shoes_mean', 'bag': 'bag_mean', 'accessory': 'accessory_mean'}
    for clothit in dailyoutfit.clothes.iterator():
        path[clothit.get_clothes_main_type_display()]=clothit.clothes_picture_url
    path_values = list(path.values())
    all_list = {'upper': [], 'bottom': [],
                'shoes': [], 'bag': [], 'accessory': []}
    all_path = {'upper': [], 'bottom': [],
                'shoes': [], 'bag': [], 'accessory': []}
    try:
        clothes = Clothes.objects.filter(user=user)
    except Clothes.DoesNotExist:
        return JsonResponse({"message": "Clothes not found"}, status=400)
    temp = int(user.weather.temperature)
    for clothit in clothes.iterator():
        # 根据天气筛选衣服种类
        sug = clothing_suggestions[clothit.get_clothes_main_type_display()][clothit.clothes_detail_type]
        if sug is None or sug[0] <= temp <= sug[1]:
            all_list[clothit.get_clothes_main_type_display()].append(clothit)
            all_path[clothit.get_clothes_main_type_display()].append(clothit.clothes_picture_url)
    model = preprocess()
    rate, replace, best_score, best_img_path, img_idx = evaluate(path_values, model, all_path)
    dailyoutfit.rate = int(rate*100)
    dailyoutfit.save()
    response = []
    try:
        replace_outfit = ReplaceOutfit.objects.get(user=user)
    except ReplaceOutfit.DoesNotExist:
        replace_outfit = ReplaceOutfit.objects.create(user=user)
    if replace:
        if replace_outfit.clothes is not None:
            replace_outfit.clothes.clear()
        else:
            replace_outfit.clothes = Clothes.objects.none()
        replace_outfit.rate = int(best_score*100)
        print(img_idx)
        # 遍历字典img_idx，把all_list中对应的衣服加入到replace_outfit中
        for key, value in img_idx.items():
            replace_outfit.clothes.add(all_list[key][value])
            response.append({
                "id": all_list[key][value].pk,
                "name":all_list[key][value].clothes_name,
                "Mtype": all_list[key][value].clothes_main_type,
                "Dtype": all_list[key][value].clothes_detail_type,
                "pictureUrl": all_list[key][value].clothes_picture_url})
        replace_outfit.save()
    return JsonResponse({"rate":  dailyoutfit.rate, "have_better": replace, "best_score": replace_outfit.rate, "replace": response, "message": "ok"}, status=200)


# 替换成推荐穿搭
@login_required
def replace(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    user = request.user
    try:
        replace_outfit = ReplaceOutfit.objects.get(user=user)
        dailyoutfit = DailyOutfit.objects.get(user=user, date_worn=datetime.date.today())
    except ReplaceOutfit.DoesNotExist or DailyOutfit.DoesNotExist:
        return JsonResponse({"message": "Outfit not found"}, status=400)
    dailyoutfit.clothes.clear()
    dailyoutfit.rate = replace_outfit.rate
    response = []
    for clothit in replace_outfit.clothes.iterator():
        dailyoutfit.clothes.add(clothit)
        response.append({
            "id": clothit.pk,
            "name": clothit.clothes_name,
            "Mtype": clothit.clothes_main_type,
            "Dtype": clothit.clothes_detail_type,
            "pictureUrl": clothit.clothes_picture_url})
    dailyoutfit.save()
    return JsonResponse({"rate": replace_outfit.rate, "clothes": response, "message": "ok"}, status=200)


# 生成推荐穿搭


@login_required
def generate(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    user = request.user
    try:
        dailyoutfit = DailyOutfit.objects.get(user=user, date_worn=datetime.date.today())
    except DailyOutfit.DoesNotExist:
        dailyoutfit = DailyOutfit.objects.create(user=user)
    try:
        clothes = Clothes.objects.filter(user=user)
    except Clothes.DoesNotExist:
        return JsonResponse({"message": "Clothes not found"}, status=400)
    path = {'upper': [], 'bottom': [],
            'shoes': [], 'bag': [], 'accessory': []}
    clist = {'upper': [], 'bottom': [],
            'shoes': [], 'bag': [], 'accessory': []}
    temp = int(user.weather.temperature)
    for clothit in clothes.iterator():
        # 根据天气筛选衣服种类
        sug = clothing_suggestions[clothit.get_clothes_main_type_display()][clothit.clothes_detail_type]
        if sug is None or sug[0] <= temp <= sug[1]:
            path[clothit.get_clothes_main_type_display()].append(clothit.clothes_picture_url)
            clist[clothit.get_clothes_main_type_display()].append(clothit)
    model = preprocess()
    best_score, best_img_path, img_idx = generate_outfit(path, model)
    response = []
    dailyoutfit.clothes.clear()
    dailyoutfit.rate = int(best_score*100)
    for key, value in img_idx.items():
        dailyoutfit.clothes.add(clist[key][value])
        response.append({
            "id": clist[key][value].pk,
            "name": clist[key][value].clothes_name,
            "Mtype": clist[key][value].clothes_main_type,
            "Dtype": clist[key][value].clothes_detail_type,
            "pictureUrl": clist[key][value].clothes_picture_url})
    dailyoutfit.save()
    return JsonResponse({"rate": dailyoutfit.rate, "clothes": response, "message": "ok"}, status=200)


# 统计穿搭评分
@login_required
def get_score(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    user = request.user
    index = request.GET.get("index")

    if index is None:
        return JsonResponse({"message": "Invalid arguments"}, status=402)

    try:
        index = int(index)
        if index == 0:
            days = 7
        elif index == 1:
            days = 14
        elif index == 2:
            days = 30
        else:
            return JsonResponse({"message": "Invalid arguments"}, status=402)

        # 获取最近days天的穿搭评分
        # print(days)
        dailyoutfit = DailyOutfit.objects.filter(user=user, date_worn__gte=datetime.date.today() - datetime.timedelta(days)) 
        score_list = []
        date_list = []
        
        for outfit in dailyoutfit.iterator():
            score_list.append(outfit.rate)
            date_list.append(outfit.date_worn.strftime("%m-%d"))
            
        # print(len(score_list))
        return JsonResponse({"ratings": score_list, "dates": date_list, "message": "ok"}, status=200)
    except ValueError:
        return JsonResponse({"message": "Invalid arguments"}, status=402)
    except DailyOutfit.DoesNotExist:
        return JsonResponse({"message": "Outfit not found"}, status=404)