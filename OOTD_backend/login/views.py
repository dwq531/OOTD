from django.http import HttpResponse, JsonResponse
from utils.jwt import encrypt_password, generate_jwt, login_required
import json
from login import controllers
from django.utils import timezone
from login.models import Gender
import re
import gzip
import requests


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

'''
openid 感觉没必要返回给用户，jwt 已经完成了
'''
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

@login_required
def get_weather(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    try:
        user = request.user
        api_key="67d28b46a25041b4a6515de071592609"
        api_location_url=f"https://geoapi.qweather.com/v2/city/lookup?location={user.addr}&key={api_key}"
        response = requests.get(api_location_url)
        data = {}

        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'gzip' in content_type:
                compressed_data = response.content
                decompressed_data = gzip.decompress(compressed_data)
                data = json.loads(decompressed_data.decode('utf-8'))

            else:
                data = response.json()
                #print("here")
            #print(data)

            locationid = data["location"][0]["id"]
            api_weather_url = f"https://devapi.qweather.com/v7/weather/now?location={locationid}&key={api_key}"
            response = requests.get(api_weather_url)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'gzip' in content_type:
                    compressed_data = response.content
                    decompressed_data = gzip.decompress(compressed_data)
                    data = json.loads(decompressed_data.decode('utf-8'))
                else:
                    data = response.json()

                user.weather.icon = data["now"]["icon"]
                user.weather.text = data["now"]["text"]
                user.weather.temperature = data["now"]["temp"]
                #print(user.weather.text)
            else:
                return "Failed to fetch weather data"
            
        else:
            return "Failed to fetch location data"

        return JsonResponse({
            'icon':user.weather.icon,
            'text':user.weather.text,
            'temperature':user.weather.temperature
        }, status=200)
    except Exception as e:
        print(f"发生异常：{str(e)}")
        return JsonResponse({"message": "Internal Server Error"}, status=500)





# 感觉好像没用，先注释了
#
# def index(request):
#     return HttpResponse('主页面')
