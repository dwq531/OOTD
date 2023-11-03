from django.http import HttpResponse, JsonResponse
from utils.jwt import encrypt_password, generate_jwt, login_required
import json
from login import controllers


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
            jwt = generate_jwt({"openid": openid})
            return JsonResponse({
                'jwt': jwt,
                'new': not isOld,
                'nickname': user.nickname,
                'age': user.age,
                'addr': user.addr,
                'gender': user.gender,
                'phone': user.phone,
                'intro': user.intro,
                'avatarUrl': user.avatarUrl,    
                'updated': user.updated,      
                'message': 'ok'
            }
            )
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)
    except:
        return JsonResponse({"message": "bad arguments"}, status=400)



def logout(request):
    return HttpResponse('退出')


def index(request):
    return HttpResponse('主页面')
