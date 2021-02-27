from rest_framework import serializers
from imoveis.models import Estado, Cidade, Imovel


def pega_ou_cria_estado(estado_dict):
    estado, _ = (
        Estado
        .objects
        .get_or_create(sigla=estado_dict['sigla'])
    )
    return estado


def pega_ou_cria_cidade(cidade_dict, estado):
    cidade, _ = (
        Cidade
        .objects
        .get_or_create(
            nome=cidade_dict['nome'],
            estado=estado
        )
    )
    return cidade


def pega_ou_cria_imovel(imovel_dict, cidade):
    imovel, _ = (
        Imovel
        .objects
        .get_or_create(
            logradouro=imovel_dict['logradouro'],
            numero=imovel_dict['numero'],
            bairro=imovel_dict['bairro'],
            cidade=cidade,
            area=imovel_dict['area'],
            quartos=imovel_dict['quartos'],
            banheiros=imovel_dict['banheiros'],
            vagas=imovel_dict['vagas'],
            preco=imovel_dict['preco']
        )
    )
    return imovel


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'


class CidadeSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()


    class Meta:
        model = Cidade
        fields = ['id', 'nome', 'estado']


    def create(self, validated_data):
        estado = pega_ou_cria_estado(validated_data['estado'])
        return pega_ou_cria_cidade(validated_data, estado)


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


    def create(self, validated_data):
        cidade_dict = validated_data['cidade']
        estado_dict = cidade_dict['estado']

        estado = pega_ou_cria_estado(estado_dict)
        cidade = pega_ou_cria_cidade(cidade_dict, estado)

        return pega_ou_cria_imovel(validated_data, cidade)
