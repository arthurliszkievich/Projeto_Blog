# djangoapp/blog/views.py

from .models import Page, Post, Category, Tag
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

User = get_user_model()


class SignUpView(CreateView):
    """
    View para registrar um novo usuário.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:login')
    template_name = 'blog/pages/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Registro - '
        context['page_main_title'] = 'Crie a sua conta'
        return context


# ===================================================================
# VIEWS DE CRIAÇÃO E EDIÇÃO (CRUD)
# ===================================================================

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar um novo Post.
    """
    model = Post
    form_class = PostForm
    # 'slug' foi removido (será gerado no models.py)
    # 'category' foi removido (será tratado no form_valid)
    # 'cover' foi removido (vamos tratar disso a seguir, por enquanto é opcional)
    template_name = 'blog/pages/post_form.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Pega o objeto post configurado
        self.object.created_by = self.request.user  # Vincula o usuário
        self.object.save()  # Salva no banco
        form.save_m2m()  # Salva as tags
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Criar Novo Post - '
        context['page_main_title'] = 'Criar Novo Post'
        context['simple_header_page'] = True
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View para atualizar um Post.
    """
    model = Post
    form_class = PostForm
    # 'slug' foi removido (será gerado no models.py)
    template_name = 'blog/pages/post_form.html'

    def get_success_url(self):
        """
        Define a URL de redirecionamento com base no status do post.
        """
        post = self.get_object()  # Pega o objeto que acabou de ser salvo

        if post.is_published:
            # Se o post foi publicado, redireciona para sua página de visualização
            return reverse('blog:post', kwargs={'slug': post.slug})
        else:
            # Se foi salvo como rascunho, redireciona para a lista de rascunhos
            return reverse('blog:post_drafts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.created_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Editar Post - '
        context['page_main_title'] = 'Editar Post'
        context['simple_header_page'] = True
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/pages/post_confirm_delete.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.created_by

# ===================================================================
# VIEWS DE LISTAGEM
# ===================================================================


class PostListViewBase(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'page_obj'
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.get_published()


class IndexView(PostListViewBase):
    pass


class CategoryView(PostListViewBase):
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

# ===================================================================
# VIEWS DE DETALHE
# ===================================================================


class PageDetailView(DetailView):
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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # A query base agora busca todos os posts
        qs = Post.objects.all()

        # Se o usuário não estiver logado, ele só pode ver os posts publicados.
        # Esta é a regra de segurança para visitantes.
        if not self.request.user.is_authenticated:
            return qs.filter(is_published=True)

        # Se o usuário ESTÁ LOGADO, ele pode ver posts que:
        # 1. Estejam publicados (Q(is_published=True)) OU
        # 2. Tenham sido criados por ele mesmo (Q(created_by=self.request.user))
        return qs.filter(
            Q(is_published=True) | Q(created_by=self.request.user)
            # .distinct() previne duplicatas caso um post seja do autor e também publicado
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['page_title'] = f'{post.title} - '
        return context


# ===================================================================
#   NOVA VIEW PARA RASCUNHOS
# ===================================================================
class DraftsView(LoginRequiredMixin, PostListViewBase):
    """
    Lista os posts não publicados (rascunhos) do usuário logado.
    """

    def get_queryset(self):
        # Sobrescrevemos o queryset para pegar apenas os posts
        # do usuário logado que NÃO estão publicados.
        return Post.objects.filter(
            is_published=False,
            created_by=self.request.user
        ).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Meus Rascunhos - '
        context['page_main_title'] = 'Meus Rascunhos'
        return context


# ===================================================================
# VIEW DE LOGOUT
# ===================================================================


def logout_view(request):
    """
    Função para deslogar o usuário e redirecioná-lo.
    """
    logout(request)
    return redirect('blog:login')
