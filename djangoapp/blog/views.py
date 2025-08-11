# djangoapp/blog/views.py

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Page, Category, Tag
from site_setup.models import SiteSetup

User = get_user_model()


def index(request):
    """
    View para a página inicial, que lista todos os posts publicados.
    """
    # A consulta foi movida para DENTRO da view.
    posts = Post.objects.get_published()
    site_setup = SiteSetup.objects.first()

    # Ajustado para 9 para um grid 3x3, por exemplo
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_setup': site_setup,
    }

    return render(request, 'blog/pages/index.html', context)


def category(request, slug):
    """
    View para listar todos os posts publicados de uma categoria específica.
    """
    # Encontra a categoria pelo slug. Se não existir, retorna erro 404.
    # Usamos .get(slug=slug) porque o slug da categoria é único.
    category_obj = get_object_or_404(Category, slug=slug)
    site_setup = SiteSetup.objects.first()

    # Filtra os posts que pertencem à categoria E estão publicados.
    # O Django permite filtrar diretamente pelo objeto da chave estrangeira.
    posts = Post.objects.get_published().filter(category=category_obj)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_setup': site_setup,
        'page_title': f'Categoria: {category_obj.name} - ',
        'page_main_title': f'Categoria: "{category_obj.name}"',
    }

    # Reutilizamos o template index.html, que já sabe listar e paginar posts.
    return render(request, 'blog/pages/index.html', context)


def page(request, slug):
    """
    View para exibir uma única Página estática (como 'Sobre' ou 'Contato').
    """
    # Esta view busca um objeto 'Page', não um 'Post'.
    page_obj = get_object_or_404(Page, slug=slug, is_published=True)
    site_setup = SiteSetup.objects.first()

    context = {
        'page': page_obj,
        'site_setup': site_setup,
        'page_title': f"{page_obj.title} - ",
    }

    return render(request, 'blog/pages/page.html', context)


def post(request, slug):
    """
    View para exibir um único Post do blog.
    """
    post_obj = get_object_or_404(Post.objects.get_published(), slug=slug)
    site_setup = SiteSetup.objects.first()

    context = {
        'post': post_obj,
        'site_setup': site_setup,
        'page_title': f"{post_obj.title} - ",
    }

    return render(request, 'blog/pages/post.html', context)


def created_by(request, id):
    author = get_object_or_404(User, pk=id)
    site_setup = SiteSetup.objects.first()
    posts = Post.objects.get_published().filter(created_by=author)
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # NOME COMPLETO DO AUTOR
    author_full_name = author.get_full_name()
    if not author_full_name:
        author_full_name = author.username

    context = {
        'page_obj': page_obj,
        'site_setup': site_setup,
        # Título para a aba do navegador
        'page_title': f'Posts de {author_full_name} - ',
        # Título para ser exibido no conteúdo da página
        'page_main_title': f'Posts de "{author_full_name}"',
    }

    return render(request, 'blog/pages/index.html', context)


def search(request):
    """
    View para a página de resultados de busca.
    """
    search_value = request.GET.get('q', '').strip()

    # Se a busca for vazia, redirecionamos para a página inicial.
    if not search_value:
        return redirect('blog:index')

    # A consulta agora é feita aqui dentro.
    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value)
    ).order_by('-pk')  # Ordena pelos mais recentes

    site_setup = SiteSetup.objects.first()

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_setup': site_setup,
        'search_value': search_value,
        'page_title': f'Busca: "{search_value}" - ',
    }

    return render(request, 'blog/pages/index.html', context)


def tag(request, slug):
    """
    View para listar todos os posts publicados de uma tag específica.
    """
    # Encontra a tag pelo slug. Se não existir, retorna erro 404.
    # Usamos .get(slug=slug) porque o slug da tag é único.
    tag_obj = get_object_or_404(Tag, slug=slug)
    site_setup = SiteSetup.objects.first()

    # Filtra os posts que pertencem à tag E estão publicados.
    # O Django permite filtrar diretamente pelo objeto da chave estrangeira.
    posts = Post.objects.get_published().filter(tags=tag_obj)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_setup': site_setup,
        'page_title': f'Tag: {tag_obj.name} - ',
        'page_main_title': f'Tag: "{tag_obj.name}"',
    }

    # Reutilizamos o template index.html, que já sabe listar e paginar posts.
    return render(request, 'blog/pages/index.html', context)
