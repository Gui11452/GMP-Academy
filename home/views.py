from django.shortcuts import render, redirect, reverse, get_list_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
# import mercadopago
from gmp.settings import RECAPTCHA_FRONT, RECAPTCHA_BACK, MEDIA_ROOT
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from blog.models import Post
from perfil.models import Perfil, Planos, Pedido, Topicos
from questoes.models import Prova
from home.models import SobreNos, FaleConosco, EmailsProntos, ArquivosExcel
from questoes.models import Disciplina, Prova, Banca, Questao, Ano
import requests
import json
import openpyxl
from django.db.models import Q

def home(request):
    posts = Post.objects.filter(visibilidade=True).order_by('-data_publicacao')
    planos = get_list_or_404(Planos)

    if request.user.is_authenticated:
        if Pedido.objects.filter(comprador__usuario=request.user).exists():
            pedido = Pedido.objects.get(comprador__usuario=request.user)
        else:
            pedido = ''
    else:
        pedido = ''

    provas_cabecalho = get_list_or_404(Prova)[:10]
    provas = Prova.objects.all()
    if not provas:
        raise Http404()

    post_um = None
    post_dois = None
    post_tres = None
    post_quatro = None

    if posts:
        posts = list(posts)

        try:
            post_um = posts[0]
        except IndexError:
            ...

        try:
            post_dois = posts[1]
        except IndexError:
            ...

        try:
            post_tres = posts[2]
        except IndexError:
            ...

        try:
            post_quatro = posts[3]
        except IndexError:
            ...

        try:
            post_cinco = posts[4]
        except IndexError:
            ...

    topicos = []
    for plano in planos:
        topicos.append(list(Topicos.objects.filter(plano=plano)))

    plano_topicos = zip(planos, topicos)
    
    return render(request, 'index.html', {
        'plano_topicos': plano_topicos,
        'posts': posts,
        'post_um': post_um,
        'post_dois': post_dois,
        'post_tres': post_tres,
        'post_quatro': post_quatro,
        'pedido': pedido,
        'provas': provas,
        'primeiro_plano': planos[0],
        'ultima_prova': provas.last(),
        'provas_cabecalho': provas_cabecalho    
    })


def planos(request):
    planos = get_list_or_404(Planos)
    provas_cabecalho = get_list_or_404(Prova)[:10]

    if request.user.is_authenticated:
        if Pedido.objects.filter(comprador__usuario=request.user).exists():
            pedido = Pedido.objects.get(comprador__usuario=request.user)
        else:
            pedido = ''
    else:
        pedido = ''

    topicos = []
    for plano in planos:
        topicos.append(list(Topicos.objects.filter(plano=plano)))

    plano_topicos = zip(planos, topicos)
    
    return render(request, 'planos.html', {
        'plano_topicos': plano_topicos,
        'primeiro_plano': planos[0], 
        'pedido': pedido,
        'provas_cabecalho': provas_cabecalho,
    })


def quem_somos(request):
    provas_cabecalho = get_list_or_404(Prova)[:10]
    sobre_nos = SobreNos.objects.all().first()

    return render(request, 'quem_somos.html', {'provas_cabecalho': provas_cabecalho, 'sobre_nos': sobre_nos,})


def envio_emails(request):
    if request.user.is_authenticated and request.user.is_staff:
        provas_cabecalho = get_list_or_404(Prova)[:10]

        emails_prontos = EmailsProntos.objects.all()

        if request.method != 'POST':
            return render(request, 'envio_email.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas_cabecalho,
                'emails_prontos': emails_prontos,
            })
        
        email_id = request.POST.get('email_id')
        recaptcha = request.POST.get('g-recaptcha-response')

        if not EmailsProntos.objects.filter(id=email_id).exists():
            messages.error(request, 'Esse e-mail não existe mais no banco de dados. Cadastre-o novamente.')
            return render(request, 'envio_email.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas_cabecalho,
                'emails_prontos': emails_prontos,
            })

        # Início - Recaptcha
        if not recaptcha:
            messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
            return render(request, 'envio_email.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas_cabecalho,
                'emails_prontos': emails_prontos,
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
            return render(request, 'envio_email.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas_cabecalho,
                'emails_prontos': emails_prontos,
            })
        # Final - Recaptcha

        email_pronto = EmailsProntos.objects.get(id=email_id)

        perfis = Perfil.objects.filter(verificacao_email=True)
        lista_emails = [perfil.usuario.email for perfil in perfis]
        
        # Enviando E-mail - Início
        dicionario_atrb = {
            'titulo': email_pronto.titulo, 
        }
        if email_pronto.texto1:
            dicionario_atrb['texto1'] = email_pronto.texto1
        if email_pronto.texto2:
            dicionario_atrb['texto2'] = email_pronto.texto2
        if email_pronto.texto3:
            dicionario_atrb['texto3'] = email_pronto.texto3
        if email_pronto.texto4:
            dicionario_atrb['texto4'] = email_pronto.texto4
        if email_pronto.texto5:
            dicionario_atrb['texto5'] = email_pronto.texto5
        if email_pronto.texto6:
            dicionario_atrb['texto6'] = email_pronto.texto6
        if email_pronto.texto7:
            dicionario_atrb['texto7'] = email_pronto.texto7
        if email_pronto.texto8:
            dicionario_atrb['texto8'] = email_pronto.texto8

        html_content = render_to_string('emails/email_personalizado.html', 
            dicionario_atrb
        )

        text_content = strip_tags(html_content)

        _email = EmailMultiAlternatives(f'{email_pronto.titulo} - GMP University', text_content, 
        settings.EMAIL_HOST_USER, lista_emails)
        _email.attach_alternative(html_content, 'text/html')
        _email.send()
        # Enviando E-mail - Fim

        email_pronto.contagem += 1
        email_pronto.save()

        messages.success(request, 'Todos os e-mails foram enviados com sucesso!')
        return render(request, 'envio_email.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
            'emails_prontos': emails_prontos,
        })

    else:
        return redirect('home')


def cadastro_questoes(request):
    if request.user.is_authenticated and request.user.is_staff:
        provas_cabecalho = get_list_or_404(Prova)[:10]

        """ for questao in Questao.objects.all():
            questao.delete() """

        if request.method != 'POST':
            return render(request, 'cadastro_questoes.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas_cabecalho,
            })
        
        arquivo = request.FILES.get('arquivo')
        recaptcha = request.POST.get('g-recaptcha-response')

        arquivo_excel = ArquivosExcel.objects.create(arquivo=arquivo)
        arquivo_excel.save()

        # Início - Recaptcha
        if not recaptcha:
            messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
            return render(request, 'cadastro_questoes.html', {
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
            return render(request, 'cadastro_questoes.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                'provas': provas_cabecalho,
            })
        # Final - Recaptcha
        
        # Manipulação Excel - Início
        caminho_arquivo = arquivo_excel.arquivo.path
        pedidos = openpyxl.load_workbook(caminho_arquivo)
        nome_planilha = pedidos.sheetnames[0]
        planilha = pedidos[nome_planilha]
        c = 0
        for linha in planilha:
            if c == 0:
                c+=1
                continue
        
            print(linha)

            texto = linha[0].value
            if Questao.objects.filter(texto=texto).exists() or not texto:
                continue

            alt_a = linha[1].value
            alt_b = linha[2].value
            alt_c = linha[3].value
            alt_d = linha[4].value
            alt_e = linha[5].value

            if not alt_a:
                alt_a = 'Vazio'

            if not alt_b:
                alt_b = 'Vazio'

            if not alt_c:
                alt_c = 'Vazio'

            if not alt_d:
                alt_d = 'Vazio'

            if not alt_e:
                alt_e = 'Vazio'

            alt_a = alt_a.replace('Certo', 'Correto')

            banca = linha[6].value
            prova = linha[7].value
            orgao = linha[8].value
            ano = int(linha[9].value.replace('Ano:', '').strip())
            gabarito = linha[10].value
            disciplina = linha[11].value

            if alt_a == 'Correto' and gabarito == 'A':
                gabarito = 'Correto'

            if not banca or not prova or not disciplina:
                continue

            banca = banca.replace('/', ' ')
            prova = prova.replace('/', ' ')
            disciplina = disciplina.replace('/', ' ')

            if not Disciplina.objects.filter(nome=disciplina).exists():
                disciplina = Disciplina.objects.create(nome=disciplina)
                disciplina.save()
            else:
                disciplina = Disciplina.objects.get(nome=disciplina)

            if not Banca.objects.filter(nome=banca).exists():
                banca = Banca.objects.create(nome=banca)
                banca.save()
            else:
                banca = Banca.objects.get(nome=banca)

            if not Prova.objects.filter(nome=prova).exists():
                prova = Prova.objects.create(nome=prova)
                prova.save()
            else:
                prova = Prova.objects.get(nome=prova)

            if not Ano.objects.filter(valor=ano).exists():
                ano = Ano.objects.create(valor=ano)
                ano.save()
            else:
                ano = Ano.objects.get(valor=ano)

            if alt_a != 'Correto' and alt_b != 'Errado':
                questao = Questao.objects.create(
                    disciplina=disciplina,
                    ano=ano,
                    prova=prova,
                    banca=banca,
                    texto=texto,
                    A=alt_a,
                    B=alt_b,
                    C=alt_c,
                    D=alt_d,
                    E=alt_e,
                    gabarito_alternativa=gabarito,
                )
            else:
                questao = Questao.objects.create(
                    disciplina=disciplina,
                    ano=ano,
                    prova=prova,
                    banca=banca,
                    texto=texto,
                    A=alt_a,
                    B=alt_b,
                    gabarito_alternativa=gabarito
                )
            questao.save()

        # arquivo_excel.delete()
        # Manipulação Excel - Fim
        
        messages.success(request, 'Questões cadastradas com sucesso!')
        return render(request, 'cadastro_questoes.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })

    else:
        return redirect('home')


def fale_conosco(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Para mandar uma menmsagem para nós, faça o login primeiro.')
        return redirect('login')

    provas_cabecalho = get_list_or_404(Prova)[:10]

    if request.method != 'POST':
        return render(request, 'fale_conosco.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    
    titulo = request.POST.get('titulo')
    assunto = request.POST.get('assunto')
    texto = request.POST.get('texto')
    recaptcha = request.POST.get('g-recaptcha-response')

    usuario = request.user

    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'fale_conosco.html', {
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
        return render(request, 'fale_conosco.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'provas': provas_cabecalho,
        })
    # Final - Recaptcha

    mensagem = FaleConosco.objects.create(usuario=usuario, titulo=titulo, assunto=assunto, texto=texto)
    mensagem.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/email_fale_conosco.html', 
    {'usuario': usuario, 'data': mensagem.data, 'titulo': titulo, 'assunto': assunto, 'texto': texto, 'email': usuario.email})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Nova Mensagem - GMP University', text_content, 
    settings.EMAIL_HOST_USER, ['ggmpuniversity@gmail.com'])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    messages.success(request, f'{usuario}, a sua mensagem foi enviada com sucesso. Aguarde o retorno em breve.')
    return render(request, 'fale_conosco.html', {
        'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        'provas': provas_cabecalho,
    })