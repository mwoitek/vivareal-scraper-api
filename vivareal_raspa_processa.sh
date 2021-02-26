#!/bin/bash

SCRIPT=$(realpath $0)
PASTA_SCRIPT=$(dirname $SCRIPT)

PYTHON_SCRIPT="${PASTA_SCRIPT}/vivareal_raspa_processa.py"
DESTINO_ARQUIVO_SAIDA="${PASTA_SCRIPT}/imoveis_api/dados_raspados/."

GECKO_LOG="${PASTA_SCRIPT}/geckodriver.log"

UNIX_TIME=$(date +"%s")
PASTA_DADOS="${PASTA_SCRIPT}/dados/dados_${UNIX_TIME}"
ARQUIVO_SAIDA="${PASTA_DADOS}/imoveis_processados_${UNIX_TIME}.jl"


python3 $PYTHON_SCRIPT

[[ -f $GECKO_LOG ]] && rm -f $GECKO_LOG

[[ ! -d $PASTA_DADOS ]] && mkdir -p $PASTA_DADOS
mv $PASTA_SCRIPT/imoveis*.jl $PASTA_DADOS/.

[[ -f $ARQUIVO_SAIDA ]] && rm -f $ARQUIVO_SAIDA
touch $ARQUIVO_SAIDA
for arquivo in $PASTA_DADOS/imoveis_processados_*.jl; do
    cat $arquivo >> $ARQUIVO_SAIDA
done
cp -f $ARQUIVO_SAIDA $DESTINO_ARQUIVO_SAIDA
