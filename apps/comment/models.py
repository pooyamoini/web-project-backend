# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.utils.timezone import now
from ..post.models import Post
from ..account.models import AccountBasic


class Subs(models.Model):
    account = models.ForeignKey(AccountBasic, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)


class SubComment(models.Model):
    account = models.ForeignKey(AccountBasic, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    replies = models.ManyToManyField(Subs, related_name='subs', default=None)
    identify = models.CharField(max_length=1000, primary_key=True)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, primary_key=True, on_delete=models.CASCADE, default=Post.objects.all()[0])
    replies = models.ForeignKey(SubComment, on_delete=models.CASCADE)
