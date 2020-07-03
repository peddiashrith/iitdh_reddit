from django.shortcuts import render, redirect
from django.db.models import Q  # Filtering Usage
from django.contrib import messages  # Quick Messages
from django.shortcuts import get_object_or_404
from .models import *


def pending_posts(request):
    posts = Post.objects.filter(status=Post.P)
    context = {"posts": posts}
    return render(request, 'post/pending_posts.html', context)


def accepted_posts(request):
    posts = Post.objects.filter(status=Post.A)
    context = {"posts": posts}
    return render(request, 'post/accepted_posts.html', context)


def accept_post(request, id):
    post = Post.objects.get(id=id)
    post.status = Post.A
    post.save()
    return redirect("pending_posts")
