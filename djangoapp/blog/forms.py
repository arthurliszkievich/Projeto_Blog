# djangoapp/blog/forms.py

from django import forms
from .models import Post, Tag, Category
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):

    category_input = forms.CharField(
        label='Ou crie uma nova categoria',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nome da nova categoria'})
    )

    tags_input = forms.CharField(
        label='Tags (separadas por vírgula)',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Ex: Python, Django, Web'})
    )

    # 2. DEFINIR O CAMPO 'content' PARA USAR O EDITOR AVANÇADO
    # Isso transforma a caixa de texto simples em um editor completo.
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Post
        # 3. ADICIONAR 'cover_in_post_content' À LISTA DE CAMPOS
        # Isso fará a caixa de seleção aparecer no formulário.
        fields = ['title', 'excerpt', 'content', 'cover',
                  'cover_in_post_content', 'category', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        if self.instance and self.instance.pk:
            tags = self.instance.tags.all()
            self.fields['tags_input'].initial = ', '.join(t.name for t in tags)

    def clean(self):
        # 1. Pega todos os dados já "limpos" (validados) pelo Django
        cleaned_data = super().clean()

        # 2. Pega os valores dos dois campos de categoria
        category_selected = cleaned_data.get('category')
        category_typed = cleaned_data.get('category_input', '').strip()

        # 3. VALIDAÇÃO PRINCIPAL:
        # Se o usuário não escolheu uma categoria no menu E também não digitou
        # uma nova categoria no campo de texto, nós lançamos um erro.
        if not category_selected and not category_typed:
            # Esta mensagem de erro será exibida no template
            raise forms.ValidationError(
                'Você deve escolher uma categoria existente ou criar uma nova.',
                code='no_category_selected_or_created'
            )

        # 4. LÓGICA DE CRIAÇÃO:
        # Se o usuário digitou uma nova categoria, nós a criamos (ou a pegamos se já existir)
        # e a definimos como a categoria oficial do formulário.
        if category_typed:
            category_obj, created = Category.objects.get_or_create(
                name=category_typed)
            cleaned_data['category'] = category_obj

        # 5. Retorna os dados limpos e prontos para serem salvos.
        return cleaned_data

    # 6. SALVANDO O POST:

    def save(self, commit=True, user=None):
        # 1. Pegamos o objeto post, mas ainda não salvamos no banco
        post = super().save(commit=False)

        # Se o usuário foi passado como argumento (da view), nós o vinculamos
        if user:
            post.created_by = user

        # Agora podemos salvar o post no banco, com o 'created_by' já definido
        if commit:
            post.save()

        # A lógica das tags continua a mesma...
        # No entanto, mas ela só deve rodar se o post foi salvo (commit=True)
        if commit:
            post.tags.clear()
            tags_str = self.cleaned_data.get('tags_input', '')
            if tags_str:
                tag_names = [name.strip() for name in tags_str.split(',')]
                for name in tag_names:
                    if name:
                        tag, created = Tag.objects.get_or_create(name=name)
                        post.tags.add(tag)

        return post
