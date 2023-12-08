from django.http import JsonResponse
from utils.jwt import login_required
from .models import Clothes
import json

@login_required
def add_clothes(request):
    """
        添加衣服
    """
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    try:
        content = request.POST
        clothes_ID = Clothes.clothesid + 1
        clothes_name = content.get("name")
        clothes_main_type = content.get("Mtype")
        clothes_detail_type = content.get("Dtype")
        clothes_picture_url = content.get("pictureUrl")

        new_clothes = Clothes(
            clothes_ID = clothes_ID,
            clothes_name = clothes_name,
            clothes_main_type = clothes_main_type,
            clothes_detail_type = clothes_detail_type,
            clothes_picture_url = clothes_picture_url,
        )
        new_clothes.save_image_from_url()
        new_clothes.save()

        return JsonResponse({"message": "Clothes added to the wardrobe successfully"}, status=201)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

@login_required
def edit_clothes(request):
    """
    修改衣服信息
    """
    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)
        
    try:
        clothes = request.clothes
        content = json.loads(request.body)        
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
            if content['gender']=='女':
                clothes.clothes_main_type = Gender.FEMALE
            elif content['gender']=='男':
                clothes_main_type = Gender.MALE
            else:
                return JsonResponse({"message": "Invalid gender"}, status=400)
        if (content.get('phone')):
            pattern = r'^\d{11}$'  # 例如：1234567890
            if re.match(pattern, content['phone']):
                user.phone = content['phone']
            else:
                return JsonResponse({"message": "Invalid phone"}, status=400)
        if (content.get('intro')):
            if len(content['intro'])>255:
                return JsonResponse({"message": "Invalid intro"}, status=400)
            else:
                user.intro = content['intro']
        if (content.get('addr')):
            if len(content['addr'])>127:
                return JsonResponse({"message": "Invalid addr"}, status=400)
            else:
                user.addr = content['addr']
        if (content.get('age')):
            if content['age']<0 or content['age']>100:
                return JsonResponse({"message": "Invalid age"}, status=400)
            else:
                user.age = content['age']
        user.save()
        user.updated = timezone.now()
        
        return JsonResponse({"avatarUrl":user.avatarUrl, "updated": user.updated, "message": "ok"}, status=200)
        
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)

@login_required
def upload_file(request):
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES['file'] 
            user = request.user
            print(user.avatarUrl)
            #删除原来的头像
            user.avatar.delete(save=False)
            user.avatarUrl = 'avatars/' + f'{user.openid}_avatar.jpg'
            user.avatar.save(user.avatarUrl, uploaded_file)
            

            return JsonResponse({"avatarUrl":user.avatarUrl, "updated": user.updated,"message": "ok"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Internal Server Error"}, status=500)