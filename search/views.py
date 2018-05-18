"""
Views in Django take a Web request and return a Web response, like HTML, a 404 error, etc.
https://docs.djangoproject.com/en/2.0/topics/http/views/

Try to keep most of the logic here.
If the view is a function, then it should return a render with the request, the template it is serving, and the third
is a dictionary that is passed to the template, which can be referenced by key in the template using Django tags.

Created by Damico Shields according to Django Format.
"""
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User, Group


from .models import Report, Category
from .forms import PostForm, SignUpForm


# Homepage view. Retrieves 5 latest reports based on their submission date, loads homepage.html
def index(request):
    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
    return render(request, 'search/homepage.html', {'latest': latest})


# Search results view. Called by the form in base_generic.html Takes the category and type, uses them to filter results
# from the database, then returns them to search_results.html.
def results(request):
    categories = Category.objects.all()
    category = request.GET['dropdown']

    # Query search
    if request.GET['q']:
        query = request.GET['q']
        query = query.strip()

        # Input validation
        if not all(x.isalnum() or x.isspace() for x in query):
            latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
            error = "Please enter alphanumeric characters only. Search either by zip code, park name or city name."
            return render(request, 'search/homepage.html', {'latest': latest, 'error': error})
        if len(query) > 40:
            latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
            error = "Please keep search under 40 characters. Search either by zip code, park name or city name"
            return render(request, 'search/homepage.html', {'latest': latest, 'error': error})

        # Category set to All
        if category == 'All Categories':
            reports = Report.objects.filter(park__name__icontains=query) \
                    | Report.objects.filter(park__zip_code__iexact=query)
            if not reports:
                if len(query) > 5 and query.isdigit():
                    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
                    error = "Not a valid zip code"
                    return render(request, 'search/homepage.html', {'latest': latest, 'error': error})
                reports = Report.objects.all()
            return render(request, 'search/search_results.html', {
                'reports': reports, 'query': query, 'categories': categories, 'cat': category, 'is_reports': True})

        # Category specified
        else:
            reports = Report.objects.filter(park__name__icontains=query, type__type__iexact=category) \
                    | Report.objects.filter(park__zip_code__iexact=query, type__type__iexact=category)
            if not reports:
                if len(query) > 5 and query.isdigit():
                    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
                    error = "Not a valid zip code"
                    return render(request, 'search/homepage.html', {'latest': latest, 'error': error})
                reports = Report.objects.filter(type__type__iexact=category)
            return render(request, 'search/search_results.html', {
                'reports': reports, 'query': query, 'categories': categories.exclude(type__iexact=category),
                'cat': category, 'is_reports': True})

    # Category search (if search is empty)
    else:
        if category == 'All Categories':
            reports = Report.objects.all()
            message = "here are all of the park report"
            return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': False, 'msg': message,
                          'categories': categories.exclude(type__iexact=category), 'cat': category})
        else:
            message = "here are the " + category.lower() + " report"
            reports = Report.objects.filter(type__type__iexact=category)
            return render(request, 'search/search_results.html', {
                          'reports': reports, 'query': False, 'msg': message,
                          'categories': categories.exclude(type__iexact=category), 'cat': category})


# Detailed report view in class form. Extends Django's generic DetailView.
class ReportDetailView(generic.DetailView):
    model = Report


# Registration with required remail field and optional name fields.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            raw_username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=raw_username, password=raw_password)
            login(request, user)
            g = Group.objects.get(name='Registered User')
            g.user_set.add(request.user)
            return redirect('search:index')
    else:
        form = SignUpForm()
    return render(request, 'search/signup.html', {'form': form})


# Posts new report. On success, redirects to the new individual report page. On failure, reloads with saved info.
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # request.session['new_report'] = form
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.user = request.user
            post.sub_date = timezone.now()
            post.save()
            return redirect('search:report_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'search/post_report.html', {'form': form})