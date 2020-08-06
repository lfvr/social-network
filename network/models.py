from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name="followers")

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    likers = models.ManyToManyField('User', related_name = "liked_posts")

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Created on {self.created} by {self.user}: {self.message}"