"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application

# Serverless cold-start verification: auto-initialize tables if empty on Vercel
if os.environ.get('VERCEL'):
    try:
        from django.db import connection
        from django.core.management import call_command
        tables = connection.introspection.table_names()
        if 'drtc_app_servicepackage' not in tables:
            call_command('migrate', interactive=False)
            call_command('seed_data', interactive=False)
    except Exception as exc:
        print(f"[Vercel Startup Notice] DB check: {exc}")
