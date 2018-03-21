from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.


def index(request):
    return render(request, 'search/index.html')


def results(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form'
    return HttpResponse(message)

