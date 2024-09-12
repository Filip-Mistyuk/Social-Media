from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserSearchForm
from .models import Profile, Follow, FollowRequest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from Post.models import Post


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    follow_request, created = FollowRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user_to_follow
    )
    
    if not created:
        follow_request.delete()
    else:
        follow_request.save()
    
    return redirect('profile:profile_with_id', user_id=user_id)

@login_required
def profile(request, user_id=None):
    if user_id is None:
        user_id = request.user.id
    
    user = get_object_or_404(User, id=user_id)
    is_following = Follow.objects.filter(from_user=request.user, to_user=user).exists()
    followers = Follow.objects.filter(to_user=user)
    following = Follow.objects.filter(from_user=user)
    posts = Post.objects.filter(author=user)
    
    context = {
        'user': user,
        'is_following': is_following,
        'followers': followers,
        'following': following,
        'posts': posts,
    }
    return render(request, 'main/home.html', context)

@login_required
def mailbox(request):
    received_requests = FollowRequest.objects.filter(to_user=request.user)
    sent_requests = FollowRequest.objects.filter(from_user=request.user)
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    return render(request, 'profile/mailbox.html', context)

@login_required
def search_users(request):
    form = UserSearchForm()
    results = []
    if 'query' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, 'search_sys/search_results.html', {'form': form, 'results': results})

@login_required
def send_follow_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    follow_request = FollowRequest.objects.create(
        from_user=request.user,
        to_user=to_user,
    )
    
    return redirect('profile:profile_with_id', user_id=user_id)

@login_required
def manage_follow_requests(request):
    received_requests = FollowRequest.objects.filter(to_user=request.user, status='pending')
    sent_requests = FollowRequest.objects.filter(from_user=request.user)
    return render(request, 'profile/follow_requests.html', {'received_requests': received_requests, 'sent_requests': sent_requests})

@login_required
def accept_follow_request(request, follow_request_id):
    follow_request = get_object_or_404(FollowRequest, id=follow_request_id)

    if request.method == 'POST':
        follow_request.status = 'accepted'
        follow_request.save()
        follow_request.to_user.profile.followers.add(follow_request.from_user.profile)
        follow_request.from_user.profile.following.add(follow_request.to_user.profile)
        follow_request.delete()

        return redirect('profile:profile_with_id', user_id=follow_request.from_user.id)
    
    return redirect('profile:profile_with_id', user_id=follow_request.from_user.id)

@login_required
def reject_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id)
    if follow_request.to_user == request.user:
        follow_request.delete()
    return redirect('profile:mailbox')

@login_required
def cancel_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id)
    if follow_request.from_user == request.user:
        follow_request.delete()
    return redirect('profile:mailbox')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'main/profile_update.html', {'form': form})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            try:
                profile.save()
                messages.success(request, 'Profile created successfully.')
                return redirect('profile:profile')
            except IntegrityError:
                messages.error(request, 'A profile for this user already exists.')
    else:
        form = ProfileForm()

    return render(request, 'main/create_profile.html', {'form': form})

@login_required
def view_subscriptions(request):
    user_profile = request.user.profile
    following = user_profile.following.all()
    
    return render(request, 'profile/view_subscriptions.html', {'following': following})

@login_required
def view_followers(request):
    user_profile = request.user.profile
    followers = user_profile.followers.all()
    
    return render(request, 'profile/view_followers.html', {'followers': followers})

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    request.user.profile.following.remove(user_to_unfollow.profile)
    user_to_unfollow.profile.followers.remove(request.user.profile)
    
    return redirect('profile:view_subscriptions')