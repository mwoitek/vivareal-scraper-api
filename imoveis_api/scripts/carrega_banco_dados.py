import os
from imoveis.models import Estado, Cidade, Imovel


LIMPA = True

PASTA = 'dados_raspados'
PASTA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    PASTA
)


def limpa_tabela(tabela):
    tabela.objects.all().delete()


def limpa_banco_dados():
    for tabela in [Estado, Cidade, Imovel]:
        limpa_tabela(tabela)


def pega_linha_dict(linha):
    return eval(linha.replace('null', 'None'))


def pega_ou_cria_estado(imovel_dict):
    estado, _ = (
        Estado
        .objects
        .get_or_create(sigla=imovel_dict['estado'])
    )
    return estado


def pega_ou_cria_cidade(imovel_dict, estado):
    cidade, _ = (
        Cidade
        .objects
        .get_or_create(
            nome=imovel_dict['cidade'],
            estado=estado
        )
    )
    return cidade


def pega_ou_cria_imovel(imovel_dict, cidade):
    logradouro = imovel_dict['logradouro']
    if logradouro is None:
        logradouro = ''

    _, criado = (
        Imovel
        .objects
        .get_or_create(
            logradouro=logradouro,
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
    return criado


def carrega_1_arquivo(nome_arquivo):
    imoveis_lidos = 0
    imoveis_aproveitados = 0

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            imovel_dict = pega_linha_dict(linha)
            imoveis_lidos += 1

            estado = pega_ou_cria_estado(imovel_dict)
            cidade = pega_ou_cria_cidade(imovel_dict, estado)

            criado = pega_ou_cria_imovel(imovel_dict, cidade)
            if criado:
                imoveis_aproveitados += 1

    print(f'Arquivo de entrada:   {nome_arquivo}\n')
    print(f'Imóveis lidos:        {imoveis_lidos}')
    print(f'Imóveis aproveitados: {imoveis_aproveitados}')

    imoveis_descartados = imoveis_lidos - imoveis_aproveitados
    print(f'Imóveis descartados:  {imoveis_descartados}\n')

    return (
        imoveis_lidos,
        imoveis_aproveitados,
        imoveis_descartados
    )


def pega_nomes_arquivos(pasta_str):
    nomes_arquivos = []

    with os.scandir(pasta_str) as pasta:
        for item in pasta:
            nome = item.name

            if item.is_file() and os.path.splitext(nome)[-1] == '.jl':
                nomes_arquivos.append(nome)

    return map(
        lambda n: os.path.join(pasta_str, n),
        nomes_arquivos
    )


def carrega_todos_arquivos(pasta_str):
    total_lidos = 0
    total_aproveitados = 0
    total_descartados = 0

    print()
    for nome_arquivo in pega_nomes_arquivos(pasta_str):
        imoveis_lidos, imoveis_aproveitados, imoveis_descartados = carrega_1_arquivo(nome_arquivo)

        total_lidos += imoveis_lidos
        total_aproveitados += imoveis_aproveitados
        total_descartados += imoveis_descartados

    print('Totais\n')
    print(f'Imóveis lidos:        {total_lidos}')
    print(f'Imóveis aproveitados: {total_aproveitados}')
    print(f'Imóveis descartados:  {total_descartados}\n')


def run():
    if LIMPA:
        limpa_banco_dados()

    if os.path.exists(PASTA):
        carrega_todos_arquivos(PASTA)
    else:
        print(f'A pasta {PASTA} não existe.')
