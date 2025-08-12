# djangoapp/blog/urls.py

from django.urls import path
from . import views  # A importação continua a mesma

app_name = 'blog'

# As chamadas das views foram atualizadas para o formato de classe
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('created_by/<int:id>/', views.CreatedByView.as_view(), name='created_by'),
]
