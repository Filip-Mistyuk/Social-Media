from django.shortcuts import render
from Post.models import Post

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/home.html', {'posts': posts})