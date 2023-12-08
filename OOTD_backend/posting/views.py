from django.shortcuts import render, get_object_or_404, redirect
from utils.jwt import login_required
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm, LikeForm, FavoriteForm


'''
创建一个贴文。可以用 POST 或 GET 请求。
POST: 提交一个贴文表单。
GET: 获取空贴文表单。
'''
@login_required
def create_post(request):
    if request.method == 'POST':    # 用户提交表单
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"message": "Invalid credentials"}, status=401)
        
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        for img in request.FILES.getlist('images'):
            post.images.create(image=img)
        return redirect('post_detail', post_id=post.pk)     # 重定向到创建的帖子的详情页面
    
    elif request.method == 'GET':   # 用户获取空表单
        form = PostForm()
        return JsonResponse({'form': form}, status=200)
    
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


'''
贴文详情页。可以用 POST 或 GET 请求。
GET: 返回此贴文的详细信息。
POST: 用户进行评论、点赞、收藏操作。
'''
@login_required
def post_detail(request, post_id):
    # 获取贴文详情
    post = get_object_or_404(Post, pk=post_id)
    
    comment_form = CommentForm()
    like_form = LikeForm(request.POST or None)
    favorite_form = FavoriteForm(request.POST or None)

    if request.method == 'POST':
        # 评论操作
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
        
        # 点赞操作
        if like_form.is_valid():
            is_liked = like_form.cleaned_data.get('is_liked')
            if is_liked:
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)

        # 收藏操作
        if favorite_form.is_valid():
            is_favorite = favorite_form.cleaned_data.get('is_favorite')
            if is_favorite:
                post.favorites.add(request.user)
            else:
                post.favorites.remove(request.user)

    return JsonResponse(
        {'post': post, 'comment_form': comment_form, 
         'liked_form': like_form, 'favorite_form': favorite_form},
        status=200)


'''
获取贴文列表。
post_type 在 urls.py 中设置。
'''
@login_required
def user_posts(request, post_type):
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    user = request.user
    
    # 通过不同的 post_type 获取贴文列表
    if post_type == 'created':
        posts = Post.objects.filter(user=user)
    elif post_type == 'favorites':
        posts = user.favorite_posts.all()
    else:
        posts = []
    
    return JsonResponse({'posts': posts, 'post_type': post_type}, status=200)