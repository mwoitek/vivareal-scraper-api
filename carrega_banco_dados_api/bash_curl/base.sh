#!/bin/bash

FUNCAO_CURL="./curl_func.sh"
if [[ -f $FUNCAO_CURL ]]; then
    source $FUNCAO_CURL
else
    echo "O arquivo $FUNCAO_CURL não existe"
    exit 1
fi

