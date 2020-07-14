from django import forms
from .models import *
from django.contrib.postgres.forms import SimpleArrayField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit



class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('header', 'tags', 'links')
        widgets = {
         'header': forms.TextInput(attrs={'class': 'textinput textInput header'}),
         'tags': forms.SelectMultiple(attrs={'class': 'selectmultiple tags'}),
         'links' : forms.TextInput(attrs={'class': 'textinput textInput links'})
         }



class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('header', 'tags', 'links')
        widgets = {
         'header': forms.TextInput(attrs={'class': 'textinput textInput header'}),
         'tags': forms.SelectMultiple(attrs={'class': 'selectmultiple tags'}),
         'links' : forms.TextInput(attrs={'class': 'textinput textInput links'})
         }
