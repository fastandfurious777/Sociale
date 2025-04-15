"""
WSGI config for Sociale project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

BASE_PATH = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_PATH / ".env"
load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sociale.settings")

application = get_wsgi_application()
