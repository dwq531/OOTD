from . import views
from django.urls import path

urlpatterns = [
    path('add_clothes',views.add_clothes,name='add_clothes'),
    path('edit_clothes/<int:clothes_id>', views.edit_clothes, name='edit_clothes'),
    path('delete_clothes', views.delete_clothes, name='delete_clothes'),
    path('get_clothes', views.get_clothes, name='get_clothes'),
    path('add_outfit', views.add_outfit, name='add_outfit'),
    path('remove_outfit', views.remove_outfit, name='remove_outfit'),
    path('get_outfit', views.get_outfit, name='get_outfit'),
    path('score', views.score, name='score'),
    path('generate', views.generate, name='generate'),
    path('replace', views.replace, name='replace'),
    path('get_score', views.get_score, name='get_score'),
    path('get_favorite_clothes', views.get_favorite_clothes, name='get_favorite_clothes'),
    path('get_clothes_count', views.get_clothes_count, name='get_clothes_count'),
]
