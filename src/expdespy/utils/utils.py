import pandas as pd
import string
from typing import Optional, Union, List


def get_summary(df: pd.DataFrame):
    df_summary = pd.DataFrame(columns=[
                            'clumn_dtype', 'na', 'na_pct', 'top_class', 'top_class_pct', 'nunique', 'unique_values'])
    for col in df.columns:
        df_summary.at[col, 'clumn_dtype'] = df[col].dtype
        df_summary.at[col, 'na'] = df[col].isna().sum()
        na_pct = df[col].isna().sum() / len(df)*100
        df_summary.at[col, 'na_pct'] = na_pct
        if na_pct == 100:
            df_summary.at[col, 'top_class'] = '...'
            df_summary.at[col, 'top_class_pct'] = '...'
        else:
            df_summary.at[col, 'top_class'] = df[col].value_counts().index[0]
            df_summary.at[col, 'top_class_pct'] = df[col].value_counts(
            ).values[0] / len(df)*100
        df_summary.at[col, 'nunique'] = df[col].nunique()
        if df[col].nunique() < 10:
            df_summary.at[col, 'unique_values'] = df[col].unique().tolist()
        else:
            df_summary.at[col, 'unique_values'] = '...'
    return df_summary


# 3. Função assign_letters para atribuir letras aos grupos para testes post hoc

def assign_letters(
    df_post_hoc: pd.DataFrame,
    G1: str,
    G2: str,
    P: str,
    alpha: float = 0.05,
    order: Optional[Union[str, List[str]]] = None,
    data: Optional[pd.DataFrame] = None,
    vals: Optional[str] = None,
    group: Optional[str] = None,
    param: bool = True
) -> pd.DataFrame:
    """
    Atribui letras de significância aos grupos de um teste post hoc
    (como Tukey HSD), com base nos p-values das comparações.

    Essa função gera um `Compact Letter Display` (CLD), atribuindo
    letras a grupos que não são significativamente diferentes entre si.

    Args:
        df_post_hoc (pd.DataFrame): DataFrame com os resultados do teste post hoc.
        G1 (str): Nome da coluna com o primeiro grupo da comparação.
        G2 (str): Nome da coluna com o segundo grupo da comparação.
        P (str): Nome da coluna contendo os valores de p-value.
        alpha (float, optional): Nível de significância para o teste. Default é 0.05.
        order (str or list, optional): Ordem dos grupos. Pode ser "ascending", "descending",
            uma lista com a ordem desejada, ou None (ordem alfabética).
        data (pd.DataFrame, optional): DataFrame original com os dados para ordenar por média.
        vals (str, optional): Nome da coluna de valores (ex: resposta) no DataFrame original.
        group (str, optional): Nome da coluna de grupos no DataFrame original.
        param (bool, optional): Usar média (True) ou mediana (False) para ordenar grupos
            quando `order` for "ascending"/"descending".

    Returns:
        pd.DataFrame: DataFrame com os grupos como índice e as letras de significância atribuídas.
    """

    # Função auxiliar para verificar se há diferença significativa entre dois grupos
    def is_significant(lv1, lv2, df=df_post_hoc, alpha=alpha) -> bool:
        match = df.loc[
            ((df[G1] == lv1) & (df[G2] == lv2)) |
            ((df[G1] == lv2) & (df[G2] == lv1)),
            P
        ]
        return not match.empty and match.iloc[0] < alpha

    letters = string.ascii_lowercase
    df_post_hoc[P] = df_post_hoc[P].apply(pd.to_numeric)

    # Determina a ordem dos grupos
    if order is None:
        order = sorted(
            set(df_post_hoc[G1].tolist() + df_post_hoc[G2].tolist()))
    elif isinstance(order, str) and order in ['ascending', 'descending']:
        if data is None or vals is None or group is None:
            raise ValueError(
                "Para ordenação por média/mediana, forneça `data`, `vals` e `group`.")
        ascending = order == 'ascending'
        data = data.copy()
        data[vals] = data[vals].apply(pd.to_numeric)
        group_stats = data.groupby(group)[vals].mean(
        ) if param else data.groupby(group)[vals].median()
        order = group_stats.sort_values(ascending=ascending).index.tolist()

    # Atribuição das letras com base em significância
    draft: dict[int, set[str]] = {}
    sets: List[set[str]] = []
    for i, l1 in enumerate(order):
        draft[i] = {l1}
        for l2 in order:
            if l1 != l2 and not any([
                is_significant(l1, l2),
                *[is_significant(l_, l2) for l_ in draft[i]]
            ]):
                draft[i].add(l2)
    [sets.append(s) for s in draft.values() if s not in sets]

    # Cria o DataFrame final com as letras
    cld = pd.DataFrame(columns=['Group', 'Letters'])
    for i, lt in enumerate(order):
        cld.loc[i, ['Group', 'Letters']] = lt, ''.join([
            letters[j] for j, s in enumerate(sets) if lt in s
        ])

    return cld.set_index('Group')
