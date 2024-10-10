from django.shortcuts import render, redirect, reverse, get_list_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from perfil.models import Perfil, RecuperacaoSenha, Planos, Pedido
from questoes.models import Prova
from django.core.validators import validate_email
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string	
from django.utils.html import strip_tags			
from django.conf import settings
import requests
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta
from questoes.models import Disciplina, Questao, QuestaoRespondida

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def perfil(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        return redirect('home')

    perfil = Perfil.objects.get(usuario=request.user)

    if Pedido.objects.filter(comprador=perfil).exists():
        pedido = Pedido.objects.get(
            comprador=perfil,
        )
    else:
        pedido = ''

    choices_disciplinas = get_list_or_404(Disciplina)
    provas_cabecalho = get_list_or_404(Prova)[:10]

    # Métricas Gerais (MG) - Início
    
    mg_numero_questoes = len(Questao.objects.filter(visibilidade=True))
    mg_numero_questoes_feitas = 0
    mg_acertos = 0
    mg_erros = 0
    for questao_respondida in QuestaoRespondida.objects.filter(usuario=request.user):
        mg_numero_questoes_feitas+=1
        if questao_respondida.resposta == 'Acertei':
            mg_acertos+=1
        elif questao_respondida.resposta == 'Errei':
            mg_erros+=1

    if mg_numero_questoes:
        porcentagem_geral = round(mg_numero_questoes_feitas / mg_numero_questoes * 100, 2)
    else:
        porcentagem_geral = 0

    if mg_numero_questoes_feitas:
        mg_aproveitamento = round(mg_acertos / mg_numero_questoes_feitas * 100, 2)
    else:
        mg_aproveitamento = 0

    metricas_gerais = {
        'numero_questoes': mg_numero_questoes,
        'numero_questoes_feitas': mg_numero_questoes_feitas,
        'porcentagem_geral': porcentagem_geral,
        'acertos': mg_acertos,
        'erros': mg_erros,
        'aproveitamento': mg_aproveitamento,
    }

    # Métricas Gerais (MG) - Fim

    if request.method != 'POST':
        return render(request, 'perfil.html', {
            'perfil': perfil, 
            'provas_cabecalho': provas_cabecalho, 
            'choices_disciplinas': choices_disciplinas, 
            'pedido': pedido,
            'metricas_gerais': metricas_gerais,
        })
    
    # Métricas Disciplinas - Início
    disciplina = request.POST.get('disciplina', '')

    if not Disciplina.objects.filter(nome=disciplina).exists():
        messages.error(request, f'A disciplina enviada não existe. Por favor, falar com o suporte!')
        return render(request, 'perfil.html', {
            'perfil': perfil, 
            'provas_cabecalho': provas_cabecalho, 
            'choices_disciplinas': choices_disciplinas, 
            'pedido': pedido,
            'metricas_gerais': metricas_gerais,
        })

    disciplina = Disciplina.objects.get(nome=disciplina)

    numero_questoes_disciplina = len(Questao.objects.filter(disciplina=disciplina, visibilidade=True))
    numero_questoes_feitas = 0
    acertos = 0
    erros = 0
    for questao_respondida in QuestaoRespondida.objects.filter(usuario=request.user):
        questao = questao_respondida.questao
        if questao.disciplina == disciplina:
            numero_questoes_feitas+=1
            if questao_respondida.resposta == 'Acertei':
                acertos+=1
            elif questao_respondida.resposta == 'Errei':
                erros+=1

    if numero_questoes_disciplina:
        numero_questoes_porcentagem = round(numero_questoes_feitas / numero_questoes_disciplina * 100, 2)
    else:
        numero_questoes_porcentagem = 0

    if numero_questoes_feitas:
        aproveitamento = round(acertos / numero_questoes_feitas * 100, 2)
    else:
        aproveitamento = 0

    metricas_disciplinas = {
        'nome_disciplina': disciplina.nome,
        'numero_questoes_disciplina': numero_questoes_disciplina,
        'numero_questoes_feitas': numero_questoes_feitas,
        'numero_questoes_porcentagem': numero_questoes_porcentagem,
        'acertos': acertos,
        'erros': erros,
        'aproveitamento': aproveitamento,
    }

    # Métricas Disciplinas - Fim
    
    messages.success(request, f'As suas métricas sobre a disciplina: "{disciplina.nome}" estão exibidas embaixo.')
    return render(request, 'perfil.html', {
        'perfil': perfil, 
        'provas_cabecalho': provas_cabecalho, 
        'choices_disciplinas': choices_disciplinas,
        'metricas_disciplinas': metricas_disciplinas,
        'pedido': pedido,
        'metricas_gerais': metricas_gerais,
    })



def login(request):
    if request.user.is_authenticated:
        return redirect('questoes')
    
    provas_cabecalho = get_list_or_404(Prova)[:10]
    
    if request.method != 'POST':
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not email or not senha:
        messages.error(request, 'Os campos não podem ficar vazios')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    if not User.objects.filter(email=email).exists():
        messages.error(request, 'O E-mail informado não está atrelado a nenhuma conta!')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    username = User.objects.get(email=email).username

    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    # Final - Recaptcha

    user = auth.authenticate(request, username=username, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    auth.login(request, user)

    if Perfil.objects.filter(usuario=user, verificacao_email=False).exists():
        messages.error(request, 'O seu e-mail ainda não foi verificado.')
        return redirect('perfil')
    else:
        return redirect('questoes')



def registro(request):
    if request.user.is_authenticated:
        return redirect('questoes')
    
    provas_cabecalho = get_list_or_404(Prova)[:10]
    
    if request.method != 'POST':
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    name = request.POST.get('name')
    user = request.POST.get('user')
    email = request.POST.get('email')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    foto = request.FILES.get('foto')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not name or not user or not email or not senha1 or not senha2:
        messages.error(request, 'Os campos não podem ficar vazios!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    if len(user) < 4:
        messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    if len(senha1) < 8:
        messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    if senha1 != senha2:
        messages.error(request, 'As senhas tem que ser iguais!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail cadastrado já existe!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    if User.objects.filter(username=user).exists():
        messages.error(request, 'O usuário cadastrado já existe!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    # Final - Recaptcha
    
    user = User.objects.create(username=user, first_name=name, email=email, password=senha1)
    user.save()
    auth.login(request, user)

    # Gerando Código - Início
    letras = string.ascii_letters
    digitos = string.digits
    # caracteres = '!@#$%&*._-'

    geral = letras + digitos
    while True:
        codigo = ''.join(random.choices(geral, k=25))
        if not Perfil.objects.filter(codigo=codigo).exists():
            break
    # Gerando Código - Fim

    perfil = Perfil.objects.get(usuario=user)
    perfil.codigo = codigo
    if foto:
        perfil.foto = foto
    perfil.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/confirmacao_email.html', 
    {'nome': user.first_name, 'link': f'{settings.DOMINIO}/perfil/confirmacao_email/{codigo}/'})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Confirmação de E-mail - GMP University', text_content, 
    settings.EMAIL_HOST_USER, [email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim
    
    messages.info(request, 'Cadastrado com sucesso! Mas antes, precisamos confirmar a sua conta.')
    messages.info(request, 'Verifique o seu e-mail e clique no link. Se não achar, vá na caixa de spam.')
    return redirect('perfil')


def alterar_dados(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    provas_cabecalho = get_list_or_404(Prova)[:10]

    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'Você está sem perfil. Fale com o suporte!')
        return redirect('perfil')
    
    _perfil = Perfil.objects.get(usuario=request.user)
    
    if request.method != 'POST':
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'perfil': _perfil,
        })

    name = request.POST.get('name')
    username = request.POST.get('user')
    email = request.POST.get('email')
    foto = request.FILES.get('foto')
    excluir_foto = request.POST.get('excluir_foto')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not name or not username or not email:
        messages.error(request, 'Os campos não podem ficar vazios!')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'perfil': _perfil,
        })
    
    if len(username) < 4:
        messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'perfil': _perfil,
        })
    
    if email != request.user.email and  User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail cadastrado já existe!')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'perfil': _perfil,
        })
    
    if username != request.user.username and  User.objects.filter(username=username).exists():
        messages.error(request, 'O usuário cadastrado já existe!')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'perfil': _perfil,
        })
    
    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'perfil': _perfil,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'perfil': _perfil,
        })
    # Final - Recaptcha
    
    user = User.objects.get(username=username)
    user.first_name = name
    user.email = email
    user.username = username
    user.save()
    if excluir_foto == 'Sim' and _perfil.foto:
        _perfil.foto = None
    elif foto:
        _perfil.foto = foto
    _perfil.save()

    messages.success(request, 'Dados trocados com sucesso!')
    return redirect('perfil')


def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return redirect('perfil')
    
    auth.logout(request)
    messages.success(request, 'Usuário desconectado!')
    return redirect('login')


def pedir_confirmacao_email(request):
   if not request.user.is_authenticated:
        return redirect('login')
   
   if not Perfil.objects.filter(usuario=request.user, verificacao_email=False).exists():
        return redirect('perfil')
   
   # Gerando Código - Início
   letras = string.ascii_letters
   digitos = string.digits
   # caracteres = '!@#$%&*._-'

   geral = letras + digitos
   while True:
        codigo = ''.join(random.choices(geral, k=25))
        if not Perfil.objects.filter(codigo=codigo).exists():
            break
   # Gerando Código - Fim

   perfil = Perfil.objects.get(usuario=request.user)
   perfil.codigo = codigo
   perfil.save()

   # Enviando E-mail - Início
   html_content = render_to_string('emails/confirmacao_email.html', 
   {'nome': request.user.first_name, 'link': f'{settings.DOMINIO}/perfil/confirmacao_email/{codigo}/'})
   text_content = strip_tags(html_content)

   _email = EmailMultiAlternatives('Confirmação de E-mail - GMP University', text_content, 
   settings.EMAIL_HOST_USER, [request.user.email])
   _email.attach_alternative(html_content, 'text/html')
   _email.send()
   # Enviando E-mail - Fim

   messages.info(request, 'Verifique o seu e-mail e clique no link. Se não achar, vá na caixa de spam.')
   return redirect('perfil')
   

def esqueceu_senha(request):
    if request.user.is_authenticated:
        return redirect('perfil')
    
    provas_cabecalho = get_list_or_404(Prova)[:10]
    
    if request.method != 'POST':
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    email = request.POST.get('email')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail enviado NÃO está atrelado a nenhuma conta!')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    user = User.objects.get(email=email)

    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    # Final - Recaptcha

    # Gerando Código - Início
    letras = string.ascii_letters
    digitos = string.digits
    # caracteres = '!@#$%&*._-'

    geral = letras + digitos

    while True:
        codigo = ''.join(random.choices(geral, k=25))
        if not RecuperacaoSenha.objects.filter(codigo=codigo).exists():
            break
    # Gerando Código - Fim

    recuperacao = RecuperacaoSenha.objects.create(usuario=user, codigo=codigo)
    recuperacao.save()
    
    # Enviando E-mail - Início
    html_content = render_to_string('emails/esqueceu_senha_email.html', 
    {'nome': user.first_name, 'link': f'{settings.DOMINIO}/perfil/recuperacao_senha/{codigo}/'})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Confirmação de E-mail - GMP University', text_content, 
    settings.EMAIL_HOST_USER, [email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    messages.info(request, 'Enviamos um link para o seu e-mail. Acesse ele para você poder trocar a sua senha com segurança.')
    messages.info(request, 'Verifique o seu e-mail e clique no link. Se não achar, vá na caixa de spam.')
    return render(request, 'esqueceu_senha.html', {
        'validador': True,
        'provas': provas_cabecalho,
    })
    

def recuperacao_senha(request, codigo):
    if request.user.is_authenticated:
        messages.info(request, 'Você está logado. Saia para poder trocar a senha.')
        return redirect('perfil')
    
    if not RecuperacaoSenha.objects.filter(codigo=codigo).exists() or not RecuperacaoSenha.objects.filter(codigo=codigo, recuperacao=False).exists():
        return redirect('home')
    
    recuperacao = RecuperacaoSenha.objects.get(codigo=codigo)

    provas_cabecalho = get_list_or_404(Prova)[:10]
    
    if request.method != 'POST':
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
            'provas': provas_cabecalho,
        })
    
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not senha1 or not senha2:
        messages.error(request, 'Os campos não podem ficar vazios!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
            'provas': provas_cabecalho,
        })

    if len(senha1) < 8:
        messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
            'provas': provas_cabecalho,
        })
    
    if senha1 != senha2:
        messages.error(request, 'As senhas tem que ser iguais!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
            'provas': provas_cabecalho,
        })
    
    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
            'provas': provas_cabecalho,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
            'provas': provas_cabecalho,
        })
    # Final - Recaptcha

    recuperacao.usuario.set_password(senha1)
    recuperacao.usuario.save()

    recuperacao.recuperacao = True
    recuperacao.save()

    messages.success(request, f'A senha de: "{recuperacao.usuario}" foi trocada!')
    return redirect('login')


def confirmar_email(request, codigo):
    if not Perfil.objects.filter(codigo=codigo).exists():
        return redirect('home')

    perfil = Perfil.objects.get(codigo=codigo)
    perfil.verificacao_email = True
    perfil.save()

    messages.success(request, 'Parabéns, a sua conta foi verificada com sucesso!')
    return redirect('questoes')


# Gerenciamento e Pagamento Assinaturas - Início

def escolher_plano(request, plano):
    request.session['plano'] = plano
    return redirect(f'{settings.DOMINIO}/perfil/registro_pagamento/registro/')

def registro_pagamento(request, situation):
    if request.user.is_authenticated:
        return redirect('payment')
    elif request.session.get('dados'):
        provas = get_list_or_404(Prova)

        if request.method != 'POST':
            return render(request, 'registro_pagamento.html', {
                'validador': True,
                'provas': provas,
            })
    
        codigo = request.POST.get('codigo')
        gerar_outro_codigo = request.POST.get('gerar_outro_codigo')

        if not codigo and (not gerar_outro_codigo or gerar_outro_codigo == 'nao'):
            messages.error(request, 'O campo do código não pode ficar vazio!')
            return render(request, 'registro_pagamento.html', {
                'validador': True,
                'provas': provas,
            })
        
        if gerar_outro_codigo == 'sim':
            # Gerando Código - Início
            letras = string.ascii_letters
            digitos = string.digits
            # caracteres = '!@#$%&*._-'

            geral = letras + digitos
            while True:
                codigo = ''.join(random.choices(geral, k=25))
                if not Perfil.objects.filter(codigo=codigo).exists():
                    break
            # Gerando Código - Fim

            perfil = Perfil.objects.get(usuario=request.user)
            perfil.codigo = codigo
            perfil.save()

            # Enviando E-mail - Início
            html_content = render_to_string('emails/confirmacao_email_pagamento.html', 
            {'nome': request.user.first_name, 'codigo': codigo})
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives('Confirmação de E-mail - GMP University', text_content, 
            settings.EMAIL_HOST_USER, [request.user.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim

            messages.info(request, 'Geramos outro código!')
            messages.info(request, 'Verifique o seu e-mail, copie o link e cole aqui embaixo. Se não achar, vá na caixa de spam.')
            request.session['dados'] = {
                'email': perfil.usuario.email,
                'username': perfil.usuario.first_name,
            }
            request.session.save()
            validador = True
            return render(request, 'registro_pagamento.html', {
                'validador': validador,
                'provas': provas,
            })

        if Perfil.objects.filter(usuario=request.user, codigo=codigo).exists():
            perfil = Perfil.objects.get(usuario=request.user, codigo=codigo)
            perfil.verificacao_email = True
            perfil.save()

            del request.session['dados']
            request.session.save()

            return redirect('payment')
        else:
            messages.error(request, 'O código abaixo é inválido. Verifique se você copiou o código certo ou gere outro código, abertando no botão abaixo')
            return render(request, 'registro_pagamento.html', {
                'validador': True,
                'provas': provas,
            })

    elif situation == 'registro':
        if request.user.is_authenticated:
            auth.logout(request)

        provas = get_list_or_404(Prova)

        if request.method != 'POST':
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        name = request.POST.get('name')
        user = request.POST.get('user')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        foto = request.FILES.get('foto')
        recaptcha = request.POST.get('g-recaptcha-response')

        if not name or not user or not email or not senha1 or not senha2:
            messages.error(request, 'Os campos não podem ficar vazios!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })
        
        if len(user) < 4:
            messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        if len(senha1) < 8:
            messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })
        
        if senha1 != senha2:
            messages.error(request, 'As senhas tem que ser iguais!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'O e-mail cadastrado já existe!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })
        
        if User.objects.filter(username=user).exists():
            messages.error(request, 'O usuário cadastrado já existe!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })
        
        # Início - Recaptcha
        if not recaptcha:
            messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_BACK,
                'response': recaptcha
            }
        )

        recaptcha_result = recaptcha_request.json()

        if not recaptcha_result.get('success'):
            messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })
        # Final - Recaptcha
        
        user = User.objects.create(username=user, first_name=name, email=email, password=senha1)
        user.save()
        auth.login(request, user)

        # Gerando Código - Início
        letras = string.ascii_letters
        digitos = string.digits
        # caracteres = '!@#$%&*._-'

        geral = letras + digitos
        while True:
            codigo = ''.join(random.choices(geral, k=25))
            if not Perfil.objects.filter(codigo=codigo).exists():
                break
        # Gerando Código - Fim

        perfil = Perfil.objects.get(usuario=user)
        perfil.codigo = codigo
        if foto:
            perfil.foto = foto
        perfil.save()

        # Enviando E-mail - Início
        html_content = render_to_string('emails/confirmacao_email_pagamento.html', 
        {'nome': user.first_name, 'codigo': codigo})
        text_content = strip_tags(html_content)

        _email = EmailMultiAlternatives('Confirmação de E-mail - GMP University', text_content, 
        settings.EMAIL_HOST_USER, [email])
        _email.attach_alternative(html_content, 'text/html')
        _email.send()
        # Enviando E-mail - Fim

        messages.info(request, 'Cadastrado com sucesso! Mas antes, precisamos confirmar a sua conta.')
        messages.info(request, 'Verifique o seu e-mail, copie o link e cole aqui embaixo. Se não achar, vá na caixa de spam.')
        request.session['dados'] = {
            'email': email,
            'username': perfil.usuario.first_name,
        }
        request.session.save()
        validador = True
        return render(request, 'registro_pagamento.html', {
            'validador': validador,
            'provas': provas,
        })

    else:
        if request.user.is_authenticated:
            auth.logout(request)

        provas = get_list_or_404(Prova)

        if request.method != 'POST':
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        email = request.POST.get('email')
        senha = request.POST.get('senha')
        recaptcha = request.POST.get('g-recaptcha-response')

        if not email or not senha:
            messages.error(request, 'Os campos não podem ficar vazios')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        if not User.objects.filter(email=email).exists():
            messages.error(request, 'O E-mail informado não está atrelado a nenhuma conta!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        username = User.objects.get(email=email).username

        # Início - Recaptcha
        if not recaptcha:
            messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_BACK,
                'response': recaptcha
            }
        )

        recaptcha_result = recaptcha_request.json()

        if not recaptcha_result.get('success'):
            messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })
        # Final - Recaptcha

        user = auth.authenticate(request, username=username, password=senha)

        if not user:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'registro_pagamento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas,
            })

        auth.login(request, user)

        if Perfil.objects.filter(usuario=user, verificacao_email=False).exists():
            messages.error(request, 'O seu e-mail ainda não foi verificado.')
            request.session['dados'] = {
                'email': email,
                'username': username,
            }
            request.session.save()
            validador = True
            return render(request, 'registro_pagamento.html', {
                'validador': True,
                'provas': provas,
            })
        else:
            return redirect('payment')



def payment(request):
    if not request.user.is_authenticated:
        return redirect(f'{settings.DOMINIO}/perfil/registro_pagamento/registro/')

    provas = get_list_or_404(Prova)

    if not Planos.objects.all().exists():
        messages.error(request, 'Nenhum plano foi cadastrado ainda!')
        return render(request, 'payment.html', {'planos': planos, 'provas': provas,})
    
    if Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists():
        messages.error(request, 'Você já possui um plano ativo!')
        return redirect('perfil')

    planos = Planos.objects.all()

    if request.method != 'POST':
        return render(request, 'payment.html', {'planos': planos, 'provas': provas,})
    
    plano = request.POST.get('plano', '')

    if not plano:
        messages.error(request, 'Selecione um plano!')
        return render(request, 'payment.html', {'planos': planos, 'provas': provas,})

    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'O seu perfil foi excluído. Por favor, fale com o suporte!')
        return render(request, 'payment.html', {'planos': planos, 'provas': provas,})
    
    perfil = Perfil.objects.get(usuario=request.user)

    # url = "https://sandbox.asaas.com/api/v3/paymentLinks"
    url = "https://asaas.com/api/v3/paymentLinks"

    try:
        if plano == 'intermediario':
            plano_preco = Planos.objects.get(tipo='intermediario').preco
        elif plano == 'avancado':
            plano_preco = Planos.objects.get(tipo='avancado').preco
        else:
            plano_preco = Planos.objects.get(tipo='basico').preco
    except:
        messages.error(request, 'Houve algum erro nos planos. Por favor, fale com o suporte!')
        return render(request, 'payment.html', {'planos': planos, 'provas': provas,})

    data_atual = datetime.now(timezone('America/Sao_Paulo'))
    relative_delta = relativedelta(days=1)
    data_validade = data_atual + relative_delta

    dia = data_validade.strftime('%d')
    mes = data_validade.strftime('%m')
    ano = data_validade.strftime('%Y')
    data_formatada = f'{ano}-{mes}-{dia}'
    # return HttpResponse(data_formatada)

    payload = {
        "billingType": "UNDEFINED",
        "chargeType": "RECURRENT",
        "callback": {
            "successUrl": f"https://ggmpacademy.com.br/perfil/sucesso/",
            "autoRedirect": True
        },
        "name": f"GMP University",
        "description": f"GMP University - Plano: {plano} - usuário: {perfil.usuario}",
        "endDate": data_formatada,
        "value": plano_preco,
        "dueDateLimitDays": 3,
        "subscriptionCycle": "MONTHLY",
        "notificationEnabled": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": settings.KEY_API,
    }

    response = dict(requests.post(url, json=payload, headers=headers).json())

    descricao = f"GMP University - Plano: {plano} - usuário: {perfil.usuario}",
    try:
        url_payment = response['url']
        idPagamento = response['id']
    except:
        url_payment = 'vazio'
        idPagamento = 'vazio'

    if not Pedido.objects.filter(comprador=perfil).exists():
        pedido = Pedido.objects.create(
            comprador=perfil,
            preco_pedido=plano_preco,
            endDate=data_formatada,
            plano=plano,
            link_pagamento=url_payment,
            descricao_pagamento=descricao,
            idPagamento=idPagamento,
        )
        pedido.save()
    elif Pedido.objects.filter(comprador=perfil, plano_ativo=False).exists():
        pedido = Pedido.objects.get(comprador=perfil, plano_ativo=False)
        pedido.comprador = perfil
        pedido.preco_pedido = plano_preco
        pedido.endDate = data_formatada
        pedido.plano = plano
        pedido.link_pagamento = url_payment
        pedido.descricao_pagamento = descricao
        pedido.idPagamento = idPagamento
        pedido.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/pagamento_pendente.html', 
    {'nome': perfil.usuario.first_name, 'link': url_payment})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Realize o Pagamento - GMP University', text_content, 
    settings.EMAIL_HOST_USER, [perfil.usuario.email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    pedido.recebeu_email_pendente = True
    pedido.save()

    # print(response.text)
    messages.info(request, 'Geramos um link para você realizar o pagamento.')
    messages.info(request, 'Você pode acessar o link clicando no botão abaixo, ou acessando o link pelo seu e-mail (olhe a caixa de spam).')
    return redirect('perfil')


def sucesso(request):
    return HttpResponse('Sucesso')


def rejeitado(request):
    return HttpResponse('Rejeitado')


def atualizar_assinatura(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not Planos.objects.all().exists():
        messages.error(request, 'Nenhum plano foi cadastrado ainda!')
        return redirect('perfil')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'O seu perfil foi excluído. Por favor, fale com o suporte!')
        return redirect('perfil')
    
    perfil = Perfil.objects.get(usuario=request.user)
    
    if not Pedido.objects.filter(comprador=perfil, plano_ativo=True).exists():
        messages.error(request, 'Você não possui nenhum plano ativo!')
        return redirect('perfil')

    planos = Planos.objects.all()
    pedido = Pedido.objects.get(comprador=perfil, plano_ativo=True)
    provas = get_list_or_404(Prova)

    if request.method != 'POST':
        return render(request, 'atualizar_assinatura.html', {'planos': planos, 'pedido': pedido, 'provas': provas,})
    
    plano = request.POST.get('plano', '')
    suspender = request.POST.get('suspender', '')

    if not plano and not suspender:
        messages.error(request, 'Selecione um plano!')
        return render(request, 'atualizar_assinatura.html', {'planos': planos, 'pedido': pedido, 'provas': provas,})

    if suspender == 'nao' and not plano:
        messages.error(request, 'Selecione um plano!')
        return render(request, 'atualizar_assinatura.html', {'planos': planos, 'pedido': pedido, 'provas': provas,})

    elif suspender == 'sim':
        headers = {
            "accept": "application/json",
            "access_token": settings.KEY_API,
        }

        # url = f"https://sandbox.asaas.com/api/v3/subscriptions/{pedido.idAssinatura}"
        url = f"https://asaas.com/api/v3/subscriptions/{pedido.idAssinatura}"

        payload = {
            "status": "INACTIVE",
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access_token": settings.KEY_API,
        }

        response = dict(requests.put(url, json=payload, headers=headers).json())

        pedido.plano_ativo = False
        pedido.save()

        messages.info(request, 'Seu plano foi suspenso!')
        return redirect('perfil')

    if plano and not suspender:

        try:
            if plano == 'basico':
                novo_preco = Planos.objects.get(tipo='basico').preco
            elif plano == 'intermediario':
                novo_preco = Planos.objects.get(tipo='intermediario').preco
            elif plano == 'avancado':
                novo_preco = Planos.objects.get(tipo='avancado').preco
        except:
            messages.error(request, 'Erro nos preços dos planos. Fale com o suporte!')
            return render(request, 'atualizar_assinatura.html', {'planos': planos, 'pedido': pedido, 'provas': provas,})

        headers = {
            "accept": "application/json",
            "access_token": settings.KEY_API,
        }

        # url = f"https://sandbox.asaas.com/api/v3/subscriptions/{pedido.idAssinatura}"
        url = f"https://asaas.com/api/v3/subscriptions/{pedido.idAssinatura}"

        payload = {
            "value": novo_preco,
            "status": "ACTIVE",
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access_token": settings.KEY_API,
        }

        response = dict(requests.put(url, json=payload, headers=headers).json())

        pedido.preco_pedido = novo_preco
        pedido.plano = plano
        pedido.save()

        messages.info(request, 'Seu plano foi atualizado!')
        return redirect('perfil')



@csrf_exempt
def webhook(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        payload = dict(payload)
        # Enviando E-mail - Início
        """ html_content = render_to_string('emails/pagamento_pendente.html', 
        {'nome': f"{payload}"})
        text_content = strip_tags(html_content)

        _email = EmailMultiAlternatives('WEHBOOK - GMP University', text_content, 
        settings.EMAIL_HOST_USER, ['guiorganization@gmail.com'])
        _email.attach_alternative(html_content, 'text/html')
        _email.send() """
        # Enviando E-mail - Fim
        # return HttpResponse('')

    except:
        return HttpResponse('')
    # return HttpResponse('')

    if payload and payload.get('payment'):
        try:
            idPagamento = payload['payment']['paymentLink']
            metodo_pagamento = payload['payment']['billingType']
            customer = payload['payment']['customer']
            status = payload['payment']['status']
            # idAssinatura = payload['payment']['id']
        except:
            return HttpResponse('')

        if Pedido.objects.filter(idPagamento=idPagamento, plano_ativo=True).exists():
            return HttpResponse('')
        elif Pedido.objects.filter(idPagamento=idPagamento, plano_ativo=False).exists():
            pedido = Pedido.objects.get(idPagamento=idPagamento)
        else:
            return HttpResponse('')
        
        try:
            pedido.metodo_pagamento = metodo_pagamento
            pedido.customer = customer
            # pedido.idAssinatura = idAssinatura
            nome = pedido.comprador.usuario.first_name
            # pedido.save()
        except:
            return HttpResponse('')
        

        try:
            # url = f"https://sandbox.asaas.com/api/v3/subscriptions?customer={customer}"
            url = f"https://asaas.com/api/v3/subscriptions?customer={customer}"

            headers = {
                "accept": "application/json",
                "access_token": settings.KEY_API,
            }

            response = dict(requests.get(url, headers=headers).json())

            pedido.idAssinatura = response['data'][0]['id']
        except:
            return HttpResponse('')


        if status == 'CONFIRMED':
            pedido.status_pedido = 'approved'
            pedido.save()

            if not pedido.recebeu_email_aprovado:
                # Enviando E-mail - Início
                html_content = render_to_string('emails/pagamento_aprovado.html', 
                {'nome': nome})
                text_content = strip_tags(html_content)

                _email = EmailMultiAlternatives('Pagamento Aprovado - GMP University', text_content, 
                settings.EMAIL_HOST_USER, [pedido.comprador.usuario.email])
                _email.attach_alternative(html_content, 'text/html')
                _email.send()
                # Enviando E-mail - Fim

                pedido.recebeu_email_aprovado = True
                pedido.plano_ativo = True
                pedido.save()

        else:
            pedido.status_pedido = 'rejected'
            pedido.save()

            if not pedido.recebeu_email_reprovado:
                # Enviando E-mail - Início
                html_content = render_to_string('emails/pagamento_rejeitado.html', 
                {'nome': nome})
                text_content = strip_tags(html_content)

                _email = EmailMultiAlternatives('Pagamento Rejeitado - GMP University', text_content, 
                settings.EMAIL_HOST_USER, [pedido.comprador.usuario.email])
                _email.attach_alternative(html_content, 'text/html')
                _email.send()
                # Enviando E-mail - Fim

                pedido.recebeu_email_reprovado = True
                pedido.save()
    else:
        return HttpResponse('')

# Gerenciamento e Pagamento Assinaturas - Fim
