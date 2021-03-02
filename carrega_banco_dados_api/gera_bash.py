import pathlib
import subprocess
from comum import parametros


def pega_nomes_scripts(dados_path, scripts_path):
    nomes_scripts = {}

    for arquivo_dicts in dados_path.glob('**/*api*'):
        nome_script = arquivo_dicts.name.replace(arquivo_dicts.suffix, '.sh')
        nome_script = str(scripts_path / nome_script)

        nomes_scripts[str(arquivo_dicts)] = nome_script

    return nomes_scripts


def copia_base_scripts(base_scripts, arquivo_saida):
    subprocess.run(
        [
            'cp',
            '-f',
            str(base_scripts),
            arquivo_saida
        ],
        check=True
    )


def gera_comando_sed(arquivo_entrada, arquivo_saida):
    return ' '.join(
        [
            f"sed 's/^/curl_func {parametros.URL_API} /g'",
            arquivo_entrada,
            '>>',
            arquivo_saida
        ]
    )


def adiciona_comandos(arquivo_entrada, arquivo_saida):
    subprocess.run(
        gera_comando_sed(arquivo_entrada, arquivo_saida),
        check=True,
        shell=True
    )


def cria_scripts(base_scripts, nomes_scripts):
    for arquivo_dicts, nome_script in nomes_scripts.items():
        if pathlib.Path(nome_script).exists() and not parametros.SOBRESCREVER:
            print(f'O script {nome_script} já existe e não será sobrescrito')
        else:
            copia_base_scripts(base_scripts, nome_script)
            adiciona_comandos(arquivo_dicts, nome_script)


if __name__ == '__main__':
    pd = parametros.PASTA_DADOS
    ps = parametros.PASTA_SCRIPTS

    cond_pd = pd.exists() and pd.is_dir()
    cond_ps = ps.exists() and ps.is_dir()

    if cond_pd and cond_ps:
        bs = parametros.BASE_SCRIPTS
        if bs.exists() and bs.is_file():
            scripts_dict = pega_nomes_scripts(pd, ps)
            cria_scripts(bs, scripts_dict)
        else:
            print(f'O arquivo {bs} é inválido')
    elif cond_pd:
        print(f'A pasta {ps} é inválida')
    else:
        print(f'A pasta {pd} é inválida')
