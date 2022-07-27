from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=25,null=False)
    def __str__(self):
        return self.title

class Feed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name="likes")
    comments = models.ManyToManyField('Comment', related_name="comments")
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.body[0:500]

class Like(models.Model):
    state = models.BooleanField(null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=500,null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:500]

    