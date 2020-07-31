from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile, Post, SubReddit, Tag, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['subreddit_following']


class FeedPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['author', 'header', 'subreddit', 'tags', 'links']

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        pass


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = ['author', 'header', 'subreddit', 'tags', 'links', 'status']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "author" in validated_data:
            validated_data.pop('author')
        instance.header = validated_data.get('header', instance.header)
        instance.subreddit = validated_data.get('subreddit', instance.header)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.links = validated_data.get('links', instance.links)
        instance.status = validated_data.get('header', instance.status)
        return instance


class SubRedditSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubReddit
        fields = ['name', 'moderators', 'tags']


""" Serializer for just listing comments not for editing and creating comments """
class ListCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['user', 'timestamp', 'text']
        read_only_fields = ['user', 'timestamp', 'text']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

