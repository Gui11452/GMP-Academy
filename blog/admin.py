from django.contrib import admin
from .models import Post, Categoria
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
	list_display = ('titulo', 'descricao', 'data_publicacao', 'data_alteracao', 'visibilidade', 'categoria')
	list_display_links = ('titulo', 'descricao', 'data_publicacao', 'data_alteracao', 'categoria')
	list_filter = ('data_publicacao', 'visibilidade', 'categoria')
	list_editable = ('visibilidade',)
	readonly_fields = ('slug',)
	list_per_page = 20
	summernote_fields = ('texto',)
	search_fields = ('titulo', 'descricao', 'texto', 'categoria__nome')

admin.site.register(Post, PostAdmin)

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	list_display_links = ('nome',)
	list_per_page = 20
	search_fields = ('nome',)

admin.site.register(Categoria, CategoriaAdmin)
