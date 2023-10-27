from . import views
from django.urls import path

urlpatterns = [
    path('api/v1/login/',views.login,name='login'),
    path('api/v1/logon/',views.logon,name='logon'),
    path('api/v1/logout/', views.logout, name='logout'),
]
