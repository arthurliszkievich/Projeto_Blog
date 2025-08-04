from django.contrib import admin
from blog.models import Tag, Category, Page, Post
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = ['-id']
    prepopulated_fields = {
        "slug": ('name',),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = ['-id']
    prepopulated_fields = {
        "slug": ('name',),
    }


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'slug', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'slug',
    list_per_page = 50
    ordering = 'is_published',
    prepopulated_fields = {
        "slug": ('title',),
    }
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published', 'created_at',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'excerpt', 'content',
    list_per_page = 50
    list_filter = 'category', 'is_published',
    ordering = '-id',
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by',
    prepopulated_fields = {
        "slug": ('title',),
    }
    raw_id_fields = ('category',)
    filter_horizontal = ('tags',)

    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método para preencher created_by e updated_by.
        """
        # Se o objeto está sendo CRIADO (change=False)
        if not change:
            # Atribui o usuário logado ao created_by
            obj.created_by = request.user

        # ATUALIZA O updated_by EM QUALQUER SITUAÇÃO (criação ou edição)
        obj.updated_by = request.user

        # Chama o método original para salvar o objeto no banco
        super().save_model(request, obj, form, change)
