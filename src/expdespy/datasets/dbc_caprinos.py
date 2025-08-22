# src/expdespy/datasets/dbc_caprinos.py

import pandas as pd


def load_dbc_caprinos() -> tuple[pd.DataFrame, str]:
    """
    Exemplo clássico de RCBD (Delineamento em Blocos Casualizados) com 5 produtos comerciais
    aplicados a grupos de caprinos separados em 3 blocos por faixa etária. A variável resposta
    é a concentração de micronutrientes no sangue (ppm).
    """
    data = {
        "bloco": [1]*5 + [2]*5 + [3]*5,
        "produto": [1, 2, 3, 4, 5]*3,
        "ppm_micronutriente": [
            83, 86, 103, 116, 132,  # bloco 1
            63, 69, 79, 81, 98,     # bloco 2
            55, 61, 79, 79, 91      # bloco 3
        ]
    }
    df = pd.DataFrame(data)
    desc = (
        "Experimento com 5 produtos comerciais fornecidos a caprinos organizados em 3 blocos "
        "de acordo com a idade. A variável resposta é a concentração de micronutrientes no sangue (ppm). "
        "Usado para análise com RCBD."
    )
    descricao = {
        'description': desc,
        'source': "Fictício",
        'response': "ppm_micronutriente",
        'trat': "produto",
        'block': "bloco"
    }
    return df, descricao
