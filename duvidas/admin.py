from django.contrib import admin
from .models import Duvidas, Respostas, Comentarios, ReportarDuvidasProfessor

class DuvidasAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'questao', 'texto', 'arquivo', 'data', 'visibilidade', 'questao')
	list_display_links = ('usuario', 'questao', 'texto', 'arquivo', 'data')
	list_filter = ('data', 'questao')
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('usuario__username', 'questao.texto', 'texto')

admin.site.register(Duvidas, DuvidasAdmin)

class ReportarDuvidasProfessorAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'questao', 'texto', 'arquivo', 'data', 'visibilidade', 'questao')
	list_display_links = ('usuario', 'questao', 'texto', 'arquivo', 'data')
	list_filter = ('data', 'questao')
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('usuario__username', 'questao.texto', 'texto')

admin.site.register(ReportarDuvidasProfessor, ReportarDuvidasProfessorAdmin)

class ComentariosAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'questao', 'texto', 'data', 'visibilidade')
	list_display_links = ('usuario', 'questao', 'texto', 'data')
	list_filter = ('data', 'questao')
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('usuario__username', 'questao.texto', 'texto')

admin.site.register(Comentarios, ComentariosAdmin)

class RespostasAdmin(admin.ModelAdmin):
	list_display = ('duvida', 'texto', 'data', 'visibilidade')
	list_display_links = ('duvida', 'texto', 'data')
	list_filter = ('data',)
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('usuario__username', 'texto')

admin.site.register(Respostas, RespostasAdmin)