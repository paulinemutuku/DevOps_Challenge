import os
import sys
import django
from django.conf import settings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ["DJANGO_SETTINGS_MODULE"] = "fitness_booking.settings"
django.setup()

print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"Settings module exists: {hasattr(settings, 'INSTALLED_APPS')}")
