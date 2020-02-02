# -*- coding: utf-8 -*-

from django.db import models
from ..account.models import AccountBasic
from ..post.models import Post


class AccountGeneric(models.Model):
    account = models.ForeignKey(
        AccountBasic, primary_key=True, on_delete=models.CASCADE, related_name='accounts')
    posts = models.ManyToManyField(Post, related_name='post')
    followers = models.ManyToManyField(
        AccountBasic, related_name='followrs')  # necessary ?
    followings = models.ManyToManyField(
        AccountBasic, related_name='followings')
    # channel is left
