AUTH="./auth.sh"
if [[ -f $AUTH ]]; then
    source $AUTH
else
    echo "O arquivo $AUTH não existe"
    exit 1
fi

REQUEST_METHOD="POST"
HEADER="Content-Type: application/json; charset=utf-8"

curl_func() {
    curl \
        "$1" \
        --request "$REQUEST_METHOD" \
        --header "$HEADER" \
        --user "$API_USER":"$API_PASSWORD" \
        --data "$2"
}
