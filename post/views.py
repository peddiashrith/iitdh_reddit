from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Q  # Filtering Usage
from django.contrib import messages  # Quick Messages
from django.http import HttpResponse, HttpResponseRedirect, Http404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import *
from .forms import *
from .serializers import FeedPostSerializer, PostSerializer, SubRedditSerializer, ListCommentsSerializer


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


""" API Class for viewing and updating sub reddit details"""


class ViewSubReddit(viewsets.ModelViewSet):
    serializer_class = SubRedditSerializer
    queryset = SubReddit.objects.all()

    # For retrieving the pending posts for a subreddit
    # pk is the primary key of the subreddit whose pending posts you need
    @action(methods=['get'], detail=True)
    def peding_posts(self, request, pk=None):
        sub_reddit = self.get_object()
        posts = sub_reddit.post_set.filter(status="PENDING")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


""" API class for viewing/creating/updating/deleting posts"""


class ViewPosts(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    http_method_names = ['post', 'put', 'delete', 'get']

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    # For getting comments for a particular post
    @action(methods=['get'], detail=True)
    def comments(self, request, pk=None):
        comments = Comment.objects.filter(post=pk)
        serializer = ListCommentsSerializer(data=comments, many=True)
        return Response(serializer.data)


"""API class for retriving feed for users  """


class ViewPostsFeed(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedPostSerializer
    queryset = Post.objects.all()
