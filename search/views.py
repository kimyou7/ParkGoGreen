from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView

from .models import Park, Report, Category
from .forms import ReportForm


def index(request):
    categories = Category.objects.all()
    return render(request, 'search/index.html', {'categories': categories})


def results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        t = request.GET['dropdown']
        reports = Report.objects.filter(park__name__icontains=q, type__type__iexact=t)
        all_reports = Report.objects.all()
        return render(request, 'search/search_results.html', {'reports': reports, 'query': q, 'all_reports': all_reports})
    else:
        q = ""
        reports = Report.objects.all()
        return render(request, 'search/search_results.html', {'reports': reports, 'query': q})


def get_report(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('')
    else:
        form = ReportForm

    return render(request, 'report.html', {'form': form})