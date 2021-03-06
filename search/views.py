"""
Views in Django take a Web request and return a Web response, like HTML, a 404 error, etc.
https://docs.djangoproject.com/en/2.0/topics/http/views/

If the view is a function, then it should return a render with the request, the template it is serving, and the third
is a dictionary that is passed to the template, which can be referenced by key in the template using Django tags.

Class based views extend generic Django views, and interact with models automatically. Set the meta data to reference
the model you want.

Created by Damico Shields according to Django Format.
"""
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django_tables2 import RequestConfig


from .models import Report, Category
from .forms import PostForm, SignUpForm, UpdateForm
from .tables import ReportTable


# Homepage view. Retrieves 5 latest reports based on their submission date, loads homepage.html
def index(request):
    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
    issue_types = Category.objects.all()
    return render(request, 'search/homepage.html', {'latest': latest, 'issue_types': issue_types})


# Search results view. Called by the form in base_generic.html Takes the category and type, uses them to filter results
# from the database, then returns them to search_results.html.
def results(request):
    categories = Category.objects.all()
    category = request.GET['dropdown']

    # Query search
    if request.GET['q']:
        query = request.GET['q']
        query = query.strip()

        # Input validation: checks for alphanumeric and that it's shorter than 40 characters.
        if not all(x.isalnum() or x.isspace() for x in query):
            latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
            error = "Please enter alphanumeric characters only. Search either by zip code or park name."
            return render(request, 'search/homepage.html', {'latest': latest, 'error': error})
        if len(query) > 40:
            latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
            error = "Please keep search under 40 characters. Search either by zip code or park name"
            return render(request, 'search/homepage.html', {'latest': latest, 'error': error})

        # Category set to All
        if category == 'All Categories':
            if len(query) == 5 and query.isdigit():  # zip code search
                reports = Report.objects.filter(park__zip_code__iexact=query)
                if not reports:
                    reports = Report.objects.all()
                    allmsg = "here are all of the park reports."
                    return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': query, 
                          'categories': categories, 'err': "zip code", 
                          'cat': category, 'is_reports': False, 'allmsg': allmsg})
            else:
                reports = Report.objects.filter(park__name__icontains=query)  # Park name search
            if not reports:  # if neither is found, similar reports are found
                if len(query) > 5 and query.isdigit():  # filters out numbers that are too long
                    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
                    error = "Not a valid zip code"
                    return render(request, 'search/homepage.html', {'latest': latest, 'error': error})
                reports = Report.objects.all()
                return render(request, 'search/search_results.html', {
                    'reports': reports, 'query': query, 'err': "search criteria", 
                    'categories': categories,
                    'cat': category, 'is_reports': False})
            return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': query, 
                          'categories': categories, 
                          'cat': category, 'is_reports': True})

        # Category specified
        else:
            if len(query) == 5 and query.isdigit():
                reports = Report.objects.filter(park__zip_code__iexact=query, type__type__iexact=category)
                if not reports:
                    reports = Report.objects.filter(type__type__iexact=category)
                    return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': query, 'err': "zip code", 
                          'categories': categories,
                          'cat': category, 'is_reports': False})
            else:
                reports = Report.objects.filter(park__name__icontains=query, type__type__iexact=category)  
            if not reports:
                if len(query) > 5 and query.isdigit():
                    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
                    error = "Not a valid zip code"
                    return render(request, 'search/homepage.html', {'latest': latest, 'error': error})
                reports = Report.objects.filter(type__type__iexact=category)
                return render(request, 'search/search_results.html', {
                    'reports': reports, 'query': query, 'err': "search criteria", 
                    'categories': categories,
                    'cat': category, 'is_reports': False})
            return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': query, 
                          'categories': categories,
                          'cat': category, 'is_reports': True})

    # Category search (if search is empty)
    else:
        if category == 'All Categories':
            reports = Report.objects.all()
            message = "here are all of the park report"
            return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': False, 'msg': message,
                          'categories': categories, 'cat': category})
        else:
            message = "here are the " + category.lower() + " report"
            reports = Report.objects.filter(type__type__iexact=category)
            return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': False, 'msg': message,
                          'categories': categories, 'cat': category})


# Detailed report view in class form. Extends Django's generic DetailView.
class ReportDetailView(generic.DetailView):
    model = Report


# Registration view with required email field and optional name fields.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  # Validates the data, returns error messages if anything is wrong.
            form.save()
            raw_username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=raw_username, password=raw_password)
            login(request, user)
            g = Group.objects.get(name='Registered User')  # Automatically makes a new user a Registered User
            g.user_set.add(request.user)
            return redirect('search:index')
    else:
        form = SignUpForm()
    return render(request, 'search/signup.html', {'form': form})


# Posts new report view. On success, redirects to the new individual report page. On failure, reloads with saved info.
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # Repopulates form with data on rejected submission.
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.user = request.user
            post.sub_date = timezone.now()
            post.save()
            return redirect('search:report_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'search/post_report.html', {'form': form})


# Update report view, extends Django generic UpdateView. Used by City Managers to change the type and stats of a report.
# PermissionRequiredMixin makes it so only users with permission to change reports can see this page.
class ReportUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'search.change_report'
    model = Report
    form_class = UpdateForm
    template_name_suffix = '_update_form'


# Delete report view, extends DeleteView. Used by City Managers to delete a report. Can only be seen by users with
# permission to delete reports.
class ReportDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'search.delete_report'
    model = Report
    success_url = reverse_lazy('search:index')


# Dashboard table view. Populates a ReportTable from tables.py and sends it to the html. Can only be seen by users
# with the ability to delete reports, ie. City Managers, enforced by the permission_required decorator.
@permission_required('search.delete_report')
def dash_table(request):
    table = ReportTable(Report.objects.all(), order_by='-sub_date')
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'search/dashboard.html', {'table': table})
