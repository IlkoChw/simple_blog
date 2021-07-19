from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(User, related_name='subscriptions')


class Post(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    email_task_created = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserPostViewing(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f'viewed post {self.post.pk} - {self.user.pk}'

    def post_viewed(self):
        if not self.viewed:
            self.viewed = True
            self.save()


@receiver(post_save, sender=Post)
def create_email_task(sender, instance, using, **kwargs):
    from .utils import new_post_email_sent
    # if not instance.email_task_created:
    # instance.email_task_created = True
    # instance.save()
    print('ok!')
    new_post_email_sent(instance.pk)
