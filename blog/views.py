from django.shortcuts import render, redirect, reverse
from .models import Categoria, Post
from django.http import HttpResponse
from faker import Faker
from time import sleep
from django.conf import settings

def blog(request):
    posts = Post.objects.filter(visibilidade=True).order_by('-data_publicacao')

    post_um = None
    post_dois = None
    post_tres = None
    post_quatro = None
    post_cinco = None
    post_seis = None
    post_sete = None
    post_oito = None
    post_nove = None
    post_dez = None
    post_onze = None
    post_doze = None

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

        try:
            post_seis = posts[5]
        except IndexError:
            ...

        try:
            post_sete = posts[6]
        except IndexError:
            ...

        try:
            post_oito = posts[7]
        except IndexError:
            ...

        try:
            post_nove = posts[8]
        except IndexError:
            ...

        try:
            post_dez = posts[9]
        except IndexError:
            ...

        try:
            post_onze = posts[10]
        except IndexError:
            ...

        try:
            post_doze = posts[11]
        except IndexError:
            ...

    
    return render(request, 'blog.html', {
        'posts': posts,
        'post_um': post_um,
        'post_dois': post_dois,
        'post_tres': post_tres,
        'post_quatro': post_quatro,
        'post_cinco': post_cinco,
        'post_seis': post_seis,
        'post_sete': post_sete,
        'post_oito': post_oito,
        'post_nove': post_nove,
        'post_dez': post_dez,
        'post_onze': post_onze,
        'post_doze': post_doze,
    })

def post(request, slug):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('home')
	)

    if not Post.objects.filter(visibilidade=True, slug=slug).exists():
        return redirect(http_referer)
    
    post = Post.objects.get(visibilidade=True, slug=slug)

    return render(request, 'post.html', {
        'post': post,
    })

def ultima_noticia(request):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('home')
	)

    if not Post.objects.filter(visibilidade=True).exists():
        return redirect(http_referer)
    
    slug = Post.objects.filter(visibilidade=True).last().slug
    return redirect(f'{settings.DOMINIO}/post/{slug}')


""" def criar_posts_fakes(request):
    faker = Faker(['pt_BR'])

    categoria = Categoria.objects.first()

    for i in range(12):
        titulo = faker.text(100).replace(' ', '-').replace('.', '')
        descricao = faker.text(200)
        texto = faker.text(3000)
        sleep(1)

        post = Post.objects.create(titulo=titulo, descricao=descricao, texto=texto, categoria=categoria)
        post.save()

    return HttpResponse(f'{i + 1} posts criados') """