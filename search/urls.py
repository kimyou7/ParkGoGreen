"""
Urls specific to this application.

Created by Damico Shields according to Django format.
"""
from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('report/<int:pk>', views.ReportDetailView.as_view(), name='report_detail'), # Uses the report's primary key
    path('signup/', views.signup, name='signup'),
    path('postnew/', views.post_new, name='postnew'),
]