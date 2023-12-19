from django.http import JsonResponse
from utils.jwt import login_required
from utils.fashion_compatibility_mcn.revision import preprocess,score,generate_outfit
from .models import Clothes, DailyOutfit,ReplaceOutfit
import json
from django.utils import timezone
from .models import Type
import datetime
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed

class AddClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['clothes_name', 'clothes_main_type', 'clothes_detail_type']
        
class DeleteClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['clothes_ID']
        
class EditClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['clothes_ID','clothes_name', 'clothes_main_type', 'clothes_detail_type']

@login_required
def add_clothes(request):
    """
    添加衣服
    """
    if request.method == "POST":
        form = AddClothesForm(request.POST)
        if not form.is_valid():
            print("Invalid arguments")
            return JsonResponse({"message": "Invalid arguments"}, status=402)
        
        new_clothes = form.save(commit=False)
        new_clothes.user = request.user
        new_clothes.clothes_ID = Clothes.clothesid + 1
        Clothes.clothesid += 1
        uploaded_file = request.FILES['file'] 
        new_clothes.clothes_picture_url = 'clothes/' + f'{new_clothes.clothesid}_clothes.jpg'
        new_clothes.clothes_picture.save(new_clothes.clothes_picture_url, uploaded_file)
        new_clothes.save()
        
        return JsonResponse({"clothesid":new_clothes.clothesid, "message": "Clothes added to the closet successfully"}, status=200)
    
    elif request.method == "GET":
        form = AddClothesForm()
        return JsonResponse({"message": "empty"}, status=200)
    
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

@login_required
def delete_clothes(request):
    """
    删除衣服
    """
    if request.method == "POST":
        form = DeleteClothesForm(request.POST)
        if not form.is_valid():
            print("Invalid arguments")
            return JsonResponse({"message": "Invalid arguments"}, status=402)
        
        clothes = get_object_or_404(Clothes, id=form.cleaned_data['clothes_ID'])
        clothes.delete()    
        return JsonResponse({"message": "Clothes deleted successfully"}, status=200)
    
    elif request.method == "GET":
        form = DeleteClothesForm()
        return JsonResponse({"message": "empty"}, status=200)
    
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

@login_required
def edit_clothes(request, clothes_ID):
    """
    编辑衣服
    """
    if request.method == "POST":
        form = EditClothesForm(request.POST)
        if not form.is_valid():
            print("Invalid arguments")
            return JsonResponse({"message": "Invalid arguments"}, status=402)
        
        clothes = get_object_or_404(Clothes, id=form.cleaned_data['clothes_ID'])
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
        form = EditClothesForm()
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
                "id": cloth.clothes_ID,
                "name": cloth.clothes_name,
                "Mtype": cloth.clothes_main_type,
                "Dtype": cloth.clothes_detail_type,
                "pictureUrl": cloth.clothes_picture_url
            })
        return JsonResponse({"clothes": clothes_list,"message": "ok"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)


# 添加穿搭
@login_required
def add_outfit(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        dailyoutfit = None
        if DailyOutfit.objects.get(user=user,date_worn=datetime.date.today()).exists():
            dailyoutfit = DailyOutfit.objects.get(user=user,date_worn=datetime.date.today())
        else:
            dailyoutfit = DailyOutfit.objects.create(user=user)
        content = json.loads(request.body)
        clothes_ID = content.get("id")
        clothes = Clothes.objects.get(clothes_ID=clothes_ID)
        if clothes is None:
            return JsonResponse({"message": "Clothes not found"}, status=400)
        dailyoutfit.clothes.add(clothes)
        dailyoutfit.save()
        return JsonResponse({"message": "Clothes added to the outfit successfully"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

# 删除穿搭
@login_required
def remove_outfit(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        dailyoutfit = DailyOutfit.objects.get(user=user,date_worn=datetime.date.today())
        content = json.loads(request.body)
        clothes_ID = content.get("id")
        clothes = dailyoutfit.clothes.get(clothes_ID=clothes_ID)
        if clothes is None:
            return JsonResponse({"message": "Clothes not found"}, status=400)
        dailyoutfit.clothes.remove(clothes)
        dailyoutfit.save()
        return JsonResponse({"message": "Clothes removed from the outfit successfully"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

# 获取穿搭
@login_required
def get_outift(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        dailyoutfit = DailyOutfit.objects.get(user=user,date_worn=datetime.date.today())
        if dailyoutfit is None:
            return JsonResponse({"clothes":'',"message": "Outfit not found"}, status=201)
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
        return JsonResponse({"clothes": clothes_list,"message": "ok"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

# 穿搭评分
@login_required
def score(request):
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        user = request.user
        dailyoutfit = DailyOutfit.objects.get(user=user,date_worn=datetime.date.today())
        if dailyoutfit is None:
            return JsonResponse({"message": "Outfit not found"}, status=400)
        paths = path = {'upper':[],'bottom':[],'shoes':[],'bag':[],'accessory':[]}
        for clothit in dailyoutfit.clothes.iterator():
           path[clothit.clothes_main_type].append(clothit.clothes_picture_url)
        all_list = []
        all_path = {'upper':[],'bottom':[],'shoes':[],'bag':[],'accessory':[]}
        clothes = Clothes.objects.filter(user=user)
        for clothit in clothes.iterator():
            # 根据天气筛选衣服种类

            all_list.append(clothit)
            all_path[clothit.clothes_main_type].append(clothit.clothes_picture_url)
        model = preprocess()
        rate, replace, best_score, best_img_path,img_idx = score(path,model,all_path)
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
        return JsonResponse({"rate":rate,"have_better":replace,"best_score":best_score,"replace":response, "message": "ok"}, status=200)

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
        dailyoutfit = DailyOutfit.objects.get(user=user,date_worn=datetime.date.today())
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
        return JsonResponse({"rate":replace_outfit.rate,"clothes":response,"message": "ok"}, status=200)

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
        dailyoutfit = DailyOutfit.objects.get(user=user,date_worn=datetime.date.today())
        if dailyoutfit is None:
            dailyoutfit = DailyOutfit.objects.create(user=user)
        clothes = Clothes.objects.filter(user=user)
        path = {'upper':[],'bottom':[],'shoes':[],'bag':[],'accessory':[]}
        clist = []
        for clothit in clothes.iterator():
            # 根据天气筛选衣服种类

            path[clothit.clothes_main_type].append(clothit.clothes_picture_url)
            clist.append(clothit)
        model = preprocess()
        best_score, best_img_path,img_idx = generate_outfit(path,model)
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
        return JsonResponse({"rate":best_score,"clothes":response,"message":"ok"}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)