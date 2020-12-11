from django.conf.urls import url
from django.urls import path

from dashboard.forms import NewGroupCategoryForm
from dashboard.models import Document, InfoObjectCategory
from dashboard.views import login, qs, DocumentsListView, GroupsListView, CategoriesListView, new_group_view, \
    new_category_form_view

app_name = 'dashboard'
urlpatterns = [
    url(r"^documents/$", DocumentsListView.as_view(model=Document, filterset_fields={'filename': ['icontains'],
                                                                                     'source': ['exact'],
                                                                                     'category': ['exact'],
                                                                                     }), name='documents'),
    url(r"^categories/$", CategoriesListView.as_view(model=InfoObjectCategory,
                                                     filterset_fields={'title': ['icontains'],
                                                                       }), name='categories'),
    path('new-category/', new_category_form_view, name='new_category'),

    path('groups/', GroupsListView.as_view(), name='groups'),

    path('login/', login, name='login'),
    path('quick-start/', qs, name='qs'),
    path('new-group/', new_group_view, name='new_group'),

]
