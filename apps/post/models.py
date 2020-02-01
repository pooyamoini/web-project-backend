# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..account.models import AccountBasic


class Post(models.Model):
    # comments
    nlikes = models.ManyToManyField(AccountBasic, related_name='nlikes')
    ndislikes = models.ManyToManyField(
        AccountBasic, related_name='ndislikes')
    content = models.CharField(max_length=50000)
    id_post = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=100, default="")
    date_post = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.account.name + '->' + self.content
