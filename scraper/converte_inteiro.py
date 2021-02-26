def converte_inteiro(string):
    try:
        return int(string)
    except (TypeError, ValueError):
        return None
