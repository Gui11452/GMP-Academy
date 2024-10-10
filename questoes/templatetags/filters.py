from django import template
from perfil.models import Planos, Perfil
from duvidas.models import Comentarios, Duvidas, Respostas, ReportarDuvidasProfessor
from questoes.models import Questao

register = template.Library()

@register.filter(name='plural_questoes')
def plural_questoes(num_questoes):
    if num_questoes == 1:
        return f'Foi encontrada {num_questoes} questão'
    return f'Foram encontradas {num_questoes} questões'

@register.filter(name='plural_aulas')
def plural_aulas(num_aulas):
    if num_aulas == 1:
        return f'Foi encontrada {num_aulas} aula'
    return f'Foram encontradas {num_aulas} aulas'


@register.filter(name='formata_slug_string')
def formata_slug_string(formata_slug_string):
    return formata_slug_string.replace('_', ' ').replace('-', ' ')

@register.filter(name='formata_preco_mensal')
def formata_preco_mensal(preco):
    if len(str(preco)) == 4:
        return f'R$ {preco}0'.replace('.', ',')
    else:
        return f'R$ {preco}'.replace('.', ',')
    
@register.filter(name='formata_preco_cheio')
def formata_preco_cheio(preco):
    return f'R$ {round(preco * 21.5)}'.replace('.', ',')

@register.filter(name='formata_plano')
def formata_plano(plano: Planos):
    if plano.tipo == 'basico':
        return plano.tipo.replace('a', 'á')
    elif plano.tipo == 'intermediario':
        return plano.tipo.replace('a', 'á')
    elif plano.tipo == 'avancado':
        return plano.tipo.replace('c', 'ç')
    
@register.filter(name='formata_plano2')
def formata_plano2(plano):
    if plano == 'basico':
        return plano.replace('a', 'á')
    elif plano == 'intermediario':
        return plano.replace('a', 'á')
    elif plano == 'avancado':
        return plano.replace('c', 'ç')
    

@register.filter(name='len_comentarios')
def len_comentarios(questao_id):
    if Questao.objects.filter(id=questao_id).exists():
        questao = Questao.objects.get(id=questao_id)
        comentarios = len(Comentarios.objects.filter(questao=questao))
        return comentarios
    else:
        return 0
    
@register.filter(name='len_duvidas')
def len_duvidas(questao_id):
    if Questao.objects.filter(id=questao_id).exists():
        questao = Questao.objects.get(id=questao_id)
        duvidas = len(Duvidas.objects.filter(questao=questao))
        return duvidas
    else:
        return 0
    
@register.filter(name='len_duvidas_professor')
def len_duvidas_professor(questao_id):
    if Questao.objects.filter(id=questao_id).exists():
        questao = Questao.objects.get(id=questao_id)
        duvidas_professor = len(ReportarDuvidasProfessor.objects.filter(questao=questao))
        return duvidas_professor
    else:
        return 0
    

@register.filter(name='foto_perfil')
def foto_perfil(user):
    if Perfil.objects.filter(usuario=user).exists():
        perfil = Perfil.objects.get(usuario=user)
        foto = perfil.foto
        if foto:
            return foto.url
