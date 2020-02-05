from django.db import models
from ..account.models import AccountBasic
from ..post.models import Post

class Follows(models.Model):
    saccount = models.ForeignKey(
        AccountBasic, primery_key=True, on_delete=models.CASCADE)
    taccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=False, default='follows')

class Comments(models.Model):
    saccount = models.ForeignKey(
        AccountBasic, primery_key=True, on_delete=models.CASCADE)
    taccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)    
    type = models.CharField(max_length=20, null=False, default='follows')


class Notification(models.Model):
    account = models.ForeignKey(
        AccountBasic, primary_key=True, on_delete=models.CASCADE)
    follows = models.ManyToManyField(Follows, related_name='follows')   
    comments = models.ManyToManyField(Comments, related_name='comments') 