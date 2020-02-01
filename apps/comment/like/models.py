# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Like(models.Model):
    comment_id = models.BigIntegerField(null= False)
    liker_id = models.CharField(max_length = 50 , null= False)
    is_like = models.BooleanField(null = False,default=  True)

    def __str__(self):
        return self.id