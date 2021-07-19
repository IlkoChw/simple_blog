from django.views.generic import ListView
from django.http import HttpResponseRedirect, Http404
from .models import Post, UserProfile, UserPostViewing


class FeedView(ListView):
    model = Post
    template_name = "main_app/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = Post.objects.filter(
            author__in=UserProfile.objects.get(user=self.request.user).subscriptions.all())

        for post in posts:
            UserPostViewing.objects.get_or_create(
                user=self.request.user,
                post=post
            )

        user_post_viewings = UserPostViewing.objects.filter(user=self.request.user)

        context['posts'] = zip(posts, user_post_viewings)

        return context


def post_viewed(request, post_pk):
    try:
        post = Post.objects.get(post__pk=post_pk)
        user_post_viewings = UserPostViewing.objects.get(user=request.user, post=post)
        user_post_viewings.post_viewed()
        return HttpResponseRedirect('/feed/')
    except UserPostViewing.DoesNotExist:
        raise Http404("UserPostViewing does not exist")
