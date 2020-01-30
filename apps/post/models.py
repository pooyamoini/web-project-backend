# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..account.models import AccountBasic


class Post(models.Model):
    nlikes = models.IntegerField()
    ndislikes = models.IntegerField()
    content = models.CharField(max_length=50000)
    id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='statics/images')
    date_post = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.account.name + '->' + self.content
