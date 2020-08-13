from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
# router.register(r'post', ViewPosts)
router.register(r'subreddit', ViewSubReddit)
router.register(r'profile', ViewUserProfiles)

post_update_urls = ViewPosts.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

post_create_url = ViewPosts.as_view({'post':'create'})

post_comments_url = ViewPosts.as_view({'get': 'comments'})
post_create_comment_url = ViewPosts.as_view({'post': 'create_comment'})

subreddit_accept_post = ViewSubReddit.as_view({'post':'accept'})

feed_list_url = ViewPostsFeed.as_view({"get":"list"})
post_detail_url = ViewPostsFeed.as_view({"get":"retrieve"})

# username_profile = ViewUserProfiles.as_view({"get":"username"})

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/feed/', feed_list_url, name='feed'), # Returns feed of all posts
    path('api/post/', post_create_url, name='post_create'), # Creates a post
    path('api/post/<int:pk>/', post_update_urls, name='post_update'), # update/partial_update/delete a post
    path('api/posts/<int:pk>/', post_detail_url, name='post_detail'), # Returns a single post
    path('api/post/<int:pk>/comments/', post_comments_url, name='post_comments'),
    path('api/post/<int:pk>/comment/', post_create_comment_url, name='post_create_comment'),
    # path('api/profile/username/<str:u_name>/', username_profile, name='user_username'),
    # path('pending_posts/', pending_posts, name="pending_posts"),
    # path('accepted_posts/', accepted_posts, name="accepted_posts"),
    # path('accept_post/<int:id>/', accept_post, name="accept_post"),
    # path('create_post/', create_post, name="create_post"),
    # path('edit_post/<int:id>/', edit_post, name="edit_post"),
    # path('post/<int:id>/', post_detail, name="post_detail"),
]
