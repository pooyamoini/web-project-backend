from django.db import models
from ..account.models import AccountBasic
from ..post.models import Post

class Follows(models.Model):
    saccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, related_name='saccount_follows')
    taccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, related_name='taccount_follows')
    type = models.CharField(max_length=20, null=False, default='follows')

class Comments(models.Model):
    saccount = models.ForeignKey(
        AccountBasic , on_delete=models.CASCADE, related_name='saccount_comments')
    taccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, related_name='taccount_comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_comments')    
    type = models.CharField(max_length=20, null=False, default='follows')

class Like(models.Model):
    saccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, related_name='saccount_like')
    taccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, related_name='taccount_like')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_like') 
    type = models.CharField(max_length=20, null=False, default='like')
    
class Dislike(models.Model):
    saccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, related_name='saccount_dislike')
    taccount = models.ForeignKey(
        AccountBasic, on_delete=models.CASCADE, related_name='taccount_dislike')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_dislike')     
    type = models.CharField(max_length=20, null=False, default='dislike')
    
class Notification(models.Model):
    account = models.ForeignKey(
        AccountBasic, primary_key=True, on_delete=models.CASCADE, related_name='account')
    follows = models.ManyToManyField(Follows, related_name='follows')   
    comments = models.ManyToManyField(Comments, related_name='comments') 
    like = models.ManyToManyField(Comments, related_name='like')
    dislike = models.ManyToManyField(Comments, related_name='dislike') 
 

    