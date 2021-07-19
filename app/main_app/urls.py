from django.urls import path
from .views import FeedView, post_viewed, PostCreateView


urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
    path('viewed/<post_pk>', post_viewed, name='post_viewed'),
    path('post/create/', PostCreateView.as_view(), name='create_post'),
]
