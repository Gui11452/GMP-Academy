from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from functools import reduce
from operator import or_
from django.db.models import Q
from gmp.settings import RECAPTCHA_FRONT, RECAPTCHA_BACK, DOMINIO
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import Questao, QuestaoRespondida, Aula, Banca, Estado, Disciplina, Ano, Prova
from duvidas.models import Comentarios, Duvidas, Respostas, ReportarDuvidasProfessor
from perfil.models import Perfil, Pedido
import requests
import json
import re
from questoes.utils import verify_acess_questions

def questoes(request):
    _redirect = verify_acess_questions(request)
    if _redirect:
        return redirect(_redirect)
    
    # Rolagem Questão - Início
    if request.session.get('rolagem_questao') and request.session['rolagem_questao'].get('count') == 0:
        request.session['rolagem_questao']['count'] = 1
    elif request.session.get('rolagem_questao'):
        del request.session['rolagem_questao']
    request.session.save()
    # Rolagem Questão - Fim

    if request.method != 'GET':
        return redirect('home')
    
    provas_cabecalho = get_list_or_404(Prova)[:10]
    
    if Pedido.objects.filter(comprador__usuario=request.user).exists():
        pedido = Pedido.objects.get(comprador__usuario=request.user)
    else:
        pedido = ''

    acerto_questao = request.GET.get('acerto_questao', '')
    palavra_chave = request.GET.get('palavra_chave', '')
    disciplinas = request.GET.getlist('disciplina', '')
    anos = request.GET.getlist('ano', '')
    provas = request.GET.getlist('prova', '')
    bancas = request.GET.getlist('banca', '')
    estados = request.GET.getlist('estado', '')
    
    request.session['link_pesquisa'] = request.build_absolute_uri()
    link_pesquisa = request.session['link_pesquisa']
    request.session.save()

    link_pesquisa_navegacao = re.sub(r'&pag=\d+', '', link_pesquisa)

    choices_bancas = get_list_or_404(Banca)
    choices_estados = get_list_or_404(Estado)
    choices_disciplinas = get_list_or_404(Disciplina)
    choices_provas = get_list_or_404(Prova)
    choices_respostas = [x[0] for x in QuestaoRespondida._meta.get_field('resposta').choices]
    try:
        choices_anos = Ano.objects.order_by('-valor')
    except:
        raise Http404

    if acerto_questao or palavra_chave or disciplinas or anos or provas or bancas or estados:
        questoes = Questao.objects.filter(visibilidade=True)

        # Disciplina - Início
        _disciplinas = []
        for nome in disciplinas:
            if Disciplina.objects.filter(nome=nome).exists():
                _disciplina = Disciplina.objects.get(nome=nome)
                _disciplinas.append(_disciplina)
        disciplinas = _disciplinas

        if disciplinas:
            queries = [Q(disciplina=disciplina) for disciplina in disciplinas]
            condicao_final = reduce(or_, queries)
            questoes = questoes.filter(condicao_final)
        # Disciplina - Fim

        # Ano - Início
        _anos = []
        for valor in anos:
            if Ano.objects.filter(valor=valor).exists():
                _ano = Ano.objects.get(valor=valor)
                _anos.append(_ano)
        anos = _anos

        if anos:
            queries = [Q(ano=ano) for ano in anos]
            condicao_final = reduce(or_, queries)
            questoes = questoes.filter(condicao_final)
        # Ano - Fim

        # Prova - Início
        _provas = []
        for nome in provas:
            if Prova.objects.filter(nome=nome).exists():
                _prova = Prova.objects.get(nome=nome)
                _provas.append(_prova)
        provas = _provas

        if provas:
            queries = [Q(prova=prova) for prova in provas]
            condicao_final = reduce(or_, queries)
            questoes = questoes.filter(condicao_final)
        # Prova - Fim

        # Banca - Início
        _bancas = []
        for nome in bancas:
            if Banca.objects.filter(nome=nome).exists():
                _banca = Banca.objects.get(nome=nome)
                _bancas.append(_banca)
        bancas = _bancas

        if bancas:
            queries = [Q(banca=banca) for banca in bancas]
            condicao_final = reduce(or_, queries)
            questoes = questoes.filter(condicao_final)
        # Banca - Fim
            
        # Estado - Início
        _estados = []
        for nome in estados:
            if Estado.objects.filter(nome=nome).exists():
                _estado = Estado.objects.get(nome=nome)
                _estados.append(_estado)
        estados = _estados

        if estados:
            queries = [Q(estado=estado) for estado in estados]
            condicao_final = reduce(or_, queries)
            questoes = questoes.filter(condicao_final)
        # Estado - Fim
            
        if palavra_chave:
            questoes = questoes.filter(texto__icontains=palavra_chave)

        qtd_questoes = len(questoes)
        # Paginação - Início
        paginator = Paginator(questoes, 10)
        page = request.GET.get('pag', 1)
        page_obj = paginator.get_page(page)
        # print(page_obj, page_obj[0])
        # Paginação - Fim

        respostas = []
        _questoes = []
        for questao in page_obj:
            if not QuestaoRespondida.objects.filter(usuario=request.user, questao=questao).exists():
                resposta = 'Pendente'
            else:
                resposta = QuestaoRespondida.objects.get(usuario=request.user, questao=questao).resposta

            if acerto_questao == resposta:
                _questoes.append(questao)

                if resposta == 'Acertei':
                    respostas.append(1)
                elif resposta == 'Errei':
                    respostas.append(-1)
                elif resposta == 'Pendente':
                    respostas.append(0)

            if acerto_questao == 'Todas':
                if resposta == 'Acertei':
                    respostas.append(1)
                elif resposta == 'Errei':
                    respostas.append(-1)
                elif resposta == 'Pendente':
                    respostas.append(0)

        if acerto_questao != 'Todas':
            questoes = _questoes
        else:
            questoes = page_obj

        questoes_zip = zip(questoes, respostas)

        return render(request, 'questoes.html', {
            'questoes_zip': questoes_zip,
            'qtd': qtd_questoes,
            'link_pesquisa': link_pesquisa,
            'link_pesquisa_navegacao': link_pesquisa_navegacao,
            'choices_disciplinas': choices_disciplinas,
            'choices_anos': choices_anos,
            'choices_provas': choices_provas,
            'choices_respostas': choices_respostas,
            'choices_bancas': choices_bancas,
            'choices_estados': choices_estados,
            'provas_cabecalho': provas_cabecalho,
            'pedido': pedido,
            'page_obj': page_obj,
        })

    return render(request, 'questoes.html', {
        'link_pesquisa': link_pesquisa,
        'choices_disciplinas': choices_disciplinas,
        'choices_anos': choices_anos,
        'choices_provas': choices_provas,
        'choices_respostas': choices_respostas,
        'choices_bancas': choices_bancas,
        'choices_estados': choices_estados,
        'provas_cabecalho': provas_cabecalho,
        'pedido': pedido,
    })


def responder_questao(request, id):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    _redirect = verify_acess_questions(request)
    if _redirect:
        return redirect(_redirect)

    if request.method != 'POST' or not Questao.objects.filter(id=id).exists():
        return redirect('questoes')
    
    _questao = Questao.objects.get(id=id)

    if (QuestaoRespondida.objects.filter(usuario=request.user, questao=_questao, resposta='Acertei').exists() or 
        QuestaoRespondida.objects.filter(usuario=request.user, questao=_questao, resposta='Errei').exists()):
        messages.error(request, f'Você já respondeu a questão: "{_questao.codigo}"')
        return redirect(http_referer)

    alternativa = request.POST.get('alternativa', '')

    if not alternativa:
        messages.error(request, f'A questão: {_questao.codigo} Escolha uma alternativa!')
        return redirect(http_referer)
    else:
        if 'Correto' in alternativa:
            alternativa = 'Correto'
        elif 'Errado' in alternativa:
            alternativa = 'Errado'
        else:
            alternativa = alternativa[0]
    
    questao_respondida = QuestaoRespondida(usuario=request.user, questao=_questao)

    if _questao.gabarito_alternativa == alternativa:
        questao_respondida.resposta = 'Acertei'
    else:
        questao_respondida.resposta = 'Errei'
    questao_respondida.save()

    if questao_respondida.resposta == 'Errei':
        messages.error(request, f'Você errou a questão: "{_questao.codigo}"')
    elif  questao_respondida.resposta == 'Acertei':
        messages.success(request, f'Você acertou a questão: "{_questao.codigo}"')

    request.session['rolagem_questao'] = {
        'id': f'#questao_{_questao.codigo}',
        'count': 0,
    }
    request.session.save()
    return redirect(http_referer.replace('Pendente', 'Todas'))

def questao(request, codigo):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )
    
    _redirect = verify_acess_questions(request)
    if _redirect:
        return redirect(_redirect)

    provas_cabecalho = get_list_or_404(Prova)[:10]

    if not Questao.objects.filter(codigo=codigo).exists():
        return redirect('questoes')
    
    questao = Questao.objects.get(codigo=codigo)

    if request.session.get('link_pesquisa'):
        link_anterior = request.session['link_pesquisa']
    else:
        link_anterior = redirect('questoes')

    comentarios = Comentarios.objects.filter(questao=questao, visibilidade=True)

    duvidas = Duvidas.objects.filter(questao=questao, visibilidade=True)
    respostas = []
    for duvida in duvidas:
        if Respostas.objects.filter(duvida=duvida, visibilidade=True).exists():
            resposta = Respostas.objects.get(duvida=duvida, visibilidade=True)
            respostas.append(resposta)
        else:
            respostas.append(False)

    if (QuestaoRespondida.objects.filter(usuario=request.user, questao=questao, resposta='Acertei').exists() or 
        QuestaoRespondida.objects.filter(usuario=request.user, questao=questao, resposta='Errei').exists()):
        questao_respondida = QuestaoRespondida.objects.get(usuario=request.user, questao=questao)
        resposta = 1 if questao_respondida.resposta == 'Acertei' else -1
        return render(request, 'questao.html', {
            'questao': questao,
            'resposta': resposta,
            'link_anterior': link_anterior,
            'comentarios': comentarios,
            'duvidas_respostas': list(zip(duvidas, respostas)),
            'provas_cabecalho': provas_cabecalho,
        })

    if request.method != 'POST':
        return render(request, 'questao.html', {
            'questao': questao,
            'link_anterior': link_anterior,
            'comentarios': comentarios,
            'duvidas_respostas': list(zip(duvidas, respostas)),
            'provas_cabecalho': provas_cabecalho,
        })
    
    alternativa = request.POST.get('alternativa', '')

    if not alternativa:
        messages.error(request, 'Escolha uma alternativa!')
        return render(request, 'questao.html', {
            'questao': questao,
            'link_anterior': link_anterior,
            'comentarios': comentarios,
            'duvidas_respostas': list(zip(duvidas, respostas)),
            'provas_cabecalho': provas_cabecalho,
        })
    
    questao_respondida = QuestaoRespondida(usuario=request.user, questao=questao)

    if questao.gabarito_alternativa == alternativa:
        questao_respondida.resposta = 'Acertei'
        questao_respondida.save()
        return render(request, 'questao.html', {
            'questao': questao,
            'sucesso': 1,
            'link_anterior': link_anterior,
            'comentarios': comentarios,
            'duvidas_respostas': list(zip(duvidas, respostas)),
            'provas_cabecalho': provas_cabecalho,
        })
    
    questao_respondida.resposta = 'Errei'
    questao_respondida.save()

    return render(request, 'questao.html', {
        'questao': questao,
        'sucesso': -1,
        'link_anterior': link_anterior,
        'comentarios': comentarios,
        'duvidas_respostas': list(zip(duvidas, respostas)),
        'provas_cabecalho': provas_cabecalho,
    })


def refazer_questao(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('questoes')
	)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if Perfil.objects.filter(verificacao_email=False, usuario=request.user).exists() or not Perfil.objects.filter(usuario=request.user).exists():
        return redirect('perfil')
    
    if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
        messages.error(request, 'Você não tem um plano ativo. Contrate um para desfrutar do nosso gigantesco banco de questões e aulas!')
        return redirect('perfil')

    if not Questao.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    questao = Questao.objects.get(visibilidade=True, id=id)

    if not QuestaoRespondida.objects.filter(usuario=request.user, questao=questao).exists():
        return redirect(http_referer)
    
    questao_respondida = QuestaoRespondida.objects.get(usuario=request.user, questao=questao)
    questao_respondida.delete()

    request.session['rolagem_questao'] = {
        'id': f'#questao_{questao.codigo}',
        'count': 0,
    }
    request.session.save()

    messages.info(request, f'Pronto, agora você pode refazer a questão: "{questao.codigo}"!')
    return redirect(http_referer)
    

def refazer_questao_2(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('questoes')
	)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if Perfil.objects.filter(verificacao_email=False, usuario=request.user).exists() or not Perfil.objects.filter(usuario=request.user).exists():
        return redirect('perfil')
    
    if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
        messages.error(request, 'Você não tem um plano ativo. Contrate um para desfrutar do nosso gigantesco banco de questões e aulas!')
        return redirect('perfil')

    if not Questao.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    questao = Questao.objects.get(visibilidade=True, id=id)

    if not QuestaoRespondida.objects.filter(usuario=request.user, questao=questao).exists():
        return redirect(http_referer)
    
    questao_respondida = QuestaoRespondida.objects.get(usuario=request.user, questao=questao)
    questao_respondida.delete()

    request.session['rolagem_questao'] = {
        'id': f'#questao_{questao.codigo}',
        'count': 0,
    }
    request.session.save()

    messages.info(request, f'Pronto, agora você pode refazer a questão: "{questao.codigo}"!')
    return redirect(http_referer.replace('Errei', 'Todas').replace('Acertei', 'Todas').replace('Pendente', 'Todas'))


def enviar_comentario(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('questoes')
	)

    if not request.user.is_authenticated:
        return redirect('login')
    
    if Perfil.objects.filter(verificacao_email=False, usuario=request.user).exists() or not Perfil.objects.filter(usuario=request.user).exists():
        return redirect('perfil')
    
    if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
        messages.error(request, 'Você não tem um plano ativo. Contrate um para desfrutar do nosso gigantesco banco de questões e aulas!')
        return redirect('perfil')
    
    if request.method != 'POST':
        return redirect(http_referer)
    
    texto = request.POST.get('comentario')

    if not Questao.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    _questao = Questao.objects.get(visibilidade=True, id=id)

    comentario = Comentarios.objects.create(usuario=request.user, texto=texto, questao=_questao)
    comentario.save()

    messages.info(request, 'O seu comentário foi publicado com sucesso!')
    return redirect(http_referer)
    

def enviar_duvida(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('questoes')
	)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if Perfil.objects.filter(verificacao_email=False, usuario=request.user).exists() or not Perfil.objects.filter(usuario=request.user).exists():
        return redirect('perfil')
    
    if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
        messages.error(request, 'Você não tem um plano ativo. Contrate um para desfrutar do nosso gigantesco banco de questões e aulas!')
        return redirect('perfil')
    
    if request.method != 'POST':
        return redirect(http_referer)
    
    texto = request.POST.get('duvida')
    arquivo = request.FILES.get('duvida_imagem')

    if not Questao.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    _questao = Questao.objects.get(visibilidade=True, id=id)

    duvida = Duvidas.objects.create(usuario=request.user, texto=texto, questao=_questao, arquivo=arquivo)
    duvida.save()

    messages.info(request, 'A sua dúvida foi publicada com sucesso. Em breve, você será respondido!')
    return redirect(http_referer)


def enviar_duvida_professor(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('questoes')
	)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if Perfil.objects.filter(verificacao_email=False, usuario=request.user).exists() or not Perfil.objects.filter(usuario=request.user).exists():
        return redirect('perfil')
    
    if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
        messages.error(request, 'Você não tem um plano ativo. Contrate um para desfrutar do nosso gigantesco banco de questões e aulas!')
        return redirect('perfil')
    
    if request.method != 'POST':
        return redirect(http_referer)
    
    texto = request.POST.get('duvida_professor')
    arquivo = request.FILES.get('duvida_imagem_professor')

    if not Questao.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    _questao = Questao.objects.get(visibilidade=True, id=id)

    duvida = Duvidas.objects.create(usuario=request.user, texto=texto, questao=_questao, arquivo=arquivo)
    duvida.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/email_reportar_duvidas_professor.html', 
    {'usuario': request.user, 'email': request.user.email, 'data': duvida.data, 'duvida': duvida,})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Nova Dúvida - GMP University', text_content, 
    settings.EMAIL_HOST_USER, ['gmplibraryinfo@gmail.com'])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    messages.info(request, 'A sua dúvida foi reportada ao professor. Verifique o seu e-mail para visualizar a resposta em breve!')
    return redirect(http_referer)


def aulas(request):
    _redirect = verify_acess_questions(request)
    if _redirect:
        return redirect(_redirect)
    
    if request.method != 'GET':
        return redirect('home')
    
    choices_disciplinas = get_list_or_404(Disciplina)
    provas_cabecalho = get_list_or_404(Prova)[:10]
    
    if Pedido.objects.filter(comprador__usuario=request.user).exists():
        pedido = Pedido.objects.get(comprador__usuario=request.user)
    else:
        pedido = ''
    
    palavra_chave = request.GET.get('palavra_chave', '')
    disciplinas = request.GET.getlist('disciplina', '')

    aulas = Aula.objects.filter(visibilidade=True)

    request.session['link_pesquisa'] = request.build_absolute_uri()
    link_pesquisa = request.session['link_pesquisa']
    request.session.save()
    link_pesquisa_navegacao = re.sub(r'&pag=\d+', '', link_pesquisa)
    # link_pesquisa_navegacao = re.sub(r'\?pag=\d+', '', link_pesquisa_navegacao)

    if not request.GET:
        return render(request, 'aulas.html', {
            'aulas': aulas,
            'choices_disciplinas': choices_disciplinas,
            'provas_cabecalho': provas_cabecalho,
            'pedido': pedido,
        })

    if palavra_chave or disciplinas:
        # Disciplina - Início
        _disciplinas = []
        for nome in disciplinas:
            if Disciplina.objects.filter(nome=nome).exists():
                _disciplina = Disciplina.objects.get(nome=nome)
                _disciplinas.append(_disciplina)
        disciplinas = _disciplinas

        if disciplinas:
            queries = [Q(disciplina=disciplina) for disciplina in disciplinas]
            condicao_final = reduce(or_, queries)
            aulas = aulas.filter(condicao_final)
        # Disciplina - Fim

        if palavra_chave:
            aulas = aulas.filter(Q(nome__icontains=palavra_chave) | Q(descricao__icontains=palavra_chave))
    
    if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
        aulas = aulas[:1]

    paginator = Paginator(aulas, 5)
    page = request.GET.get('pag', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'aulas.html', {
        'aulas': aulas,
        'page_obj': page_obj,
        'qtd': len(aulas),
        'choices_disciplinas': choices_disciplinas,
        'provas_cabecalho': provas_cabecalho,
        'pedido': pedido,
        'link_pesquisa_navegacao': link_pesquisa_navegacao,
    })
    


def redirecionamento_aulas(request, disciplina: str):
    disciplina_formatada = disciplina.replace(' ', '+')
    return redirect(f'{DOMINIO}/aulas/?disciplina={disciplina_formatada}')

def redirecionamento_questoes(request, prova: str):
    if prova == 'Todas':
        return redirect(f'{DOMINIO}/questoes/?acerto_questao={prova}')
    prova_formatada = prova.replace(' ', '+')
    return redirect(f'{DOMINIO}/questoes/?prova={prova_formatada}')

def redirecionamento_questoes_form(request):
    if request.method == 'GET':
        
        if not request.user.is_authenticated:
            messages.error(request, 'Faça o login para poder acessar as questões!')
            return redirect('login')
        
        if Perfil.objects.filter(verificacao_email=False, usuario=request.user).exists() or not Perfil.objects.filter(usuario=request.user).exists():
            messages.error(request, 'O seu e-mail ainda não foi verificado!')
            return redirect('perfil')
        
        if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
            messages.error(request, 'Você não tem um plano ativo. Contrate um para desfrutar do nosso gigantesco banco de questões e aulas!')
            return redirect('perfil')
        
        search = request.GET.get('search', '')

        choices_provas = get_list_or_404(Prova)
        for choice_prova in choices_provas:
            nome_prova = choice_prova.nome
            if nome_prova in search:
                nome_prova: str = nome_prova.replace(' ', '+')
                return redirect(f'{DOMINIO}/questoes/?prova={nome_prova}')
        messages.error(request, f'Nada foi encontrado com esse termo: {search}')
        return redirect(f'{DOMINIO}/questoes/')
    else:
        return redirect('home')