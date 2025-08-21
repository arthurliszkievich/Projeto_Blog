# djangoapp/blog/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),

    # A URL mais específica ('create') vem primeiro.
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),

    # As URLs com variáveis vem depois.
    path('post/<slug:slug>/update/',
         views.PostUpdateView.as_view(), name='post_update'),


    path('post/<slug:slug>/delete/',
         views.PostDeleteView.as_view(), name='post_delete'),

    # A URL mais genérica ('catch-all' para slugs) vem por último.
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post'),


    # --- OUTRAS ROTAS ---
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('created_by/<int:id>/', views.CreatedByView.as_view(), name='created_by'),
    path('my-posts/drafts/', views.DraftsView.as_view(), name='post_drafts'),

    # --- ROTAS DE AUTENTICAÇÃO ---
    path('login/', auth_views.LoginView.as_view(template_name='blog/pages/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
