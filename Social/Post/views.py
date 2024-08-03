from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm, CommentForm
from django.views import View
from .models import Post, Like

class PostLikeToggle(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        like_qs = Like.objects.filter(post=post, user=request.user)
        
        if like_qs.exists():
            like_qs.delete()
        else:
            Like.objects.create(post=post, user=request.user)
        
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
@login_required
def post_list(request):
    posts = Post.objects.all()
    form = CommentForm()
    return render(request, 'main/home.html', {'posts': posts, 'form': form})

@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect('post:post_list')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('main:home')
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', {'form': form})
