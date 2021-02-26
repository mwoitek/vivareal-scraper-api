import re
from json import dumps
from scraper.converte_inteiro import converte_inteiro


regexps = {
    'logradouro': r'((?P<logradouro>(\w|[-.\' ])+)((, )|( - )))?',
    'numero': r'((?P<numero>[0-9]+) - )?',
    'bairro': r'(?P<bairro>(\w|[-.\' ])+), ',
    'cidade': r'(?P<cidade>(\w|[-.\' ])+) - ',
    'estado': r'(?P<estado>[A-Z]{2})',
}
regexp_endereco = re.compile(''.join(regexps.values()))


campos_excluir = ['logradouro', 'numero']


class ImovelDict():
    def __init__(self, string):
        self.dict_velho = eval(string.replace('null', 'None'))
        self.dict_novo = {}


    def __str__(self):
        return dumps(self.dict_novo)


    def pega_endereco(self):
        return self.dict_velho['endereco']


    def pega_partes_endereco(self):
        endereco_match = regexp_endereco.match(self.pega_endereco())
        partes_endereco = {}

        for grupo in regexps:
            partes_endereco[grupo] = endereco_match.group(grupo)
        partes_endereco['numero'] = converte_inteiro(partes_endereco['numero'])

        return partes_endereco


    def pega_dict_novo(self):
        dict_novo = self.dict_velho.copy()
        partes_endereco = self.pega_partes_endereco()

        del dict_novo['endereco']
        dict_novo = {**partes_endereco, **dict_novo}

        return dict_novo


    def eh_valido(self):
        campos = [k for k in self.dict_novo if k not in campos_excluir]
        valido = True

        for campo in campos:
            if self.dict_novo[campo] is None:
                valido = False
                break

        return valido


class ImoveisProcessador():
    def __init__(self, entrada, saida):
        self.entrada = entrada
        self.saida = saida

        self.enderecos = self.pega_enderecos()
        self.imoveis_lidos = self.pega_imoveis_lidos()

        self.enderecos_unicos = self.pega_enderecos_unicos()

        self.imoveis = self.pega_imoveis()
        self.imoveis_aproveitados = self.pega_imoveis_aproveitados()

        del self.enderecos
        del self.enderecos_unicos


    def pega_enderecos(self):
        enderecos = []

        with open(self.entrada, 'r') as arquivo:
            for linha in arquivo:
                enderecos.append(ImovelDict(linha).pega_endereco())

        return enderecos


    def pega_enderecos_unicos(self):
        return set(self.enderecos)


    def pega_imoveis_lidos(self):
        return len(self.enderecos)


    def pega_imoveis(self):
        imoveis = []

        with open(self.entrada, 'r') as arquivo:
            for linha in arquivo:
                imovel = ImovelDict(linha)
                imovel.dict_novo = imovel.pega_dict_novo()
                endereco = imovel.pega_endereco()

                if endereco in self.enderecos_unicos and imovel.eh_valido():
                    imoveis.append(imovel)
                    self.enderecos_unicos.remove(endereco)

        return imoveis


    def pega_imoveis_aproveitados(self):
        return len(self.imoveis)


    def pega_imoveis_descartados(self):
        return self.imoveis_lidos - self.imoveis_aproveitados


    def escreve_imoveis(self):
        with open(self.saida, 'a') as arquivo:
            for imovel in self.imoveis:
                arquivo.write(str(imovel) + '\n')


    def escreve_resumo(self):
        print(f'Arquivo processado:   {self.entrada}\n')
        print(f'Imóveis lidos:        {self.imoveis_lidos}')
        print(f'Imóveis aproveitados: {self.imoveis_aproveitados}')
        print(f'Imóveis descartados:  {self.pega_imoveis_descartados()}')
