from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
class LikeForm(forms.Form):
    is_liked = forms.BooleanField(required=False)

class FavoriteForm(forms.Form):
    is_favorite = forms.BooleanField(required=False)