from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def login(request):
    """
    微信登录，检查是否在用户列表里，没有则添加
    """
    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    return HttpResponse('登录成功')



def logout(request):
    return HttpResponse('退出')

def index(request):
    return HttpResponse('主页面')
