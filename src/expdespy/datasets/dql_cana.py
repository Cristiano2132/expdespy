# src/expdespy/datasets/dql_cana.py

import pandas as pd

def load_dql_cana() -> pd.DataFrame:
    """
    Dados de um experimento em Quadrado Latino (LSD) com 5 variedades de cana forrageira.

    Retorna:
        DataFrame com colunas: 'linha', 'coluna', 'tratamento', 'resposta'
    """
    data = [
        [1, 1, 'D', 432], [1, 2, 'A', 518], [1, 3, 'B', 458], [1, 4, 'C', 583], [1, 5, 'E', 331],
        [2, 1, 'C', 724], [2, 2, 'E', 478], [2, 3, 'A', 524], [2, 4, 'B', 550], [2, 5, 'D', 400],
        [3, 1, 'E', 489], [3, 2, 'B', 384], [3, 3, 'C', 556], [3, 4, 'D', 297], [3, 5, 'A', 420],
        [4, 1, 'B', 494], [4, 2, 'D', 500], [4, 3, 'E', 313], [4, 4, 'A', 486], [4, 5, 'C', 501],
        [5, 1, 'A', 515], [5, 2, 'C', 660], [5, 3, 'D', 438], [5, 4, 'E', 394], [5, 5, 'B', 318],
    ]

    df = pd.DataFrame(data, columns=["linha", "coluna", "tratamento", "resposta"])
    desc = "Experimento em Quadrado Latino (LSD) com 5 variedades de cana forrageira."
    description = {'description': desc,
                'source': "Fictício",
                'response': "resposta",
                'trat': "tratamento",
                'rows': "linha",
                'cols': "coluna",
                }
    
    return df, description