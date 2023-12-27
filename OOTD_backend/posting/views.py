from django.shortcuts import get_object_or_404
from utils.jwt import login_required
from django.http import JsonResponse
from .models import Post
from .forms import PostForm, ImageForm, CommentForm
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
            return JsonResponse({"message": "Invalid form"}, status=400)

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
            return JsonResponse({"message": "Invalid form"}, status=400)

        post = get_object_or_404(Post, pk=post_id)
        post.images.create(image=request.FILES["image"])
        return JsonResponse({"message": "Image uploaded successfully"}, status=200)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required
def post_detail(request, post_id):
    """
    GET: 返回此贴文的详细信息。
    """
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    post = get_object_or_404(Post, pk=post_id)
    post_serializer = PostSerializer(post)

    comments = post.comments.all()
    comments_serializer = CommentSerializer(comments, many=True)

    return JsonResponse(
        {"post": post_serializer.data, "comments": comments_serializer.data}, status=200
    )


@login_required
def comment_post(request, post_id):
    """
    POST: 提交一个评论表单。
    """
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    form = CommentForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"message": "Invalid form"}, status=400)

    post = get_object_or_404(Post, pk=post_id)
    comment = form.save(commit=False)
    comment.user = request.user
    comment.post = post
    comment.save()

    serializer = CommentSerializer(comment)

    return JsonResponse({"comment": serializer.data}, status=200)


@login_required
def like_post(request, post_id):
    """
    POST: 点赞或取消点赞。
    """
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        post.user.likes -= 1
    else:
        post.likes.add(user)
        post.user.likes += 1
    post.user.save()
    return JsonResponse({"message": "Success"}, status=200)


@login_required
def favorite_post(request, post_id):
    """
    POST: 收藏或取消收藏。
    """
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.favorites.all():
        post.favorites.remove(user)
        user.favorite_posts.remove(post)
    else:
        post.favorites.add(user)
        user.favorite_posts.add(post)

    return JsonResponse({"message": "Success"}, status=200)


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
    elif post_type == "favorite":
        posts = user.favorite_posts.all()
    elif post_type == "all":
        posts = Post.objects.all()
    else:
        posts = []

    serializer = PostSerializer(posts, many=True)

    return JsonResponse({"posts": serializer.data, "post_type": post_type}, status=200)


# 获取收藏、发帖、获赞数量
@login_required
def user_post_info(request):
    if request.method != "GET":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    user = request.user
    return JsonResponse(
        {
            "favorites": user.favorite_posts.count(),
            "posts": Post.objects.filter(user=user).count(),
            "likes": user.likes,
        },
        status=200,
    )