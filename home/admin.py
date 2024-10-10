from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import SobreNos, FaleConosco, EmailsProntos, ArquivosExcel

class SobreNosAdmin(SummernoteModelAdmin):
    list_display = ('titulo', 'video', 'foto')
    list_display_links  = ('titulo', 'video', 'foto')
    summernote_fields = ('texto',)
    list_per_page = 10
    search_fields = ('titulo',)

admin.site.register(SobreNos, SobreNosAdmin)

class FaleConoscoAdmin(SummernoteModelAdmin):
    list_display = ('usuario', 'data' ,'titulo', 'assunto')
    list_display_links  = ('usuario', 'data', 'titulo', 'assunto')
    list_filter = ('usuario',  'data')
    list_per_page = 10
    search_fields = ('usuario__username', 'titulo', 'assunto')

admin.site.register(FaleConosco, FaleConoscoAdmin)

class EmailsProntosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'texto1', 'texto2')
    list_display_links  = ('titulo', 'texto1', 'texto2')
    list_per_page = 10
    readonly_fields = ('contagem',)
    search_fields = ('titulo', 'texto1', 'texto2')

admin.site.register(EmailsProntos, EmailsProntosAdmin)

class ArquivosExcelAdmin(admin.ModelAdmin):
    list_display = ('arquivo',)
    list_display_links  = ('arquivo',)
    list_per_page = 10

admin.site.register(ArquivosExcel, ArquivosExcelAdmin)
