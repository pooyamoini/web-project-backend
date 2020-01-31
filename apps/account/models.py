# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models


class AccountBasic(models.Model):
    username = models.CharField(
        max_length=15, null=False, primary_key=True, default="")
    name = models.CharField(max_length=40, null=False, default="")
    email = models.CharField(max_length=50, null=False, default="")
    password = models.CharField(max_length=200, null=False, default="")
    profile = models.CharField(max_length=100, default="")
    gender = models.CharField(max_length=20, default="")
    bio = models.CharField(max_length=500, default="")
    phone_number = models.BigIntegerField(default=0)
    country = models.CharField(max_length=20, default="")

    def __str__(self):
        return(self.name)


class LoggInBasic(models.Model):
    account = models.ForeignKey(
        AccountBasic, primary_key=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=110)
    token_gen_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.name
