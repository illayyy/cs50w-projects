from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name="user_followers", symmetrical=False)


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="user_likes", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.creator}: {self.content}"
