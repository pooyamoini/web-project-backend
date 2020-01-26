# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=50, null=False)