from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic.list import ListView

from dashboard.models import Group, InfoObjectCategory
from dashboard.models.information_object import InformationObject
from doc_managment.settings import MAIN_PAGE


def index(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect(MAIN_PAGE)
    else:
        return redirect('auth:login')


def login(request, *args, **kwargs):
    return render(request, "auth/login.html")


def qs(request, *args, **kwargs):
    return render(request, "dashboard/intro.html")


class DocumentsListView(ListView):
    model = InformationObject
    paginate_by = 100

    def get_queryset(self):
        new_context = InformationObject.objects.filter(
            connected_group__id__in=[group.id for group in self.request.user.groups.all()]
        )
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class GroupsListView(ListView):
    model = Group
    paginate_by = 100

    def get_queryset(self):
        new_context = self.request.user.groups.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CategoriesListView(ListView):
    model = InfoObjectCategory
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        groups = self.request.user.groups.all()
        docs = InformationObject.objects.filter(
            connected_group__id__in=[group.id for group in groups]
        )
        categories = list(set([doc.category for doc in docs if doc]))
        cat_list = [{"category": cat,
                     "docs": InformationObject.objects.filter(category=cat)[:2]}
                    for cat in categories]
        context['now'] = timezone.now()
        context['categories'] = cat_list
        return context
