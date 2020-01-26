# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class AccountBasic(models.Model):
    username = models.CharField(max_length=15, null=False, primary_key=True, default="")
    name = models.CharField(max_length=40, null=False, default="")
    email = models.CharField(max_length=50, null=False, default="")
    password = models.CharField(max_length=200, null=False, default="")

    def __str__(self):
        return(self.name)