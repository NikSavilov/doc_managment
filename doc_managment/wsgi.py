"""
WSGI config for doc_managment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doc_managment.settings')

application = get_wsgi_application()

# SET env variable RUN_BOT == '0', to start it outside django thread
RUN_BOT = os.environ.get("RUN_BOT", "1")
if RUN_BOT == "1":
    from dashboard.main import get_service
    service = get_service()
