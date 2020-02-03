# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Number(models.Model):
    name = models.IntegerField(primary_key=True, default=0)
    value = models.IntegerField()
