import pathlib


PASTA_DADOS = 'dados'
PASTA_SCRIPTS = 'bash_curl'
BASE_SCRIPTS = 'base.sh'
URL_API = 'http://localhost:8000/imoveis_api/imoveis/'
SOBRESCREVER = True

PASTA_DADOS = pathlib.Path(__file__).absolute().parents[2] / PASTA_DADOS
PASTA_SCRIPTS = pathlib.Path(__file__).absolute().parents[1] / PASTA_SCRIPTS
BASE_SCRIPTS = PASTA_SCRIPTS / BASE_SCRIPTS
URL_API = URL_API.replace('/', '\\/')
