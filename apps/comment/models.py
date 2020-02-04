# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..account.models import AccountBasic
from ..post.models import Post


class RowComment(models.Model):
    xid = models.CharField(primary_key=True, default='', max_length=1000)
    account = models.ForeignKey(AccountBasic, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000, default="")


class SubComment(models.Model):
    main = models.ForeignKey(
        RowComment, on_delete=models.CASCADE, related_name="main_comment")
    replies = models.ManyToManyField(RowComment)
    cid = models.IntegerField(primary_key=True, default=0)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, primary_key=True, default=None)
    comments = models.ManyToManyField(SubComment, related_name="commentss")
