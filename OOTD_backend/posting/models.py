from django.db import models
from login.models import User


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, default="分享穿搭")
    content = models.TextField(blank=True, default="")
    images = models.ManyToManyField("Image", blank=True)
    rate = models.FloatField(default=0, blank=True)
    weather = models.CharField(max_length=200, blank=True, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    favorites = models.ManyToManyField(User, related_name="favorite_posts", blank=True)
    show_rate = models.BooleanField(default=False)
    show_weather = models.BooleanField(default=False)


class Image(models.Model):
    image = models.ImageField(upload_to="post_images/")
    description = models.CharField(max_length=255, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
