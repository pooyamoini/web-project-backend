from django.db import models

from ..account.models import AccountBasic
from ..post.models import Post

class Channel(models.Model):
    name = models.CharField(primary_key=True, max_length=40)
    bio = models.CharField(max_length=100)
    rules = models.CharField(max_length=300)
    admin = models.ForeignKey(AccountBasic, on_delete=models.CASCADE, related_name='admin')
    members = models.ManyToManyField(AccountBasic, related_name='members')
    followers = models.ManyToManyField(AccountBasic, related_name='followers')
    posts = models.ManyToManyField(Post, related_name='posts')