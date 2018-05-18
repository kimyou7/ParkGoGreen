"""
WSGI config for csc648team13 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/bitnami/apps/django/django_projects//opt/bitnami/apps/django/django_projects/csc648-team13')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects//opt/bitnami/apps/django/django_projects/csc648-team13/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csc648-team13.settings")

application = get_wsgi_application()
