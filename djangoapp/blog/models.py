"""
Módulo de modelos para o aplicativo Blog.

Este módulo contém todos os modelos de dados para o sistema de blog,
incluindo Tags, Categorias, Páginas e Posts. Cada modelo possui
funcionalidades específicas para gerenciamento de conteúdo e SEO.
"""

from django.db import models
from utils.rands import slugify, random_slug
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from utils.images import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse

User = get_user_model()


class Tag(models.Model):
    """
    Modelo para representar tags/etiquetas dos posts.

    As tags são usadas para categorizar e organizar o conteúdo do blog,
    permitindo aos usuários encontrar posts relacionados por tópicos específicos.

    Attributes:
        name (CharField): Nome da tag (máximo 100 caracteres)
        slug (SlugField): Versão URL-friendly do nome, gerada automaticamente

    Meta:
        verbose_name: Nome singular para exibição no admin
        verbose_name_plural: Nome plural para exibição no admin
    """
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para gerar automaticamente o slug.

        O método implementa a seguinte lógica:
        1. Verifica se o slug está vazio
        2. Gera um slug limpo a partir do nome usando a função slugify
        3. Verifica se o slug já existe no banco de dados
        4. Se existir, adiciona um sufixo aleatório para garantir unicidade
        5. Salva o objeto no banco de dados

        Args:
            *args: Argumentos posicionais passados para o método save original
            **kwargs: Argumentos nomeados passados para o método save original
        """
        # 1. VERIFICA SE O SLUG ESTÁ VAZIO
        # Se estiver, significa que estamos criando uma nova tag ou
        # queremos que o slug seja gerado a partir do nome.
        if not self.slug:
            # 2. GERA O SLUG LIMPO
            # Usa a sua poderosa função slugify para limpar o campo 'name'.
            self.slug = slugify(self.name)

        # --- LÓGICA EXTRA PARA GARANTIR UNICIDADE ---
        # Guarda o slug original para o caso de precisarmos adicionar um sufixo
        original_slug = self.slug

        # Procura no banco por outras tags com o mesmo slug.
        # self.__class__ é uma forma segura de se referir ao model atual (Tag).
        # Usamos .exclude(pk=self.pk) para não encontrar a si mesmo ao editar.
        queryset = self.__class__.objects.filter(
            slug=self.slug
        ).exclude(pk=self.pk)

        # 3. VERIFICA SE O SLUG JÁ EXISTE
        # Se o queryset encontrou alguma coisa, significa que o slug já está em uso.
        if queryset.exists():
            # 4. GERA UM NOVO SLUG COM SUFIXO ALEATÓRIO
            # Anexa um hífen e uma string aleatória de 4 caracteres.
            # E repete o processo até encontrar um slug que seja verdadeiramente único.
            self.slug = f'{original_slug}-{random_slug(k=4)}'
        # -----------------------------------------------

        # 5. SALVA NO BANCO DE DADOS
        # Finalmente, chama o método save() original para salvar o objeto no banco.
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Retorna a representação em string da tag.

        Returns:
            str: O nome da tag
        """
        return self.name


class Category(models.Model):
    """
    Modelo para representar categorias dos posts.

    As categorias são usadas para organizar posts em grupos temáticos maiores,
    proporcionando uma estrutura hierárquica de organização do conteúdo.

    Attributes:
        name (CharField): Nome da categoria (máximo 100 caracteres)
        slug (SlugField): Versão URL-friendly do nome, único no sistema

    Meta:
        verbose_name: Nome singular para exibição no admin
        verbose_name_plural: Nome plural para exibição no admin
    """
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True)

    def __str__(self) -> str:
        """
        Retorna a representação em string da categoria.

        Returns:
            str: O nome da categoria
        """
        return self.name


def get_absolute_url(self):
    """
    Retorna a URL canônica para o post.

    Este método é usado pelo Django para gerar URLs para o objeto.
    É especialmente útil em templates e para SEO.

    Returns:
        str: URL do post se publicado e com slug, senão URL da página inicial

    Logic:
        - Se o post não está publicado OU não tem slug: retorna página inicial
        - Se o post está publicado E tem slug: retorna URL específica do post
    """
    # Se o post NÃO tem um slug (ou seja, ainda não foi salvo),
    # ou se ele simplesmente não está publicado, não podemos (ou não queremos)
    # apontar para sua página de detalhe.
    # Nesse caso, podemos retornar para a página inicial do blog.
    if not self.is_published or not self.slug:
        return reverse('blog:index')
    # Se ele está publicado e tem um slug, retornamos a URL correta.
    return reverse('blog:page', args=(self.slug,))


class Page(models.Model):
    """
    Modelo para representar páginas estáticas do site.

    As páginas são conteúdos estáticos como "Sobre", "Contato", etc.
    Diferem dos posts por serem conteúdo mais permanente e não cronológico.

    Attributes:
        title (CharField): Título da página (máximo 65 caracteres)
        slug (SlugField): Versão URL-friendly do título, único no sistema
        is_published (BooleanField): Define se a página está publicada
        content (TextField): Conteúdo da página em texto
    """
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True)

    is_published = models.BooleanField(
        default=False, help_text=('Este campo precisa estar marcado para a página ser exibida no site.')
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para gerar automaticamente o slug.

        Implementa a mesma lógica de geração de slug das Tags,
        garantindo que cada página tenha um slug único.

        Args:
            *args: Argumentos posicionais passados para o método save original
            **kwargs: Argumentos nomeados passados para o método save original
        """
        if not self.slug:
            self.slug = slugify(self.title)

        # A lógica de unicidade pode ser exatamente a mesma
        original_slug = self.slug
        queryset = self.__class__.objects.filter(
            slug=self.slug
        ).exclude(pk=self.pk)

        if queryset.exists():
            self.slug = f'{original_slug}-{random_slug(k=4)}'

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Retorna a representação em string da página.

        Returns:
            str: O título da página
        """
        return self.title


class PostManager(models.Manager):
    """
    Manager customizado para o modelo Post.

    Fornece métodos de consulta específicos para posts, incluindo
    filtros para posts publicados e métodos de conveniência.
    """

    def get_published(self):
        """
        Retorna todos os posts publicados ordenados por ID decrescente.

        Returns:
            QuerySet: Posts publicados ordenados do mais recente para o mais antigo
        """
        return self.filter(is_published=True).order_by('-pk')

    def latest(self):  # type: ignore
        """
        Retorna os 5 posts mais recentes que estão publicados.

        Returns:
            QuerySet: Os 5 posts publicados mais recentes
        """
        return self.get_published()[:5]


class Post(models.Model):
    """
    Modelo principal para representar posts do blog.

    Este é o modelo central do sistema de blog, contendo todos os campos
    necessários para um post completo, incluindo conteúdo, metadados,
    relacionamentos e funcionalidades de SEO.

    Attributes:
        title (CharField): Título do post (máximo 60 caracteres)
        slug (SlugField): Versão URL-friendly do título, único no sistema
        excerpt (CharField): Resumo/descrição do post (máximo 150 caracteres)
        is_published (BooleanField): Define se o post está publicado
        content (TextField): Conteúdo completo do post
        cover (ImageField): Imagem de capa do post
        cover_in_post_content (BooleanField): Se a capa deve aparecer no conteúdo
        created_at (DateTimeField): Data/hora de criação (automática)
        updated_at (DateTimeField): Data/hora da última atualização (automática)
        created_by (ForeignKey): Usuário que criou o post
        updated_by (ForeignKey): Usuário que fez a última atualização
        tags (ManyToManyField): Tags associadas ao post
        category (ForeignKey): Categoria do post

    Meta:
        verbose_name: Nome singular para exibição no admin
        verbose_name_plural: Nome plural para exibição no admin
    """
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=60)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True)
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False, help_text=('Este campo precisa estar marcado para a página ser exibida no site.')
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=False, help_text=('Se marcado, a imagem de capa será exibida no conteúdo do post')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_by')
    # Relacionamento muitos-para-muitos com Tag
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para gerar slug e redimensionar imagens.

        Este método implementa duas funcionalidades principais:
        1. Geração automática de slug único a partir do título
        2. Redimensionamento automático da imagem de capa quando alterada

        O processo é executado na seguinte ordem:
        1. Gera o slug se não existir
        2. Verifica unicidade do slug e adiciona sufixo se necessário
        3. Guarda referência da imagem antiga (se existir)
        4. Salva o objeto no banco de dados
        5. Redimensiona a nova imagem se ela foi alterada

        Args:
            *args: Argumentos posicionais passados para o método save original
            **kwargs: Argumentos nomeados passados para o método save original
        """
        # --- Bloco de Geração de Slug ---
        # (Executado ANTES do super().save())
        if not self.slug:
            # Gera o slug a partir do 'title' e garante unicidade
            self.slug = slugify(self.title)
            original_slug = self.slug
            queryset = self.__class__.objects.filter(
                slug=self.slug
            ).exclude(pk=self.pk)
            if queryset.exists():
                self.slug = f'{original_slug}-{random_slug(k=4)}'

        # --- Bloco de Redimensionamento de Imagem ---

        # 1. Guarda o estado da imagem atual ANTES de salvar o objeto
        # Se o post já existe, pegamos a instância antiga do banco.
        if self.pk:
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_cover = old_instance.cover
        else:
            # Se é um post novo, não há imagem antiga.
            old_cover = None

        # 2. SALVA O OBJETO NO BANCO (com o novo slug e a nova imagem não redimensionada)
        # Este passo é CRUCIAL e deve acontecer apenas UMA VEZ.
        super().save(*args, **kwargs)

        # 3. Verifica se a imagem precisa ser redimensionada DEPOIS de salvar
        # Se o post tiver uma imagem de capa...
        if self.cover:
            # E se a imagem mudou (ou se é um post novo com imagem)
            cover_has_changed = not old_cover or old_cover.name != self.cover.name

            if cover_has_changed:
                print(
                    f'--- Redimensionando a imagem de capa: {self.cover.name} ---')
                # Chama a função para redimensionar, com um tamanho apropriado para posts.
                resize_image(self.cover, new_width=800)

    def get_absolute_url(self):
        """
        Retorna a URL canônica para o post.

        Este método é usado pelo Django para gerar URLs para o objeto.
        É especialmente útil em templates e para SEO.

        Returns:
            str: URL do post se publicado e com slug, senão URL da página inicial

        Logic:
            - Se o post não está publicado OU não tem slug: retorna página inicial
            - Se o post está publicado E tem slug: retorna URL específica do post
        """
        # Se o post NÃO tem um slug (ou seja, ainda não foi salvo),
        # ou se ele simplesmente não está publicado, não podemos (ou não queremos)
        # apontar para sua página de detalhe.
        # Nesse caso, podemos retornar para a página inicial do blog.
        if not self.is_published or not self.slug:
            return reverse('blog:index')
        # Se ele está publicado e tem um slug, retornamos a URL correta.
        return reverse('blog:post', args=(self.slug,))

    def __str__(self):
        """
        Retorna a representação em string do post.

        Returns:
            str: O título do post
        """
        return self.title


class PostAttachment(AbstractAttachment):
    """
    Modelo personalizado para anexos do django-summernote.

    Este modelo estende o AbstractAttachment do django-summernote para
    personalizar o comportamento dos anexos (imagens, arquivos) que são
    inseridos no editor de texto dos posts.

    Herda todos os campos necessários do AbstractAttachment:
    - name: Nome do arquivo
    - file: Arquivo em si
    - uploaded: Data de upload

    Meta:
        verbose_name: Nome singular para exibição no admin
        verbose_name_plural: Nome plural para exibição no admin
    """
    class Meta(AbstractAttachment.Meta):
        verbose_name = 'Post Attachment'
        verbose_name_plural = 'Post Attachments'
