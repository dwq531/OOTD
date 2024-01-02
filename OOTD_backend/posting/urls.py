from django.urls import path
from .views import create_post, post_detail, user_posts, upload_image,like_post,favorite_post,comment_post,user_post_info

urlpatterns = [
    # 贴文创建
    path("create_post/", create_post, name="create_post"),
    # 贴文详情
    path("post_detail/id=<int:post_id>/", post_detail, name="post_detail"),
    # 用户贴文列表
    path("user_posts/<str:post_type>/", user_posts, name="user_posts"),
    # 图片上传
    path("upload_image/<int:post_id>/", upload_image, name="upload_image"),
    # 点赞
    path("like_post/<int:post_id>/", like_post, name="like_post"),
    # 收藏
    path("favorite_post/<int:post_id>/", favorite_post, name="favorite_post"),
    # 评论
    path("comment_post/<int:post_id>/", comment_post, name="comment_post"),
    # 统计信息
    path("user_post_info",user_post_info,name="user_post_info")
]
