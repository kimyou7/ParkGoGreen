import django_tables2 as tables
from django_tables2 import A
from .models import Report


class ReportTable(tables.Table):
    link = tables.LinkColumn('search:report_detail', text='Link', args=[A('pk')], attrs={'a': {'target': '_blank'}})

    class Meta:
        model = Report
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['id', 'image', 'thumbnail']