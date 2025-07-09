from django.contrib import admin
from .models import MenuLink, SiteSetup


# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = ('text', 'url_or_path', 'new_tab')
#     search_fields = ('text', 'url_or_path')
#     list_filter = ('new_tab',)
#     ordering = ('text',)


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1
    verbose_name = 'Menu Link'
    verbose_name_plural = 'Menu Links'


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'show_header', 'show_search',
                    'show_menu', 'show_description', 'show_pagination', 'show_footer')
    search_fields = ('title', 'description')
    list_filter = ('show_header', 'show_search', 'show_menu',
                   'show_description', 'show_pagination', 'show_footer')
    ordering = ('title',)
    inlines = [MenuLinkInline]

    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()
