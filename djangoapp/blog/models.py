from django.db import models
from utils.rands import slugify, random_slug


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
