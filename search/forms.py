"""
forms.py

https://docs.djangoproject.com/en/2.0/topics/forms/
Here is where you simplify/automate HTML forms using Django. Each form should be a class, and it should extend either
forms.Form or the ModelForm, which builds a form based on an existing model.

Created by Damico Shields according to Django format
"""

from django.forms import ModelForm

from .models import Report, Category


# ModelForm for the Report model, to be used when posting new reports.
class PostForm(ModelForm):

    class Meta:
        model = Report # Which model the form should use
        fields = ['park', 'type', 'image', 'description'] # List of the fields from the model you want the form to use

    # Excludes All from the post drop down menu
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Category.objects.exclude(type="All")
        self.fields['image'].required = False
