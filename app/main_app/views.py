from django.views.generic import ListView
from .models import Post, UserProfile


class FeedView(ListView):
    model = Post
    template_name = "main_app/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(
            author__in=UserProfile.objects.get(user=self.request.user).subscriptions.all())

        return context
