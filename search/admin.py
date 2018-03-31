from django.contrib import admin

from .models import Category, Status, Park, Report
# Register your models here.
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Park)
admin.site.register(Report)