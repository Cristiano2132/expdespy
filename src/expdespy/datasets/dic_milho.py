# src/expdespy/datasets/dic_milho.py

import pandas as pd

def load_dic_milho() -> tuple[pd.DataFrame, str]:
    """
    Exemplo clássico de DIC (Delineamento Inteiramente Casualizado) com 4 variedades de milho
    e 5 repetições. A variável resposta é a produtividade (em sacas/ha).
    """
    data = {
        "variedade": ["A"] * 5 + ["B"] * 5 + ["C"] * 5 + ["D"] * 5,
        "produtividade": [
            25, 26, 20, 23, 21,  # A
            31, 25, 28, 27, 24,  # B
            22, 26, 28, 25, 29,  # C
            33, 29, 31, 34, 28   # D
        ]
    }
    df = pd.DataFrame(data)
    descricao = (
        "Experimento com 4 variedades de milho (A, B, C, D) distribuídas aleatoriamente "
        "em 20 parcelas (5 por variedade). A variável resposta é a produtividade em sacas por hectare. "
        "Usado para análise com DIC e testes de comparação múltipla."
    )
    return df, descricao