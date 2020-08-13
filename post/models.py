from django.db import models
from django.contrib.auth.models import User

# *Only available for PostgreSQL database
from django.contrib.postgres.fields import ArrayField


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class SubReddit(models.Model):
    name = models.CharField(max_length=256)
    moderators = models.ManyToManyField(User, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    subreddit_following = models.ManyToManyField(SubReddit, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    A = "ACCEPTED"
    P = "PENDING"
    R = "REJECTED"
    status_choices = [
        (A, "ACCEPTED"),
        (P, "PENDING"),
        (R, "REJECTED"),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=256)
    subreddit = models.ForeignKey(
        SubReddit, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField(max_length=5120, blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=status_choices, default=P)

    # TODO: We will add file and image fields after wards

    def __str__(self):
        return self.header


class Link(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="links")
    url = models.URLField(max_length=2048)

    def __str__(self):
        return f'[{self.url}] on post "{self.post.header}"'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=256)

    def __str__(self):
        return f'[{self.text}] by {self.user.username} on ({self.post.header}) at  <{self.timestamp}>'
