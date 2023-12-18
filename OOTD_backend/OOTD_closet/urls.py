from . import views
from django.urls import path

urlpatterns = [
    path('add_clothes',views.add_clothes,name='add_clothes'),
    path('edit_clothes', views.edit_clothes, name='edit_clothes'),
    path('add_outfit', views.add_outfit, name='add_outfit'),
    path('remove_outfit', views.remove_outfit, name='remove_outfit'),
    path('get_outift', views.get_outift, name='get_outift'),
    path('score', views.score, name='score'),
    path('generate', views.generate, name='generate'),
    path('replace', views.replace, name='replace'),
]
