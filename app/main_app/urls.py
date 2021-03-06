from django.urls import path
from .views import FeedView, post_viewed, BlogView, subscription_view, PostDetailView, redirect_to_feed, UserListView


urlpatterns = [
    path('', redirect_to_feed, name='redirect_to_feed'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('users/', UserListView.as_view(), name='users'),
    path('blog/<str:user_name>', BlogView.as_view(), name='blog'),
    path('post/<pk>', PostDetailView.as_view(), name='post_detail'),
    path('viewed/<post_pk>', post_viewed, name='post_viewed'),
    path('subscription/<user_pk>', subscription_view, name='subscription'),
]
