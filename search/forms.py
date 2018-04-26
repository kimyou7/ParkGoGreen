"""
forms.py

https://docs.djangoproject.com/en/2.0/topics/forms/
Here is where you simplify/automate HTML forms using Django. Each form should be a class, and it should extend either
forms.Form or the ModelForm, which builds a form based on an existing model.

Created by Damico Shields according to Django format
"""
from django.forms import ModelForm

from .models import Report


# ModelForm for the Report model, to be used when posting new reports.
class PostForm(ModelForm):

    class Meta:
        model = Report # Which model the form should use
        fields = ['description', 'image', 'type', 'park'] # List of the fields from the model you want the form to use
