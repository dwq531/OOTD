from . import views
from django.urls import path

urlpatterns = [
    path('api/closet/add_clothes',views.add_clothes,name='add_clothes'),
    path('api/closet/edit_clothes', views.edit_clothes, name='edit_clothes'),
]
