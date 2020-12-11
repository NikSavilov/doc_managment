import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doc_managment.settings")
django.setup()

if __name__ == "__main__":
    from dashboard.main import get_service

    service = get_service()
