from django.db import models
from django.utils.text import slugify

class Categoria(models.Model):
    nome = models.CharField(default='', max_length=50, verbose_name='Nome da Categoria')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return f'{self.nome}'

class Post(models.Model):
    titulo = models.CharField(default='', max_length=1000, verbose_name='Título', unique=True)
    slug = models.SlugField(default='', max_length=1100, verbose_name='Slug', unique=True)
    descricao = models.TextField(default='', max_length=3000, verbose_name='Descrição')
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name='Data Publicação')
    data_alteracao = models.DateTimeField(auto_now=True, verbose_name='Data Alteração')
    texto = models.TextField(default='', verbose_name='Texto')
    visibilidade = models.BooleanField(default=True, verbose_name='Visibilidade')
    foto = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True, null=True, default=None)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, verbose_name='Categoria', null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.titulo}'
