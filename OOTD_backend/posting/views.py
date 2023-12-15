from django.shortcuts import get_object_or_404, redirect
from utils.jwt import login_required
from django.http import JsonResponse
from .models import Post
from .forms import PostForm, ImageForm, CommentForm, LikeForm, FavoriteForm
from .serializers import PostSerializer, CommentSerializer


@login_required
def create_post(request):
    """
    创建一个贴文。可以用 POST 或 GET 请求。
    POST: 提交一个贴文表单。
    GET: 获取空贴文表单。
    """
    if request.method == "POST":  # 用户提交表单
        form = PostForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        post = form.save(commit=False)
        post.user = request.user
        post.save()

        return JsonResponse({"id": post.pk}, status=201)  # 返回新创建的帖子的ID

    elif request.method == "GET":  # 用户获取空表单
        form = PostForm()
        serializer = PostSerializer(form.instance)
        return JsonResponse({"form": serializer.data}, status=200)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def upload_image(request, post_id):
    """
    上传图片到贴文。只能用 POST 请求。
    """
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"message": "Invalid credentials"}, status=401)

        post = get_object_or_404(Post, pk=post_id)
        post.images.create(image=request.FILES["image"])
        return JsonResponse({"message": "Image uploaded successfully"}, status=200)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def post_detail(request, post_id):
    """
    贴文详情页。可以用 POST 或 GET 请求。
    GET: 返回此贴文的详细信息。
    POST: 用户进行评论、点赞、收藏操作。
    """
    # 获取贴文详情
    post = get_object_or_404(Post, pk=post_id)

    comment_form = CommentForm(request.POST or None)
    like_form = LikeForm(request.POST or None)
    favorite_form = FavoriteForm(request.POST or None)

    comment_serializer = None
    post_serializer = None

    if request.method == "POST":
        # 评论操作
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            comment_serializer = CommentSerializer(comment_form)

    # 点赞操作
    is_liked = None
    if like_form.is_valid():
        is_liked = like_form.cleaned_data.get("is_liked")
        if is_liked:
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)

    # 收藏操作
    is_favorite = None
    if favorite_form.is_valid():
        is_favorite = favorite_form.cleaned_data.get("is_favorite")
        if is_favorite:
            post.favorites.add(request.user)
        else:
            post.favorites.remove(request.user)

    return JsonResponse(
        {
            "post": post_serializer.data if post_serializer is not None else {},
            "comment_form": comment_serializer.data
            if comment_serializer is not None
            else {},
            "liked_form": is_liked,
            "favorite_form": is_favorite,
        },
        status=200,
    )


@login_required
def user_posts(request, post_type):
    """
    获取贴文列表。
    post_type 在 urls.py 中设置。
    """
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    user = request.user

    # 通过不同的 post_type 获取贴文列表
    if post_type == "created":
        posts = Post.objects.filter(user=user)
    elif post_type == "favorites":
        posts = user.favorite_posts.all()
    elif post_type == "all":
        posts = Post.objects.all()
    else:
        posts = []

    serializer = PostSerializer(posts, many=True)

    return JsonResponse({"posts": serializer.data, "post_type": post_type}, status=200)
