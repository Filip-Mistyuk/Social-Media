from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profiles/<int:user_id>/', views.profile, name='profile_with_id'),
    path('profile_update/', views.update_profile, name='update_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('follow/<int:user_id>/', views.send_follow_request, name='send_follow_request'),
    path('manage-follow-requests/', views.manage_follow_requests, name='manage_follow_requests'),
    path('accept-follow-request/<int:follow_request_id>/', views.accept_follow_request, name='accept_follow_request'),
    path('reject-follow-request/<int:request_id>/', views.reject_follow_request, name='reject_follow_request'),
    path('cancel/<int:request_id>/', views.cancel_follow_request, name='cancel_follow_request'),
    path('search/', views.search_users, name='search_users'),
    path('mailbox/', views.mailbox, name='mailbox'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('view_subscriptions/', views.view_subscriptions, name='view_subscriptions'),
    path('view_followers/', views.view_followers, name='view_followers'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
]
