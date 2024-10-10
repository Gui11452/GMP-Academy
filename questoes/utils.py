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
from duvidas.models import Comentarios, Duvidas, Respostas
from perfil.models import Perfil, Pedido
import requests
import json

def verify_acess_questions(request, login_required=True):
    if login_required and not request.user.is_authenticated:
        return 'login'
    else:
        ...
    
    if Perfil.objects.filter(verificacao_email=False, usuario=request.user).exists() or not Perfil.objects.filter(usuario=request.user).exists():
        return 'perfil'
    
    num_questoes_feitas = len(QuestaoRespondida.objects.filter(usuario=request.user))
    
    if not Pedido.objects.filter(comprador__usuario=request.user, plano_ativo=True).exists() and num_questoes_feitas == 10:
        messages.error(request, 'Você já fez todas as 10 questões gratuitas. Contrate um para desfrutar do nosso gigantesco banco de questões e aulas!')
        return 'perfil'