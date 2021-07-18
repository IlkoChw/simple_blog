from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(User, related_name='subscriptions')
