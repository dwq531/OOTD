from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "show_rate", "show_weather"]


class ImageForm(forms.Form):
    image = forms.ImageField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
