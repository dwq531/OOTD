from django.http import HttpResponse, JsonResponse
from utils.jwt import encrypt_password, generate_jwt, login_required
import json
from login import controllers
from django.utils import timezone
from login.models import Gender
import re


def login(request):
    """
    微信登录，检查是否在用户列表里，没有则添加
    """
    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        content = json.loads(request.body)
        code = content.get("code")
        data = controllers.get_openid(code)
        if data:
            openid = data['openid']
            user, isOld = controllers.get_user(openid)
            if not isOld:  # 新用户，不在用户列表里
                user,cflag = controllers.create_user(openid)
                #user.save_image_from_url()
            jwt = generate_jwt({"openid": openid})
            return JsonResponse({
                'jwt': jwt,
                'new': not isOld,
                'nickname': user.nickname,
                'age': user.age,
                'addr': user.addr,
                'gender': Gender(user.gender).label,
                'phone': user.phone,
                'intro': user.intro,
                'avatarUrl': user.avatarUrl,
                'updated': user.updated,
                'message': 'ok'
            }, status = 200)
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)
    except:
        return JsonResponse({"message": "bad arguments"}, status=400)


@login_required
def logout(request):
    return JsonResponse({"message": "ok"}, status=200)


@login_required
def user(request):
    """
    获取用户信息
    """
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    try:
        user = request.user
        
        return JsonResponse({
            'nickname': user.nickname,
            'age': user.age,
            'addr': user.addr,
            'gender': Gender(user.gender).label,
            'phone': user.phone,
            'intro': user.intro,
            'avatarUrl': user.avatarUrl,
            'updated': user.updated,
            'message': 'ok'
        }, status=200)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


@login_required
def edit_info(request):
    """
    修改用户信息
    """
    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)
        
    try:
        user = request.user
        content = json.loads(request.body)        
        if (content.get('avatarUrl')):
            user.avatarUrl = content['avatarUrl']
            user.save_image_from_url()
            if user.avatar is None:
                return JsonResponse({"message": "Invalid avatarUrl"}, status=400)
        
        if (content.get('nickname')):
            if len(content['nickname'])>32:
                return JsonResponse({"message": "Invalid nickname"}, status=400)
            else:
                user.nickname = content['nickname']
        if (content.get('gender')):
            if content['gender']=='女':
                user.gender = Gender.FEMALE
            elif content['gender']=='男':
                user.gender = Gender.MALE
            else:
                return JsonResponse({"message": "Invalid gender"}, status=400)
        if (content.get('phone')):
            pattern = r'^\d{10}$'  # 例如：123-456-7890
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

'''
openid 感觉没必要返回给用户，jwt 已经完成了
'''



# 感觉好像没用，先注释了
#
# def index(request):
#     return HttpResponse('主页面')
