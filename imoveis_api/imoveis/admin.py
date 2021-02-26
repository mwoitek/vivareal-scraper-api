from django.contrib import admin
from imoveis.models import Estado, Cidade, Imovel


class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')


class ImovelAdmin(admin.ModelAdmin):
    list_display = (
        'pega_logradouro_numero',
        'pega_cidade_estado',
        'pega_preco'
    )

    fieldsets = [
        (
            None,
            {
                'fields': ['adicionado']
            }
        ),
        (
            'Endereço',
            {
                'fields': [
                    'logradouro',
                    'numero',
                    'bairro',
                    'cidade'
                ]
            }
        ),
        (
            'Detalhes sobre o Imóvel',
            {
                'fields': [
                    'area',
                    'quartos',
                    'banheiros',
                    'vagas',
                    'preco'
                ]
            }
        )
    ]


admin.site.register(Estado)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Imovel, ImovelAdmin)
