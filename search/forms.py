"""
forms.py

https://docs.djangoproject.com/en/2.0/topics/forms/
Here is where you simplify/automate HTML forms using Django. Each form should be a class, and it should extend either
forms.Form or the ModelForm, which builds a form based on an existing model.

Created by Damico Shields according to Django format
"""
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Report, Category


# ModelForm for the Report model, to be used when posting new reports.
class PostForm(ModelForm):

    class Meta:
        model = Report # Which model the form should use
        fields = ['park', 'type', 'image', 'description'] # List of the fields from the model you want the form to use

    # Excludes All from the post drop down menu
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Category.objects.exclude(type="All Categories")
        self.fields['image'].required = False


# Sign up form with added email field and optional name fields.
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
