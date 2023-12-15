from . import views
from django.urls import path

urlpatterns = [
    path('api/closet/',views.add_clothes,name='add_clothes'),
    path('api/closet/', views.edit_clothes, name='edit_clothes'),
]
