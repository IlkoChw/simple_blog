from django.urls import path
from .views import FeedView, post_viewed


urlpatterns = [
    path('feed/', FeedView.as_view()),
    path('viewed/<post_pk>', post_viewed, name='post_viewed'),
]
