from concurrent.futures import ThreadPoolExecutor
from scraper.processador import ImoveisProcessador
from scraper.scraper import ImoveisScraper


HEADLESS = False
PAGS = 2
VERBOSE = False


partes_url = [
    'https://www.vivareal.com.br/venda/',
    None,
    'apartamento_residencial/',
]


def arruma_cidades_dict(cidades_dict):
    for cidade, parte_url in cidades_dict.items():
        partes_url[1] = parte_url
        cidades_dict[cidade] = ''.join(partes_url)


def raspa_cidade(par_cidade):
    cidade, url = par_cidade
    raspador = ImoveisScraper(
        url=url,
        pags=PAGS,
        saida='imoveis_' + cidade + '.jl',
        headless=HEADLESS
    )

    raspador.raspa_cidade(verbose=VERBOSE)
    raspador.quit()


def gera_entrada_saida_dict(cidades_dict):
    entrada_saida_dict = {}

    for cidade in cidades_dict:
        entrada = 'imoveis_' + cidade + '.jl'
        saida = 'imoveis_processados_' + cidade + '.jl'
        entrada_saida_dict[entrada] = saida

    return entrada_saida_dict


def processa_cidade(par_entrada_saida):
    entrada, saida = par_entrada_saida
    proc = ImoveisProcessador(entrada=entrada, saida=saida)

    proc.escreve_imoveis()
    proc.escreve_resumo()

    print()


cidades = {
    'bh': 'minas-gerais/belo-horizonte/',
    'cwb': 'parana/curitiba/',
    'poa': 'rio-grande-do-sul/porto-alegre/',
    'rj': 'rj/rio-de-janeiro/',
    'sp': 'sp/sao-paulo/',
}
arruma_cidades_dict(cidades)
entrada_saida = gera_entrada_saida_dict(cidades)

# with ThreadPoolExecutor(max_workers=2) as executor:
#     executor.map(raspa_cidade, cidades.items())
for par in cidades.items():
    raspa_cidade(par)

print()
with ThreadPoolExecutor() as executor:
    executor.map(processa_cidade, entrada_saida.items())
