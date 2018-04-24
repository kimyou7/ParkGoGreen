from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy

from .models import Report


def index(request):
    latest = Report.objects.filter(sub_date__lte=timezone.now()).order_by('-sub_date')[:5]
    login_form = AuthenticationForm
    return render(request, 'search/homepage.html', {'latest': latest})


def results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
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


class ReportDetailView(generic.DetailView):
    model = Report


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'search/signup.html'
