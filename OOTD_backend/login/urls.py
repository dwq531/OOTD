from . import views
from django.urls import path

urlpatterns = [
    path('api/user/login',views.login,name='login'),
    path('api/user/logout', views.logout, name='logout'),
]
