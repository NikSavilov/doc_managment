import django_filters
from django_filters import CharFilter

from dashboard.models import Document, InfoObjectCategory


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = Document
        fields = ["source"]


class CategoriesFilter(django_filters.FilterSet):
    class Meta:
        model = InfoObjectCategory
        fields = ["title", ]
