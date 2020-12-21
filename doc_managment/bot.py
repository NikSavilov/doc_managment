import os
import django
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

os.chdir(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doc_managment.settings")
django.setup()

if __name__ == "__main__":
    from dashboard.main import get_service

    service = get_service()
