import pathlib
from json import dumps
from comum import parametros


def pega_nomes_arquivos(pasta_path):
    nomes_arquivos = {}

    for arquivo_entrada in pasta_path.glob('**/*processados_1*.jl'):
        arquivo_saida = (
            arquivo_entrada
            .name
            .replace('processados', 'processados_api')
            .replace(arquivo_entrada.suffix, '.txt')
        )
        arquivo_saida = str(arquivo_entrada.parent / arquivo_saida)

        nomes_arquivos[str(arquivo_entrada)] = arquivo_saida

    return nomes_arquivos


def pega_dict(linha):
    return eval(linha.replace('null', 'None'))


def converte_dict(dict_velho):
    dict_novo = dict_velho.copy()

    if dict_novo['logradouro'] is None:
        dict_novo['logradouro'] = ''

    cidade_dict = {
        'nome': dict_novo['cidade'],
        'estado': {'sigla': dict_novo['estado']}
    }
    dict_novo['cidade'] = cidade_dict
    del dict_novo['estado']

    return dict_novo


def pega_converte_dict(linha):
    return converte_dict(pega_dict(linha))


def pega_converte_todos_dicts(arquivo_entrada):
    dicts_novos = []

    with open(arquivo_entrada, 'r') as arquivo:
        for linha in arquivo:
            dicts_novos.append(pega_converte_dict(linha))

    return dicts_novos


def escreve_dict(dict_novo):
    return ''.join(
        [
            '\"',
            (
                dumps(dict_novo, ensure_ascii=False)
                .replace('\'', '\\\'')
                .replace('\"', '\\\"')
            ),
            '\"\n'
        ]
    )


def escreve_todos_dicts(dicts_novos, arquivo_saida):
    if pathlib.Path(arquivo_saida).exists() and not parametros.SOBRESCREVER:
        print(f'O arquivo {arquivo_saida} já existe e não será sobrescrito')
    else:
        with open(arquivo_saida, 'w') as arquivo:
            for dict_novo in dicts_novos:
                arquivo.write(escreve_dict(dict_novo))


def converte_1_arquivo(par_entrada_saida):
    arquivo_entrada, arquivo_saida = par_entrada_saida
    dicts_novos = pega_converte_todos_dicts(arquivo_entrada)
    escreve_todos_dicts(dicts_novos, arquivo_saida)


def converte_todos_arquivos(nomes_arquivos):
    for par_entrada_saida in nomes_arquivos.items():
        converte_1_arquivo(par_entrada_saida)


if __name__ == '__main__':
    if parametros.PASTA_DADOS.exists() and parametros.PASTA_DADOS.is_dir():
        arquivos_dict = pega_nomes_arquivos(parametros.PASTA_DADOS)
        converte_todos_arquivos(arquivos_dict)
    else:
        print(f'A pasta {parametros.PASTA_DADOS} é inválida')
