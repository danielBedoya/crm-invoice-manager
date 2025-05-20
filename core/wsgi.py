"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import threading
from rq import Worker, Connection
from django_rq import get_connection

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

def start_worker():
    with Connection(get_connection("default")):
        worker = Worker(["default"])
        worker.work(burst=False)  # Set to False to keep it running continuously

threading.Thread(target=start_worker, daemon=True).start()
