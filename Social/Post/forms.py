from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Write a comment...',
        'rows': 1,
        'class': 'comment-input'
    }))

    class Meta:
        model = Comment
        fields = ['text']