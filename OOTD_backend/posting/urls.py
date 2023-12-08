from django.urls import path
from .views import create_post, post_detail, user_posts

urlpatterns = [
    # 贴文创建
    path("create_post/", create_post, name="create_post"),
    # 贴文详情
    path("post_detail/id=<int:post_id>/", post_detail, name="post_detail"),
    # 用户贴文列表
    path("user_posts/<str:post_type>/", user_posts, name="user_posts"),
]
