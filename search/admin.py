"""
Registers models from the database to be displayed in the built-in Django Admin page
"""

from django.contrib import admin

from .models import Category, Status, Park, Report

admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Park)
admin.site.register(Report)
