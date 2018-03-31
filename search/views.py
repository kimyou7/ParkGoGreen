from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView

from .models import Park, Report, Category, Status


def index(request):
    categories = Category.objects.all()
    return render(request, 'search/index.html', {'categories': categories})


def results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        reports = Report.objects.filter(park__name__icontains=q)
        return render(request, 'search/search_results.html', {'reports': reports, 'query': q})
    else:
        q = ""
        reports = Report.objects.all()
        return render(request, 'search/search_results.html', {'reports': reports, 'query': q})
