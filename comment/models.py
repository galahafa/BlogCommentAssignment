from django.db import models


class Post(models.Model):
    text = models.CharField(max_length=1024)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
