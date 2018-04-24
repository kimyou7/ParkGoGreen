from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('report/<int:pk>', views.ReportDetailView.as_view(), name='report_detail'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]