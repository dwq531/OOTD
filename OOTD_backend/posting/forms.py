from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "images"]

    images = forms.ImageField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class LikeForm(forms.Form):
    is_liked = forms.BooleanField(required=False)


class FavoriteForm(forms.Form):
    is_favorite = forms.BooleanField(required=False)
