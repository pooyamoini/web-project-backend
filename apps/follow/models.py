# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class  AccountFollowType(models.Model):
    id = models.BigAutoField(primary_key=True)
    follower_id = models.CharField(max_length = 15 , null= False )
    followed_id = models.CharField(max_length = 15 , null= False )

    def __str__(selt):
        return(self.id)
