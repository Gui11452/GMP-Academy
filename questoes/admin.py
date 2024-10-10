from django.contrib import admin
from .models import Questao, QuestaoRespondida, Aula, Banca, Disciplina, Ano, Prova, Estado
from django_summernote.admin import SummernoteModelAdmin

class BancaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    list_per_page = 10
    search_fields = ('nome',)

admin.site.register(Banca, BancaAdmin)

class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    list_per_page = 10
    search_fields = ('nome',)

admin.site.register(Estado, BancaAdmin)

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    list_per_page = 10
    search_fields = ('nome',)

admin.site.register(Disciplina, DisciplinaAdmin)

class AnoAdmin(admin.ModelAdmin):
    list_display = ('valor',)
    list_display_links = ('valor',)
    list_per_page = 10
    search_fields = ('valor',)

admin.site.register(Ano, AnoAdmin)

class ProvaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    list_per_page = 10
    search_fields = ('nome',)

admin.site.register(Prova, ProvaAdmin)


class QuestaoAdmin(SummernoteModelAdmin):
    list_display = ('codigo', 'disciplina', 'ano', 'prova', 'banca', 'estado', 'visibilidade')
    list_display_links = ('codigo', 'disciplina', 'ano', 'prova', 'banca', 'estado')
    list_filter = ('disciplina', 'ano', 'prova', 'gabarito_alternativa', 'visibilidade', 'banca', 'estado')
    list_per_page = 10
    list_editable = ('visibilidade',)
    search_fields = ('texto', 'codigo', 'disciplina__nome', 'ano__valor', 'prova__nome', 'banca__nome', 'estado__nome')
    summernote_fields = ('texto',)
    readonly_fields = ('gabarito_texto', 'codigo',)
    ordering = ('-codigo',)

admin.site.register(Questao, QuestaoAdmin)

class QuestoesRespondidasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'questao', 'resposta')
    list_display_links = ('usuario', 'questao', 'resposta')
    list_filter = ('resposta',)
    list_per_page = 10
    search_fields = ('usuario__username', 'questao__codigo', 'questao__ano__valor', 'questao__disciplina__nome', 'questao__prova__nome', 'resposta')

admin.site.register(QuestaoRespondida, QuestoesRespondidasAdmin)


class AulaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'disciplina', 'visibilidade')
    list_display_links = ('nome', 'descricao', 'disciplina')
    list_filter = ('disciplina', 'visibilidade')
    list_editable = ('visibilidade',)
    list_per_page = 10
    search_fields = ('nome', 'descricao', 'disciplina')

admin.site.register(Aula, AulaAdmin)
