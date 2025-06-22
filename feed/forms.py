from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': "What's on your mind?"}),
        }
        labels = {
            'description': ''
        } 