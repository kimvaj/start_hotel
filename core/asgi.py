from django.core.asgi import get_asgi_application
from dotenv import load_dotenv
import os

load_dotenv()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

application = get_asgi_application()
