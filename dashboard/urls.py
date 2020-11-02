from django.urls import path

from dashboard.views import login, qs, DocumentsListView

app_name = 'dashboard'
urlpatterns = [
    path('documents/', DocumentsListView.as_view(), name='documents'),
    path('login/', login, name='login'),
    path('quick-start/', qs, name='qs'),
]
