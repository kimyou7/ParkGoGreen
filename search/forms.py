from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Report


class PostForm(ModelForm):

    class Meta:
        model = Report
        fields = ['description', 'image', 'type', 'park']
