from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django_filters.views import FilterView

from dashboard.filter import DocumentFilter, CategoriesFilter
from dashboard.forms import NewGroupCategoryForm
from dashboard.models import Group, InfoObjectCategory, Document, Keyword
from dashboard.models.category import GroupInfoObjectCategory
from dashboard.models.information_object import InformationObject
from doc_managment.settings import MAIN_PAGE


def index(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect(MAIN_PAGE)
    else:
        return redirect('auth_app:login')


def login(request, *args, **kwargs):
    return render(request, "auth/login.html")


def qs(request, *args, **kwargs):
    return render(request, "dashboard/intro.html")


def new_group_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        new_group = Group.objects.create(administrator=user)
        user.profile.groups.add(new_group)
        user.save()
        new_group.save()
        context = {"group": new_group}
        return render(request, "dashboard/new_group.html", context)
    else:
        return redirect('auth_app:login')


class DocumentsListView(FilterView):
    model = Document
    context_object_name = 'docs'
    filter_class = DocumentFilter
    paginate_by = 100

    def get_queryset(self):
        new_context = Document.objects.filter(
            connected_group__id__in=[group.id for group in self.request.user.profile.groups.all()]
        )
        return new_context


class GroupsListView(ListView):
    model = Group
    paginate_by = 100

    def get_queryset(self):
        new_context = self.request.user.profile.groups.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CategoriesListView(FilterView):
    model = InfoObjectCategory
    context_object_name = 'docs'
    filter_class = CategoriesFilter
    paginate_by = 100

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            search_str = kwargs['filter'].data['title__icontains']
        except:
            search_str = ""

        obj_list = kwargs.get('object_list')
        if not search_str:
            groups = self.request.user.profile.groups.all()
            global_categories = InfoObjectCategory.objects.all()
            groups_categories = GroupInfoObjectCategory.objects.filter(group__in=groups)
            context['full_categories'] = [
                {"categories": groups_categories,
                 "title": "Персональные категории"},
                {"categories": global_categories,
                 "title": "Глобальные категории"},
            ]
        else:
            context['full_categories'] = [
                {"categories": obj_list,
                 "title": "Найденные категории"},
            ]
        return context

    def get_queryset(self):
        groups = [gr.id for gr in self.request.user.profile.groups.all()]
        excluded_groups = Group.objects.all().exclude(id__in=groups)
        global_categories = InfoObjectCategory.objects.all().select_subclasses().exclude(
            groupinfoobjectcategory__group__in=excluded_groups)
        return global_categories


def new_category_form_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewGroupCategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            try:
                group = request.user.profile.groups.first()
            except:
                group = None
            cat = GroupInfoObjectCategory(title=data.get("category_name"),
                                          group=group)
            cat.save()
            for kwd in [data.get("keyword_1"), data.get("keyword_2"), data.get("keyword_3")]:
                if kwd:
                    kwd = Keyword(word=kwd, category=cat)
                    kwd.save()

            return redirect("dashboard:categories")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewGroupCategoryForm()

    return render(request, 'dashboard/new_category.html', {'form': form})
