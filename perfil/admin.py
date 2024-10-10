from django.contrib import admin
from .models import Perfil, RecuperacaoSenha, Planos, Pedido, Topicos

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'verificacao_email', 'codigo', 'foto')
    list_display_links = ('usuario', 'verificacao_email', 'foto')
    list_filter = ('verificacao_email',)
    list_per_page = 10
    search_fields = ('usuario__username',)
    readonly_fields = ('codigo',)

admin.site.register(Perfil, PerfilAdmin)

class TopicosAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    list_per_page = 10
    search_fields = ('nome',)

admin.site.register(Topicos, TopicosAdmin)

class TopicosInline(admin.TabularInline):
	model = Topicos
	extra = 1

class PlanosAdmin(admin.ModelAdmin):
    inlines = [
		TopicosInline
	]
    list_display = ('nome', 'preco', 'tipo')
    list_display_links = ('nome', 'preco', 'tipo')
    list_filter = ('preco',)
    list_filter = ('tipo',)
    list_per_page = 10

admin.site.register(Planos, PlanosAdmin)

class RecuperacaoSenhaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo', 'data' ,'recuperacao')
    list_display_links = ('usuario', 'codigo', 'data' ,'recuperacao')
    list_filter = ('recuperacao', 'data')
    list_per_page = 10
    search_fields = ('usuario__username',)
    readonly_fields = ('codigo',)

admin.site.register(RecuperacaoSenha, RecuperacaoSenhaAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('comprador', 'metodo_pagamento', 'preco_pedido', 'status_pedido', 'data_pedido', 'plano_ativo', 'plano')
    list_display_links = ('comprador', 'metodo_pagamento', 'preco_pedido', 'status_pedido', 'plano_ativo', 'plano')
    list_filter = ('metodo_pagamento', 'status_pedido', 'data_pedido', 'plano_ativo', 'plano')
    list_per_page = 10
    search_fields = ('comprador__usuario__username',)

admin.site.register(Pedido, PedidoAdmin)
