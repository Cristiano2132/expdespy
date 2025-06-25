import pandas as pd

def load_fatorial_rcbd_np():
    """
    Carrega dados de um experimento fatorial 2×2 em delineamento em blocos completos (RCBD),
    com 5 repetições por combinação de fatores.

    Fatores:
        N (fator A): 0 (baixo), 1 (alto)
        P (fator B): 0 (baixo), 1 (alto)

    Retorna:
        df (pd.DataFrame): colunas ['block', 'N', 'P', 'produtividade']
        description (dict): metadata com 'response', 'factors', etc.
    """
    data = []
    valores = {
        (0,0): [10.5, 11.0, 9.8, 11.2, 9.9],
        (0,1): [11.2, 11.0, 10.4, 13.1, 10.6],
        (1,0): [11.5, 12.4, 10.2, 12.7, 10.4],
        (1,1): [14.0, 14.1, 13.8, 13.5, 14.2],
    }
    for i, ((n, p), obs) in enumerate(valores.items()):
        for rep, y in enumerate(obs, start=1):
            data.append({'block': rep, 'N': n, 'P': p, 'produtividade': y})

    df = pd.DataFrame(data)
    desc = """
        Dados de um experimento fatorial 2×2 em delineamento em blocos completos (RCBD),
        com 5 repetições por combinação de fatores.
        Fatores:
            N (fator A): 0 (baixo), 1 (alto)
            P (fator B): 0 (baixo), 1 (alto)
    """
    description = {
        'description': desc,
        'response': 'produtividade',
        'factors': ['N', 'P'],
        'blocks': 'block',
        'source': 'Exemplo fictício'
    }
    return df, description