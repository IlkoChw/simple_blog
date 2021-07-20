from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from .models import Post, UserProfile, UserPostViewing
from django.contrib.auth.models import User


class FeedView(ListView):
    model = Post
    template_name = "main_app/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = Post.objects.filter(
            author__in=UserProfile.objects.get(user=self.request.user).subscriptions.all()).order_by('-created')

        for post in posts:
            UserPostViewing.objects.get_or_create(
                user=self.request.user,
                post=post
            )

        user_post_viewings = UserPostViewing.objects.filter(user=self.request.user)

        context['posts'] = zip(posts, user_post_viewings)

        return context


class PostCreateView(CreateView):
    template_name = 'main_app/create_post.html'
    model = Post
    success_url = reverse_lazy('feed')
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogView(ListView):
    model = Post
    template_name = "main_app/blog.html"

    def get_queryset(self):
        return User.objects.get(username=self.kwargs['user_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_queryset()

        context['author'] = author
        context['subscriptions'] = UserProfile.objects.get(pk=self.request.user.pk).subscriptions.all()
        context['posts'] = Post.objects.filter(author=author)

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'main_app/post_detail.html'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['pk'])


def post_viewed(request, post_pk):
    try:
        post = Post.objects.get(post__pk=post_pk)
        user_post_viewings = UserPostViewing.objects.get(user=request.user, post=post)
        user_post_viewings.post_viewed()
        return HttpResponseRedirect(reverse_lazy('feed'))
    except UserPostViewing.DoesNotExist:
        raise Http404("UserPostViewing does not exist")


def subscription_view(request, user_pk):
    try:
        author = User.objects.get(pk=user_pk)
        current_user_profile = UserProfile.objects.get(user=request.user)
        if author in current_user_profile.subscriptions.all():
            current_user_profile.subscriptions.remove(author)
        else:
            current_user_profile.subscriptions.add(author)

        return HttpResponseRedirect(reverse_lazy('blog', kwargs={'user_name': author.username}))
    except UserPostViewing.DoesNotExist:
        raise Http404("Subscription does not exist")


def redirect_to_feed(request):
    return HttpResponseRedirect(reverse_lazy('feed'))
