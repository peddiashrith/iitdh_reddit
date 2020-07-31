from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .views import *


"""

"""

router = routers.DefaultRouter()
router.register(r'feed', ViewPostsFeed)
router.register(r'post', ViewPosts)
router.register(r'subreddit', ViewSubReddit)


urlpatterns = [
    path('api/', include(router.urls)),
    path('pending_posts/', pending_posts, name="pending_posts"),
    path('accepted_posts/', accepted_posts, name="accepted_posts"),
    path('accept_post/<int:id>/', accept_post, name="accept_post"),
    path('create_post/', create_post, name="create_post"),
    path('edit_post/<int:id>/', edit_post, name="edit_post"),
    path('post/<int:id>/', post_detail, name="post_detail"),
]
