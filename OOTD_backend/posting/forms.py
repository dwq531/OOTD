from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class ImageForm(forms.Form):
    image = forms.ImageField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
