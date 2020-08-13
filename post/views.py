from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Q  # Filtering Usage
from django.contrib import messages  # Quick Messages
from django.http import HttpResponse, HttpResponseRedirect, Http404

from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import *
from .forms import *
from .serializers import *
from .utils import *

# def pending_posts(request):
#     posts = Post.objects.filter(status=Post.P)
#     context = {"posts": posts}
#     return render(request, 'post/pending_posts.html', context)
#
#
# def accepted_posts(request):
#     posts = Post.objects.filter(status=Post.A)
#     context = {"posts": posts}
#     return render(request, 'post/accepted_posts.html', context)
#
#
# def accept_post(request, id):
#     post = Post.objects.get(id=id)
#     post.status = Post.A
#     post.save()
#     return redirect("pending_posts")
#
#
# def create_post(request):
#     form = PostCreateForm()
#     if request.method == "POST":
#         newpost = PostCreateForm(request.POST)
#         if newpost.is_valid():
#             print("New Post is: ", newpost)
#             newpost = newpost.save(commit=False)
#             newpost.author = request.user
#             newpost.save()
#             return redirect('pending_posts')
#         else:
#             return HttpResponse("Form is not valid")
#     context = {'form': form}
#     return render(request, 'post/create_post.html', context)


# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id)
#     context = {'post': post}
#     return render(request, 'post/post_detail.html', context)


# def edit_post(request, id):
#     post = get_object_or_404(Post, id=id)
#     if post.author != request.user:
#         raise Http404
#     form = PostEditForm(instance=post)
#     if request.method == "POST":
#         form = PostEditForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('pending_posts')
#         else:
#             return HttpResponse("Form is not valid")
#     context = {'form': form}
#     return render(request, 'post/update_post.html', context)


""" API Class for viewing and updating sub reddit details"""


class ViewSubReddit(viewsets.ModelViewSet):
    serializer_class = SubRedditSerializer
    queryset = SubReddit.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'pending' or self.action == 'accept' or self.action == 'users':
            permission_classes = [permissions.IsAuthenticated]
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes += [permissions.IsAdminUser, permissions.IsAuthenticated, EditSubRedditPermission]
        if self.action == 'delete':
            permission_classes += [permissions.IsAdminUser, permissions.IsAuthenticated,
                                   EditSubRedditPermission, DeleteSubRedditPermission]

        return [permission() for permission in permission_classes]

    """
    {
        "name": "Third sub reddit",
        "moderators": [
            1                   # ID of the moderators
        ],
        "tags": [
            "tag1",
            "tag2
        ]
    }
    """

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        tags = data.pop('tags', None)
        serializer = SubRedditSerializer(data=data, context={"tags": tags})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'SubReddit Created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'detail': 'Invalid SubReddit', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if not does_subreddit_exist(pk):
            return Response(data={'detail': 'SubReddit does not exist'}, status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        prev_sub_reddit = SubReddit.objects.get(pk=pk)
        tags = data.pop('tags', None)
        serializer = SubRedditSerializer(prev_sub_reddit, data=data, context={"tags": tags})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'SubReddit Updated'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'detail': 'Invalid SubReddit', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # For retrieving the pending posts for a subreddit
    # pk is the primary key of the subreddit whose pending posts you need
    @action(methods=['get'], detail=True)
    def pending(self, request, pk=None):
        if not does_subreddit_exist(pk):
            return Response(data={'detail': 'SubReddit Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        if not is_user_moderator(request.user.id, pk):
            return Response(data={'detail': 'User is not moderator for this SubReddit'},
                            status=status.HTTP_401_UNAUTHORIZED)
        sub_reddit = self.get_object()
        posts = sub_reddit.post_set.filter(status="PENDING")
        serializer = FeedPostSerializer(posts, many=True)
        return Response(serializer.data)

    # TODO : Dealing with already Accepted and Rejected Posts
    """
    This method is for accepting a post by moderator
    input Post JSON object
    Example:
    {
    'accepting_post_id':'2'        // ID of the Sub Reddit
    }
    """

    @action(methods=['post'], detail=True)
    def accept(self, request, pk=None):
        if not does_subreddit_exist(pk):
            return Response(data={'detail': 'SubReddit Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        post_id = data.get('accepting_post_id')
        if not is_user_moderator(request.user.id, pk):
            return Response(data={'detail': 'User is not moderator for sub reddit'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not does_post_exist(post_id):
            return Response(data={'detail': 'Post Not Found'}, status=status.HTTP_404_NOT_FOUND)
        if not is_post_in_subreddit(post_id, pk):
            return Response(data={'detail': 'Post Not Found in this subreddit'}, status=status.HTTP_404_NOT_FOUND)

        post = Post.objects.get(pk=post_id)
        post.status = Post.A
        post.save()
        return Response(data={'detail': 'status saved'}, status=status.HTTP_200_OK)

    """
    sample post body
    {
    "rejecting_post_id":25
    }
    
    """

    # TODO : Dealing with already Accepted and Rejected Posts
    @action(methods=['post'], detail=True)
    def reject(self, request, pk=None):
        if not does_subreddit_exist(pk):
            return Response(data={'detail': 'SubReddit Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        post_id = data.get('rejecting_post_id')
        if not is_user_moderator(request.user.id, pk):
            return Response(data={'detail': 'User is not moderator for sub reddit'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not does_post_exist(post_id):
            return Response(data={'detail': 'Post Not Found'}, status=status.HTTP_404_NOT_FOUND)
        if not is_post_in_subreddit(post_id, pk):
            return Response(data={'detail': 'Post Not Found in this subreddit'}, status=status.HTTP_404_NOT_FOUND)
        post = Post.objects.get(pk=post_id)
        post.status = Post.R
        post.save()
        return Response(data={'detail': 'status saved'}, status=status.HTTP_200_OK)

    """
    For retriving all the users following the sub reddit
    """

    @action(methods=['get'], detail=True)
    def users(self, request, pk=None):
        if not does_subreddit_exist(pk):
            return Response(data={'detail': 'SubReddit Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        users = [i.user for i in SubReddit.objects.get(pk=pk).profile_set.all()]
        serializer = UserSerializer(users, many=True)
        try:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data={'error': 'Internal Exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    """
    For removing a user from subreddit by moderator
    """

    @action(methods=['post'], detail=True)
    def remove_user(self, request, pk=None):
        if not does_subreddit_exist(pk):
            return Response(data={'detail': 'SubReddit Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        user_id = data.get('user_id')
        if not does_user_exist(user_id):
            return Response(data={'detail': 'User Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
        if not is_user_following_subreddit(user_id, pk):
            return Response(data={'detail': 'User does not follow given SubReddit'}, status=status.HTTP_404_NOT_FOUND)
        if not is_user_moderator(request.user.id, pk):
            return Response(data={'detail': 'User is not moderator for sub reddit'},
                            status=status.HTTP_401_UNAUTHORIZED)
        profile = Profile.objects.get(user__id=user_id)
        profile.subreddit_following.remove(pk)
        return Response(data={'detail': 'User is removed'}, status=status.HTTP_200_OK)


""" API class for viewing/creating/updating/deleting posts"""


class ViewPosts(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'create_comment':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated, EditPostPermission]
        elif self.action == "delete":
            permission_classes = [permissions.IsAuthenticated, EditPostPermission, DeletePostPermission]
        return [permission() for permission in permission_classes]

    """
    Sample create post Json body
    {
        "header": "Post 1",
        "subreddit": 1,
        "tags": [
            "tag2",
            "tag3",
            "tag200"
        ],
        "description":"This is Post description",
        "links": [
            "http://localhost:8000/admin/post/tag/",
            "http://localhost:8000/admin/post/tag/",
            "http://youtube.com/"
        ]
    }
    """

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        if not is_user_following_subreddit(request.user.id, data.get('subreddit')):
            return Response(data={'detail': 'User is not following the sub reddit'},
                            status=status.HTTP_401_UNAUTHORIZED)
        data['author'] = request.user.id
        tags = data.pop('tags', None)
        links = data.pop('links', None)
        serializer = PostSerializer(data=data, context={"tags": tags, "links": links})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'Post Created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'detail': 'Invalid Post', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    """
        You cannot update Author of the post or subreddit for a post
        Sample update post Json body
        {
            "header": "Post 1",
            "tags": [
                "tag2",
                "tag3",
                "tag200"
            ],
            "description":"This is Post description",
            "links": [
                "http://localhost:8000/admin/post/tag/",
                "http://localhost:8000/admin/post/tag/",
                "http://youtube.com/"
            ]
        }
    """

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if not does_post_exist(pk):
            return Response(data={'detail': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        prev_post = Post.objects.get(pk=kwargs['pk'])
        data['author'] = prev_post.author.id
        tags = data.pop('tags', None)
        links = data.pop('links', None)
        serializer = PostSerializer(prev_post, data=data,
                                    context={"tags": tags, "links": links, "partial": False})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'Post Updated'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'detail': 'Invalid Post', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if not does_post_exist(pk):
            return Response(data={'detail': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        prev_post = Post.objects.get(pk=kwargs['pk'])
        tags = data.pop('tags', None)
        links = data.pop('links', None)
        serializer = PostSerializer(prev_post, data=data, partial=True
                                    , context={"tags": tags, "links": links, "partial": True})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'Post Updated'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'detail': 'Invalid Details', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    # For fetching comments for a particular post
    @action(methods=['get'], detail=True)
    def comments(self, request, pk=None):
        if not does_post_exist(pk):
            return Response(data={'detail': 'Post Not Found'}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post=pk)
        serializer = ListCommentsSerializer(comments, many=True)
        return Response(serializer.data)

    # To creating comment for a post
    """
    {
    "post":"17",
    "text":"This is a good post"
    }
    """

    @action(methods=['post'], detail=True)
    def create_comment(self, request, pk=None):
        data = JSONParser().parse(request)
        if not does_post_exist(pk) or not does_post_exist(data.get('post')):
            return Response(data={'detail': 'Post Not Found'}, status=status.HTTP_404_NOT_FOUND)
        data['user'] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail ': 'Comment Saved'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'detail': 'Invalid Request', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


"""API class for retriving feed for users  """


class ViewPostsFeed(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedPostSerializer
    queryset = Post.objects.filter(status="ACCEPTED")


class ViewUserProfiles(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == "follow" or self.action == "unfollow" or self.action == "following":
            permission_classes += [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    # Get user's profile using username
    @action(methods=['get'], detail=False, url_path='username/(?P<u_name>\w+)')
    def username(self, request, u_name):
        try:
            user = User.objects.get(username=u_name)
        except User.DoesNotExist:
            return Response(data={'detail': 'username does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    """
    For making a user follow a subreddit
    sample JSON request object
    {
    "subreddit_id":2
    }
    """

    @action(methods=["post"], detail=False)
    def follow(self, request):
        user_id = request.user.id
        data = JSONParser().parse(request)
        subreddit_id = data['subreddit_id']
        if is_user_following_subreddit(user_id, subreddit_id):
            return Response(data={'detail': 'user is already following the subreddit'}, status=status.HTTP_200_OK)
        if not does_subreddit_exist(subreddit_id):
            return Response(data={'detail': 'subreddit does not exist'}, status=status.HTTP_404_NOT_FOUND)

        profile = User.objects.get(pk=user_id).profile
        profile.subreddit_following.add(SubReddit.objects.get(pk=subreddit_id))
        profile.save()
        return Response(data={'detail': 'profile updated'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def unfollow(self, request):
        user_id = request.user.id
        data = JSONParser().parse(request)
        subreddit_id = data['subreddit_id']
        if not is_user_following_subreddit(user_id, subreddit_id):
            return Response(data={'detail': 'user already not following the subreddit'}, status=status.HTTP_200_OK)
        if not does_subreddit_exist(subreddit_id):
            return Response(data={'detail': 'subreddit does not exist'}, status=status.HTTP_404_NOT_FOUND)

        profile = User.objects.get(pk=user_id).profile
        profile.subreddit_following.remove(SubReddit.objects.get(pk=subreddit_id))
        profile.save()
        return Response(data={'detail': 'profile updated'}, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def following(self, request):
        user_id = request.user.id
        serializer = SubRedditSerializer(User.objects.get(pk=user_id).profile.subreddit_following.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

