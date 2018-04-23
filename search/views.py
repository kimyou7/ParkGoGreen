from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm

from .models import Park, Report, Category
from .forms import ReportForm


def index(request):
    categories = Category.objects.all()
    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
    login_form = AuthenticationForm
    return render(request, 'search/homepage.html', {'categories': categories, 'latest': latest})


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


class ReportDetailView(generic.DetailView):
    model = Report
