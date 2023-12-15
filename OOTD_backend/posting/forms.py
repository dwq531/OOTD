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


class LikeForm(forms.Form):
    is_liked = forms.BooleanField(required=False)


class FavoriteForm(forms.Form):
    is_favorite = forms.BooleanField(required=False)
