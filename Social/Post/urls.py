from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:pk>/comments/', views.post_comment, name='post_comment'),
    path('create/', views.create_post, name='create_post'),
    path('post/like/<int:pk>/', views.PostLikeToggle.as_view(), name='post_like_toggle'),
]
