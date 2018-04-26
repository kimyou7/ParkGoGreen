from django.contrib import admin

from .models import Category, Status, Park, Report

# Registers models to the built-in Django Admin page.
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Park)
admin.site.register(Report)