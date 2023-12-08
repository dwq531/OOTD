from . import views
from django.urls import path

urlpatterns = [
    path('api/user/add_clothes',views.add_clothes,name='add_clothes'),
    path('api/user/edit_clothes', views.edit_clothes, name='edit_clothes'),
]
