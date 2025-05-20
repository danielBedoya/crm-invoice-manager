"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()


# Only fork a worker process if we're not in the reloader subprocess
if os.environ.get("RUN_MAIN") != "true":
    pid = os.fork()
    if pid == 0:
        from rq import Worker
        from django_rq import get_connection
        from rq import Connection

        with Connection(get_connection("default")):
            worker = Worker(["default"])
            worker.work(burst=False)
        os._exit(0)
