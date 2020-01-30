# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Comment(models.Model):
    post_id = models.Int


    def __str__(self):
        return self.id