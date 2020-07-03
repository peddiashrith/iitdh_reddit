from django.db import models
from django.contrib.auth.models import User

# *Only available for PostgreSQL database
from django.contrib.postgres.fields import ArrayField


class Role(models.Model):
    U = "USER"
    M = "MODERATOR"
    A = "ADMIN"
    role_choices = [
        (U, "USER"),
        (M, "MODERATOR"),
        (A, "ADMIN"),
    ]
    name = models.CharField(
        max_length=12, choices=role_choices, default=U, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class SubReddit(models.Model):
    name = models.CharField(max_length=256)
    moderators = models.ManyToManyField(User, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, blank=True, null=True)
    subreddit_following = models.ManyToManyField(
        SubReddit, blank=True)

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
    links = ArrayField(models.URLField(
        max_length=500, blank=True, null=True), size=10)
    status = models.CharField(
        max_length=10, choices=status_choices, default=P)

    # TODO: We will add file and image fields after wards

    def __str__(self):
        return self.header
