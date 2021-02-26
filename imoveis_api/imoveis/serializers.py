from rest_framework import serializers
from imoveis.models import Estado, Cidade, Imovel


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'


class CidadeSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()


    class Meta:
        model = Cidade
        fields = ['id', 'nome', 'estado']


class ImovelSerializer(serializers.HyperlinkedModelSerializer):
    cidade = CidadeSerializer()


    class Meta:
        model = Imovel
        fields = [
            'url',
            'id',

            'logradouro',
            'numero',
            'bairro',
            'cidade',

            'area',
            'quartos',
            'banheiros',
            'vagas',
            'preco'
        ]
