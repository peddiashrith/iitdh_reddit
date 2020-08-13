from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *
from .utils import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['subreddit_following']


# This serializer is for read-only operations
class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class TagSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []},
        }


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['post', 'url']


# This serializer is for read-only operations
class FeedPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    links = serializers.SlugRelatedField(slug_field='url', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'header', 'description', 'subreddit', 'tags', 'links']


# This serializer is used to update and create posts
class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)
    tags = TagSerializerPost(many=True, required=False)
    links = LinkSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'author', 'header', 'description', 'subreddit', 'tags', 'links']

    def create(self, validated_data):
        tags = self.context.get("tags")
        links = self.context.get("links")
        post = Post.objects.create(**validated_data)
        if tags is not None:
            for tag in tags:
                post.tags.add(get_tag_or_add(tag))
        if links is not None:
            for link in links:
                post.links.create(url=link)
        return post

    # This update function will not update author for a post
    # TODO: Make SubReddit not editable directly by update method
    def update(self, instance, validated_data):
        is_partial = self.context.get("partial")
        if "author" in validated_data:
            validated_data.pop('author')
        tags = self.context.get("tags")
        links = self.context.get("links")
        super().update(instance, validated_data)
        if tags is not None:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(get_tag_or_add(tag))
            instance.save()
        if links is not None:
            instance.links.all().delete()
            for link in links:
                instance.links.create(url=link)
            instance.save()
        return instance


class SubRedditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = SubReddit
        fields = ['id', 'name', 'moderators', 'tags']

    def create(self, validated_data):
        moderators = validated_data.pop('moderators')
        subreddit = SubReddit.objects.create(**validated_data)
        tags = self.context.get('tags')
        if moderators is not None:
            for m in moderators:
                subreddit.moderators.add(m)
        if tags is not None:
            for tag in tags:
                subreddit.tags.add(get_tag_or_add(tag))
            subreddit.save()
        return subreddit

    def update(self, instance, validated_data):
        moderators = validated_data.pop('moderators', None)
        tags = self.context.get('tags')
        super().update(instance, validated_data)
        if moderators is not None:
            instance.moderators.clear()
            for mod in moderators:
                instance.moderators.add(mod)
        if tags is not None:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(get_tag_or_add(tag))
        instance.save()
        return instance


""" Serializer for just listing comments not for editing and creating comments """


class ListCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['user', 'timestamp', 'text']
        read_only_fields = ['user', 'timestamp', 'text']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'timestamp', 'text']
