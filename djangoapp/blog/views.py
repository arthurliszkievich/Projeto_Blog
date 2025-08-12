# djangoapp/blog/views.py

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Page, Post, Category, Tag

User = get_user_model()


# O SiteSetupMixin foi removido, pois o Context Processor cuidará disso.

class PostListViewBase(ListView):  # <- Herança de SiteSetupMixin removida
    """
    Classe base para todas as listagens de posts.
    Ela configura o modelo, template, paginação e o queryset base.
    """
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'page_obj'
    paginate_by = 9

    def get_queryset(self):
        """
        Define o queryset base para todas as listagens.
        """
        return self.model.objects.get_published()


class IndexView(PostListViewBase):  # Herda diretamente de ListView
    pass


class CategoryView(PostListViewBase):
    """View para listar posts de uma categoria."""

    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            Category, slug=self.kwargs.get('slug'))
        return qs.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Categoria: {self.category.name} - '
        context['page_main_title'] = f'Categoria: "{self.category.name}"'
        return context


class TagView(PostListViewBase):
    """View para listar posts de uma tag."""

    def get_queryset(self):
        qs = super().get_queryset()
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return qs.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Tag: {self.tag.name} - '
        context['page_main_title'] = f'Tag: "{self.tag.name}"'
        return context


class CreatedByView(PostListViewBase):
    """View para listar posts de um autor."""

    def get_queryset(self):
        qs = super().get_queryset()
        self.author = get_object_or_404(User, pk=self.kwargs.get('id'))
        return qs.filter(created_by=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_full_name = self.author.get_full_name() or self.author.username
        context['page_title'] = f'Posts de {author_full_name} - '
        context['page_main_title'] = f'Posts de "{author_full_name}"'
        return context


class SearchView(PostListViewBase):
    """View para a página de busca."""

    def get_queryset(self):
        qs = super().get_queryset()
        self.search_value = self.request.GET.get('q', '').strip()

        if not self.search_value:
            return qs.none()

        return qs.filter(
            Q(title__icontains=self.search_value) |
            Q(excerpt__icontains=self.search_value) |
            Q(content__icontains=self.search_value)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_value'] = self.search_value
        context['page_title'] = f'Busca: "{self.search_value}" - '
        context['page_main_title'] = f'Busca por "{self.search_value}"'
        return context


class PageDetailView(DetailView):  # <- Herança de SiteSetupMixin removida
    """View para a página de detalhe de uma Página estática."""
    model = Page
    template_name = 'blog/pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        context['page_title'] = f'{page.title} - '
        return context


class PostDetailView(DetailView):  # <- Herança de SiteSetupMixin removida
    """View para a página de detalhe de um Post."""
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['page_title'] = f'{post.title} - '
        return context
