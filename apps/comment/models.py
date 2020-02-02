# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.utils.timezone import now

class Comment(models.Model):
    id = models.BigAutoField(primary_key = True , null = False)
    post_id = models.BigIntegerField(null= False)
    comment = models.CharField(max_length = 300 , null = False , default = "")
    creator_id = models.CharField(max_length = 300 , null = False )
    creation_date = models.DateField(default = now() , editable = False)
    creation_time = models.TimeField(default = now().time() , editable = False)
    edited_time = models.TimeField(null = True)
    edited_date = models.DateField(null = True)
    comment_replied_to_id = models.BigIntegerField(null= True)
    image_name = models.CharField(max_length = 60 , null = True)
    like_counter = models.IntegerField(null = False , default= 0)
    dislike_counter = models.IntegerField(null= False , default= 0)

# from datetime import datetime

# class Comment(models.Model):
#     id = models.BigAutoField(primary_key = True)
#     post_id = models.BigIntegerField(null= False)
#     comment_creator_id = models.CharField(max_length=40, null=False, default="")
#     reply_to_comment_id = models.BigIntegerField(null= True)
#     creation_time = models.TimeField(default = datetime.now())
#     image_name = models.CharField(max_length = 60 , null = True)
#     Comment_body = models.CharField(max_length = 300 , null = False , default = "")
    
# >>>>>>> Stashed changes


#     def __str__(self):
#         return self.id