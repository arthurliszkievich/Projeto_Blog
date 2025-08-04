from django.db import models
from django.conf import settings
from utils.model_validators import validate_png
from utils.images import resize_image


class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'site_setup.SiteSetup', on_delete=models.CASCADE, null=True, blank=True,
        related_name='menu_links')

    def __str__(self):
        return self.text


class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/', verbose_name='Favicon',
        # Assuming validade_png is defined in utils/model_validators
        null=True, blank=True, validators=[validate_png],

    )

    def save(self, *args, **kwargs):

        # 1. Guarda o estado original do objeto ANTES de salvar
        # Se self.pk não existe, é um objeto novo.
        if self.pk:
            # Busca a versão antiga do objeto diretamente do banco de dados
            old_instance = SiteSetup.objects.get(pk=self.pk)
            # Pega o nome do favicon antigo
            old_favicon_name = str(old_instance.favicon.name)
        else:
            # Se é um objeto novo, não há favicon antigo
            old_favicon_name = None

        # 2. Salva o objeto no banco de dados
        # Isso é importante para que o arquivo de imagem seja enviado para o disco
        # e o self.favicon.name seja atualizado com o caminho final.
        super().save(*args, **kwargs)

        # 3. Verifica se a imagem precisa ser redimensionada
        # Garante que o campo favicon não está vazio
        if self.favicon:
            # Compara o nome do favicon atual com o antigo
            favicon_has_changed = old_favicon_name != str(self.favicon.name)

            # Se o favicon mudou (ou se é um objeto novo com um favicon), redimensiona.
            if favicon_has_changed:
                print(
                    f"--- Redimensionando favicon: {self.favicon.name} para 32px ---")
                resize_image(self.favicon, new_width=32)

    def __str__(self):
        return self.title
