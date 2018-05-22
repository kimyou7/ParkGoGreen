"""
Urls specific to this application.

Created by Damico Shields according to Django format.
"""
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('report/<int:pk>', views.ReportDetailView.as_view(), name='report_detail'), # Uses the report's primary key
    path('signup/', views.signup, name='signup'),
    path('postnew/', views.post_new, name='postnew'),
    path('dashboard/', views.dash_table, name='dashboard'),
    path('update/<int:pk>/', views.ReportUpdate.as_view(), name='report_update'),
    path('update/<int:pk>/delete/', views.ReportDelete.as_view(), name='report_delete'),
    path('about/', TemplateView.as_view(template_name='search/about.html'), name='about'),
    path('about/damico/', TemplateView.as_view(template_name='search/damicoprofile.html'), name='damico'),
    path('about/jaimes/', TemplateView.as_view(template_name='search/jaimes.html'), name='jaimes'),
    path('about/justice/', TemplateView.as_view(template_name='search/justiceprofile.html'), name='justice'),
    path('about/andrew/', TemplateView.as_view(template_name='search/andrewprofile.html'), name='andrew'),
    path('about/leo/', TemplateView.as_view(template_name='search/leoprofile.html'), name='leo'),
    path('about/kimyou/', TemplateView.as_view(template_name='search/kimprofile.html'), name='kimyou'),
    path('privacy/', TemplateView.as_view(template_name='search/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='search/terms.html'), name='terms'),
]