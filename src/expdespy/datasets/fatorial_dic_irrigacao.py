# src/expdespy/datasets/fatorial_dic_irrigacao.py

import pandas as pd


def load_fatorial_dic():
    """
    Carrega dados do experimento fatorial em CRD com dois fatores:
    Irrigação (f1) e Calagem (f2), ambos com dois níveis (0 = ausência, 1 = presença).
    
    Retorna:
        Tuple[pd.DataFrame, str]: dataframe com os dados e nome da variável resposta.
    """
    data = {
        "f1": [0]*6 + [1]*6,
        "f2": [0, 0, 0, 1, 1, 1] * 2,
        "produtividade": [
            25, 32, 27, 35, 28, 33,  # A0B0 e A0B1
            41, 35, 38, 60, 67, 59   # A1B0 e A1B1
        ]
    }
    description = {'description': """
        Dados de um experimento fatorial em CRD com dois fatores:
        Irrigação (f1) e Calagem (f2), ambos com dois níveis (0 = ausência, 1 = presença).
    """,
                'source': "Fictício",
                'response': "produtividade",
                'factors': ["f1", "f2"],
                'levels': {
                    'f1': {0: 'ausência', 1: 'presença'},
                    'f2': {0: 'ausência', 1: 'presença'}
                }
    }
    df = pd.DataFrame(data)
    return df, description