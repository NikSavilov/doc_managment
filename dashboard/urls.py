from django.urls import path

from dashboard.views import login, qs, DocumentsListView, GroupsListView, CategoriesListView

app_name = 'dashboard'
urlpatterns = [
    path('documents/', DocumentsListView.as_view(), name='documents'),
    path('groups/', GroupsListView.as_view(), name='groups'),
    path('categories/', CategoriesListView.as_view(), name='categories'),

    path('login/', login, name='login'),
    path('quick-start/', qs, name='qs'),
]
