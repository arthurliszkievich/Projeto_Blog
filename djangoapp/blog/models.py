from django.db import models
from utils.rands import slugify, random_slug
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from utils.images import resize_image
from django_summernote.models import AbstractAttachment

User = get_user_model()


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
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
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=100, unique=True, blank=True)

    is_published = models.BooleanField(
        default=False, help_text=('Este campo precisa estar marcado para a página ser exibida no site.')
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
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
        return self.title


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

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

    def __str__(self):
        return self.title


class PostAttachment(AbstractAttachment):
    """
    Modelo para armazenar os anexos (imagens, arquivos) enviados
    através do editor Summernote nos posts.
    """
    # Garanta que o "pass" tenha um recuo (geralmente 4 espaços)
    pass


# **O que este código faz?**
# *   `AbstractAttachment`: É uma classe base fornecida pelo `django-summernote` que já vem com todos os campos necessários para um anexo(nome do arquivo, caminho, data de upload, etc.).
# *   Ao herdar de `AbstractAttachment`, você está criando um modelo concreto no seu banco de dados com toda essa funcionalidade, mas que pertence ao seu aplicativo `blog`.

# **Passo 2: Crie e Aplique as Migrações**

# Agora que você criou um novo modelo, você precisa dizer ao Django para criar a tabela correspondente no seu banco de dados.

# 1. ** Crie o arquivo de migração: **
# ```bash
# docker-compose exec djangoapp python manage.py makemigrations
# ```
# Você deverá ver uma saída dizendo que um novo arquivo de migração foi criado para o modelo `PostAttachment`.

# 2. ** Aplique a migração ao banco de dados: **
# ```bash
# docker-compose exec djangoapp python manage.py migrate
# ```

# **Passo 3: Reinicie o Servidor**

# Após as migrações serem aplicadas, reinicie o servidor para garantir que tudo seja carregado corretamente:
# ```bash
# docker-compose restart djangoapp
