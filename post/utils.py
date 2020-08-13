from rest_framework.permissions import BasePermission

from .models import *


def does_post_exist(pk):
    try:
        p = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return False
    return True


def is_post_pending(pk):
    try:
        p = Post.objects.get(pk=pk)
        if p.status == "PENDING":
            return True
        else:
            return False
    except Post.DoesNotExits:
        return False


def does_user_exist(pk):
    try:
        u = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return False
    return True


def does_comment_exist(pk):
    try:
        c = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return False
    return True


def does_tag_exist(pk):
    try:
        t = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return False
    return True


def does_tag_exist_by_name(name):
    try:
        t = Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        return False
    return True


# Returns a tag object if exists else creates one and returns
def get_tag_or_add(name):
    try:
        t = Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        return Tag.objects.create(name=name)
    return t


def does_profile_exist(pk):
    try:
        p = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return False
    return True


def does_subreddit_exist(pk):
    try:
        t = SubReddit.objects.get(pk=pk)
    except SubReddit.DoesNotExist:
        return False
    return True


def is_post_in_subreddit(post_id, subreddit_id):
    try:
        p = Post.objects.get(pk=post_id)
        if p.subreddit.id == int(subreddit_id):
            return True
        return False
    except Post.DoesNotExist:
        return False


# TODO : Check if given user is a moderator for the SubReddit
def is_user_moderator(user_id, subreddit_id):
    return True


def is_user_following_subreddit(user_id, subreddit_id):
    try:
        user = User.objects.get(pk=user_id)
        if subreddit_id in [subreddit.id for subreddit in user.profile.subreddit_following.all()]:
            return True
        return False
    except User.DoesNotExist:
        return False


# TODO : Check if given user has the permisssion to edit the SubReddit
class EditSubRedditPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


# TODO : Check if given user has the permission to edit the Post
class EditPostPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


# TODO : Check if given user has the permisssion to delete the SubReddit
class DeleteSubRedditPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


# TODO : Check if given user has the permisssion to delete the Post
class DeletePostPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
