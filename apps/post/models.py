# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..account.models import AccountBasic


class Post(models.Model):
    # comments
    nlikes = models.IntegerField(default=0)
    ndislikes = models.IntegerField(default=0)
    content = models.CharField(max_length=50000)
    id_post = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='statics/images')
    date_post = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.account.name + '->' + self.content
