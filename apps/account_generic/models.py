# -*- coding: utf-8 -*-

from django.db import models
from ..account.models import Account
from ..post.models import Post


class AccountGeneric(models.Model):
    account = models.ForeignKey(
        Account, primary_key=True, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)
    followers = models.ManyToManyField(Account)
    followings = models.ManyToManyField(Account)
