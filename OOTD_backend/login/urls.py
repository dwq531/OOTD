from . import views
from django.urls import path
from django.conf.urls.static import static # 添加本行
from django.conf import settings 
urlpatterns = [
    path('api/user/login',views.login,name='login'),
    path('api/user/logout', views.logout, name='logout'),
    path('api/user/edit_info', views.edit_info, name='edit_info'),
    path('api/user/user', views.user, name='user'),
    path('api/user/avatar', views.upload_file, name='upload_file'),
    path('/api/user/weather',views.get_weather,name='get_weather'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
