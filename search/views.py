"""
Views in Django take a Web request and return a Web response, like HTML, a 404 error, etc.
https://docs.djangoproject.com/en/2.0/topics/http/views/

Try to keep most of the logic here.
If the view is a function, then it should return a render with the request, the template it is serving, and the third
is a dictionary that is passed to the template, which can be referenced by key in the template using Django tags.

Created by Damico Shields according to Django Format.
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy

from .models import Report
from .forms import PostForm


# Homepage view. Retrieves 5 latest reports based on their submission date, loads homepage.html
def index(request):
    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
    login_form = AuthenticationForm
    return render(request, 'search/homepage.html', {'latest': latest})


# Search results view. Called by the form in base_generic.html Takes the category and type, uses them to filter results
# from the database, then returns them to search_results.html.
def results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if len(q) > 40:
            latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
            error = "Please keep search under 40 characters."
            return render(request, 'search/homepage.html', {'latest': latest, 'error': error})
        t = request.GET['dropdown']
        reports = Report.objects.filter(park__name__icontains=q, type__type__iexact=t)
        similar = Report.objects.filter(type__type__iexact=t)
        return render(request, 'search/search_results.html', {'reports': reports, 'query': q, 'similar': similar})
    else:
        q = ""
        t = request.GET['dropdown']
        reports = []
        similar = Report.objects.filter(type__type__iexact=t)
        return render(request, 'search/search_results.html', {'reports': reports, 'query': q, 'similar': similar})


# Detailed report view in class form. Extends Django's generic DetailView.
class ReportDetailView(generic.DetailView):
    model = Report


# Registration view extending the Django generic CreateView and using the Django UserCreationForm. On success, redirects
# to the success_url. Loads the signup.html
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'search/signup.html'


# Report posting view extending CreateView and using the PostForm created by us. On a succesful posting redirects to the
# homepage. Loads post_report.html
class PostReport(generic.CreateView):
    form_class = PostForm
    success_url = reverse_lazy('search:index')
    template_name = 'search/post_report.html'
