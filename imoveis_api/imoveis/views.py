from rest_framework import viewsets
from imoveis.models import Estado, Cidade, Imovel
from imoveis.serializers import EstadoSerializer
from imoveis.serializers import CidadeSerializer
from imoveis.serializers import ImovelSerializer


class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer


class CidadeViewSet(viewsets.ModelViewSet):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer


class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer
