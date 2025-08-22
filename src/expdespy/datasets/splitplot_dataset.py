import pandas as pd

def load_splitplot_dic():
    """
    Carrega dados simulados para um experimento em parcelas subdivididas em CRD.
    
    Fatores:
        - Cultivar (parcela): A, B
        - Adubo (subparcela): 0, 1, 2
    3 repetições por combinação.
    
    Retorna:
        df (pd.DataFrame): colunas ['cultivar', 'adubo', 'produtividade']
        description (dict): metadados do experimento
    """
    data = []
    valores = {
        ("A", 0): [20.1, 20.3, 19.8],
        ("A", 1): [22.5, 23.0, 22.1],
        ("A", 2): [24.8, 25.0, 24.5],
        ("B", 0): [19.5, 18.9, 19.8],
        ("B", 1): [21.0, 20.7, 21.3],
        ("B", 2): [22.0, 21.9, 22.4],
    }
    for (cultivar, adubo), obs in valores.items():
        for y in obs:
            data.append({'cultivar': cultivar, 'adubo': adubo, 'produtividade': y})
    
    df = pd.DataFrame(data)
    desc = """
        Experimento com parcelas subdivididas (CRD): fator principal = Cultivar, subparcela = Adubo.
        3 repetições por combinação.
    """
    description = {
        'description': desc,
        'response': 'produtividade',
        'main_plot': 'cultivar',
        'subplot': 'adubo',
        'source': 'Exemplo fictício - CRD',
    }
    return df, description


def load_splitplot_dbc():
    """
    Carrega dados simulados para um experimento em parcelas subdivididas em RCBD.
    
    Fatores:
        - Cultivar (parcela): A, B
        - Adubo (subparcela): 0, 1, 2
    Blocos: 1, 2, 3
    
    Retorna:
        df (pd.DataFrame): colunas ['block', 'cultivar', 'adubo', 'produtividade']
        description (dict): metadados do experimento
    """
    data = []
    blocks = [1, 2, 3]
    for block in blocks:
        for cultivar in ["A", "B"]:
            for adubo in [0, 1, 2]:
                media = {
                    ("A", 0): 20,
                    ("A", 1): 22.5,
                    ("A", 2): 25,
                    ("B", 0): 19,
                    ("B", 1): 21,
                    ("B", 2): 22,
                }[(cultivar, adubo)]
                y = media + pd.Series([0.2, -0.1, 0.3]).sample(1).iloc[0]
                data.append({
                    'block': block,
                    'cultivar': cultivar,
                    'adubo': adubo,
                    'produtividade': round(y, 2),
                })
    
    df = pd.DataFrame(data)
    desc = """
        Experimento com parcelas subdivididas (RCBD): fator principal = Cultivar, subparcela = Adubo.
        3 blocos (repetições).
    """
    description = {
        'description': desc,
        'response': 'produtividade',
        'main_plot': 'cultivar',
        'subplot': 'adubo',
        'block': 'block',
        'source': 'Exemplo fictício - RCBD',
    }
    return df, description