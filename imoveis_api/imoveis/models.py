from django.db import models
from django.utils import timezone


class Estado(models.Model):
    sigla = models.CharField(max_length=2, unique=True)


    def __str__(self):
        return self.sigla


class Cidade(models.Model):
    nome = models.CharField('cidade', max_length=70)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)


    def __str__(self):
        return self.nome + ' - ' + self.estado.sigla


class Imovel(models.Model):
    adicionado = models.DateTimeField('adicionado em', default=timezone.now)

    logradouro = models.CharField(max_length=200, blank=True)
    numero = models.IntegerField('número', null=True)
    bairro = models.CharField(max_length=70)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)

    area = models.IntegerField('área (m\u00b2)')
    quartos = models.IntegerField()
    banheiros = models.IntegerField()
    vagas = models.IntegerField()
    preco = models.IntegerField('preço (R$)')


    def __str__(self):
        partes = [
            self.pega_logradouro_numero(),
            self.pega_cidade_estado(),
            self.pega_preco()
        ]

        if partes[0] == '---':
            return ' - '.join(partes[1:])
        return ' - '.join(partes)


    def pega_logradouro_numero(self):
        logradouro_numero = self.logradouro
        if not logradouro_numero:
            return '---'

        numero = self.numero
        if numero is not None:
            logradouro_numero += ', ' + str(numero)

        return logradouro_numero
    pega_logradouro_numero.short_description = 'logradouro e número'


    def pega_cidade_estado(self):
        return str(self.cidade)
    pega_cidade_estado.short_description = 'cidade - estado'


    def pega_preco(self):
        return 'R$ ' + '{:,}'.format(self.preco).replace(',', '.') + ',00'
    pega_preco.short_description = 'preço'
