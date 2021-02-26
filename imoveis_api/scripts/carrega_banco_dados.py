from imoveis.models import Estado, Cidade, Imovel


ARQUIVO = './dados_raspados/imoveis_processados_1614181256.jl'
LIMPA = False


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


def run():
    if LIMPA:
        limpa_banco_dados()

    imoveis_lidos = 0
    imoveis_aproveitados = 0

    with open(ARQUIVO, 'r') as arquivo:
        for linha in arquivo:
            imovel_dict = pega_linha_dict(linha)
            imoveis_lidos += 1

            estado = pega_ou_cria_estado(imovel_dict)
            cidade = pega_ou_cria_cidade(imovel_dict, estado)

            criado = pega_ou_cria_imovel(imovel_dict, cidade)
            if criado:
                imoveis_aproveitados += 1

    print(f'Imóveis lidos:        {imoveis_lidos}')
    print(f'Imóveis aproveitados: {imoveis_aproveitados}')
    print(f'Imóveis descartados:  {imoveis_lidos - imoveis_aproveitados}')
