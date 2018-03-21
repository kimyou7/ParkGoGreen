from django.shortcuts import render
from django.http import HttpResponse

from .models import Park

# Create your views here.


def index(request):
    return render(request, 'search/index.html')


def results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        reports = Park.objects.filter(name__icontains=q)
        return render(request, 'search/search_results.html', {'reports': reports, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
