from django import forms
from .models import *
from django.contrib.postgres.forms import SimpleArrayField


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('header', 'tags', 'links')


class PostEditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('header', 'tags', 'links')
