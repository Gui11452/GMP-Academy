from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import random

class Prova(models.Model):
    nome = models.CharField(max_length=300, verbose_name='Nome', unique=True)

    def clean(self, *args, **kwargs):
        error_messages = {}

        if Prova.objects.filter(nome=self.nome).exists():
            error_messages['nome'] = f'O nome: "{self.nome}" já existe. Coloque outro!'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Prova'
        verbose_name_plural = 'Provas'

    def __str__(self):
        return self.nome
    
class Estado(models.Model):
    nome = models.CharField(max_length=300, verbose_name='Nome', unique=True)

    def clean(self, *args, **kwargs):
        error_messages = {}

        if Estado.objects.filter(nome=self.nome).exists():
            error_messages['nome'] = f'O nome: "{self.nome}" já existe. Coloque outro!'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.nome
    
class Ano(models.Model):
    valor = models.PositiveIntegerField(default=0, verbose_name='Nome', unique=True)

    def clean(self, *args, **kwargs):
        error_messages = {}

        if Ano.objects.filter(valor=self.valor).exists():
            error_messages['valor'] = f'O ano: "{self.valor}" já foi cadastrado. Coloque outro!'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Ano'
        verbose_name_plural = 'Anos'

    def __str__(self):
        return f'{self.valor}'
    
class Disciplina(models.Model):
    nome = models.CharField(max_length=300, verbose_name='Nome', unique=True)

    def clean(self, *args, **kwargs):
        error_messages = {}

        if Disciplina.objects.filter(nome=self.nome).exists():
            error_messages['nome'] = f'O nome: "{self.nome}" já existe. Coloque outro!'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return self.nome 
    
class Banca(models.Model):
    nome = models.CharField(max_length=300, verbose_name='Nome', unique=True)

    def clean(self, *args, **kwargs):
        error_messages = {}

        if Banca.objects.filter(nome=self.nome).exists():
            error_messages['nome'] = f'O nome: "{self.nome}" já existe. Coloque outro!'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Banca'
        verbose_name_plural = 'Bancas'

    def __str__(self):
        return self.nome 


class Questao(models.Model):
    codigo = models.CharField(max_length=255, verbose_name='Código', unique=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, verbose_name='Disciplina')
    ano = models.ForeignKey(Ano, on_delete=models.PROTECT, verbose_name='Ano')
    prova = models.ForeignKey(Prova, on_delete=models.PROTECT, verbose_name='Prova')
    banca = models.ForeignKey(Banca, on_delete=models.PROTECT, verbose_name='Banca')
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, verbose_name='Estado', blank=True, null=True)
    texto = models.TextField(verbose_name='Texto')
    A = models.CharField(max_length=2000, verbose_name='A', blank=True, null=True)
    B = models.CharField(max_length=2000, verbose_name='B', blank=True, null=True)
    C = models.CharField(max_length=2000, verbose_name='C', blank=True, null=True)
    D = models.CharField(max_length=2000, verbose_name='D', blank=True, null=True)
    E = models.CharField(max_length=2000, verbose_name='E', blank=True, null=True)

    gabarito_alternativa = models.CharField(
		default='A',
		max_length=7,
		choices=(
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            ('E', 'E'),
            ('Correto', 'Correto'),
            ('Errado', 'Errado'),
        ),
		verbose_name="Gabarito Alternativa"
	)
    gabarito_texto = models.CharField(max_length=2000, verbose_name='Gabarito Texto')
    visibilidade = models.BooleanField(default=True, verbose_name='Visibilidade')

    def clean(self, *args, **kwargs):
        error_messages = {}
        print(not(self.A and self.B and self.C and self.D and self.E))
        print(self.gabarito_alternativa != 'Correto' and self.gabarito_alternativa != 'Errado')
        print(not(self.A and self.B and self.C and self.D and self.E) and (self.gabarito_alternativa != 'Correto' and 
                                                                 self.gabarito_alternativa != 'Errado'))
        if (self.A or self.B or self.C or self.D or self.E) and (self.gabarito_alternativa == 'Correto' or 
                                                                 self.gabarito_alternativa == 'Errado'):
            mensagem = 'Se você escolheu o gabarito como (Certo/Errado), deixe as alternativas A/B/C/D/E em branco.'
            if self.A:
                error_messages['A'] = mensagem
            if self.B:
                error_messages['B'] = mensagem
            if self.C:
                error_messages['C'] = mensagem
            if self.D:
                error_messages['D'] = mensagem
            if self.E:
                error_messages['E'] = mensagem
        
        
        elif not(self.A and self.B and self.C and self.D and self.E) and (self.gabarito_alternativa != 'Correto' and 
                                                                 self.gabarito_alternativa != 'Errado'):
            mensagem = 'Preencha as alternativas A/B/C/D/E e coloque um gabarito válido. Se for do tipo (Certo/Errado), deixe-as em branco.'
            error_messages['gabarito_alternativa'] = mensagem

        if error_messages:
            raise ValidationError(error_messages)

    
    def save(self, *args, **kwargs):
        if self.gabarito_alternativa == Questao._meta.get_field('A').name:
            self.gabarito_texto = self.A

        elif self.gabarito_alternativa == Questao._meta.get_field('B').name:
            self.gabarito_texto = self.B

        elif self.gabarito_alternativa == Questao._meta.get_field('C').name:
            self.gabarito_texto = self.C

        elif self.gabarito_alternativa == Questao._meta.get_field('D').name:
            self.gabarito_texto = self.D

        elif self.gabarito_alternativa == Questao._meta.get_field('E').name:
            self.gabarito_texto = self.E

        elif self.gabarito_alternativa == 'Correto':
            self.gabarito_texto = 'Correto'
        
        else:
            self.gabarito_texto = 'Errado'

        """ while not self.codigo:
            _codigo = random.randint(100000, 999999)
            validador = True
            for questao in Questao.objects.all():
                if questao.codigo.replace('Q', '') == str(_codigo):
                    validador = False
                    break
            if validador:
                self.codigo = f'Q{_codigo}'
                break
            else:
                continue """
        
        if not self.codigo:
            if not Questao.objects.all().exists():
                self.codigo = f'Q{1}'
            else:
                _questao = Questao.objects.last()
                codigo_questao = int(_questao.codigo.replace('Q', ''))
                self.codigo = f'Q{codigo_questao + 1}'

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

    def __str__(self):
        return self.codigo


class QuestaoRespondida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, verbose_name='Questão')
    resposta = models.CharField(
		default='Pendente',
		max_length=100,
		choices=(
            ('Acertei', 'Acertei'),
            ('Errei', 'Errei'),
            ('Pendente', 'Pendente'),
        ),
		verbose_name="Resposta"
	)

    class Meta:
        verbose_name = 'Questão Respondida'
        verbose_name_plural = 'Questões Respondidas'

    def __str__(self):
        return f'{self.usuario} / {self.questao}'
    

# Aulas - Início
class Aula(models.Model):
    pdf = models.FileField(upload_to="pdfs/%Y/%m/%d/", verbose_name='PDF (Opcional)', blank=True, null=True)
    video = models.URLField(max_length=10000, verbose_name='Link')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, verbose_name='Disciplina')
    visibilidade = models.BooleanField(default=True, verbose_name='Visibilidade')
    nome = models.CharField(default='', max_length=255, verbose_name='Nome')
    descricao = models.TextField(default='', max_length=10000, verbose_name='Descrição')

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return f'{self.nome}'
# Aulas - Fim
