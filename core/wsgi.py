from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
import os

load_dotenv()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

application = get_wsgi_application()
