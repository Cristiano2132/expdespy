# src/expdespy/datasets/fatorial_dic_irrigacao.py

import pandas as pd


def load_fatorial_dic_nitrogenio_fosforo():
    """
    Carrega dados de experimento fatorial em CRD com dois fatores:
    Nitrogênio (f1) e Fósforo (f2), ambos com dois níveis (0 = dose baixa, 1 = dose alta),
    com 5 repetições por combinação.

    Returns:
        Tuple[pd.DataFrame, dict]: Dados e metadados do experimento.
    """
    data = {
        "f1": [0]*10 + [1]*10,
        "f2": [0]*5 + [1]*5 + [0]*5 + [1]*5,
        "produtividade": [
            10.5, 11.0, 9.8, 11.2, 9.9,    # N0P0
            11.2, 11.0, 10.4, 13.1, 10.6,  # N0P1
            11.5, 12.4, 10.2, 12.7, 10.4,  # N1P0
            14.0, 14.1, 13.8, 13.5, 14.2   # N1P1
        ]
    }

    description = {
        'description': """
            Dados de experimento fatorial em CRD com dois fatores:
            Nitrogênio (f1) e Fósforo (f2), ambos com dois níveis (0 = dose baixa, 1 = dose alta),
            com 5 repetições por combinação.
        """,
        'source': "Fictício",
        'response': "produtividade",
        'factors': ["f1", "f2"],
        'levels': {
            'f1': {0: 'baixa dose de N', 1: 'alta dose de N'},
            'f2': {0: 'baixa dose de P', 1: 'alta dose de P'}
        }
    }

    df = pd.DataFrame(data)
    return df, description