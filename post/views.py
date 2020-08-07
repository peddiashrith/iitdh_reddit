from django.shortcuts import render, redirect
from django.db.models import Q  # Filtering Usage
from django.contrib import messages  # Quick Messages
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, Http404

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


def create_post(request):
    form = PostCreateForm()
    if request.method == "POST":
        newpost = PostCreateForm(request.POST)
        if newpost.is_valid():
            print("New Post is: ", newpost)
            newpost = newpost.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('pending_posts')
        else:
            return HttpResponse("Form is not valid")
    context = {'form': form}
    return render(request, 'post/create_post.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post}
    return render(request, 'post/post_detail.html', context)


def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404
    form = PostEditForm(instance=post)
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('pending_posts')
        else:
            return HttpResponse("Form is not valid")
    context = {'form': form}
    return render(request, 'post/update_post.html', context)
