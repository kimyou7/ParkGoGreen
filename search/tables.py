"""
tables.py

Structure for the django_tables2 library. Github: https://github.com/jieter/django-tables2
Creates a Django work flow for easily creating sortable, paginated tables.
"""
import django_tables2 as tables
from django_tables2 import A
from .models import Report


# Table of reports. Adds a column of links that point towards individual report pages and can't be sorted.
class ReportTable(tables.Table):
    link = tables.LinkColumn('search:report_detail', text='Link', args=[A('pk')], attrs={'a': {'target': '_blank'}},
                             orderable=False)

    class Meta:
        model = Report
        template_name = 'django_tables2/bootstrap4.html'
        exclude = ['id', 'image', 'thumbnail']  # Exclude the primary key and image urls from the table