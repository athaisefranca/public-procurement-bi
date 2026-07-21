"""Preparação da camada estatística da base sintética de compras públicas."""

from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_STATISTICAL_COLUMNS: list[str] = [
    "process_id",
    "item_id",
    "publication_date",
    "organization_code",
    "purchase_modality",
    "category",
    "item_description",
    "quantity",
    "estimated_unit_value",
    "estimated_total_value",
    "status",
]

CATEGORICAL_COLUMNS: list[str] = [
    "purchase_modality",
    "category",
    "status",
]

NUMERIC_COLUMNS: list[str] = [
    "quantity",
    "estimated_unit_value",
    "estimated_total_value",
]


def load_treated_data(file_path: str) -> pd.DataFrame:
    """Lê a base tratada usada no perfil estatístico.

    Args:
        file_path: Caminho do arquivo CSV tratado.

    Returns:
        DataFrame com os registros da base tratada.

    Raises:
        TypeError: Se file_path não for uma string.
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o arquivo estiver vazio.
    """
    if not isinstance(file_path, str):
        raise TypeError(
            "O caminho do arquivo deve ser fornecido como texto."
        )

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo tratado não encontrado: {file_path}"
        )

    data = pd.read_csv(path)

    if data.empty:
        raise ValueError("A base tratada está vazia.")

    return data


def validate_statistical_columns(data: pd.DataFrame) -> None:
    """Verifica as colunas necessárias para o perfil estatístico.

    Args:
        data: DataFrame da base tratada.

    Raises:
        TypeError: Se data não for um DataFrame.
        ValueError: Se alguma coluna obrigatória estiver ausente.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Os dados devem ser fornecidos em um DataFrame.")

    missing_columns = [
        column
        for column in REQUIRED_STATISTICAL_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas estatísticas ausentes: {missing_text}"
        )


def prepare_statistical_base(data: pd.DataFrame) -> pd.DataFrame:
    """Valida tipos, ausências e chaves da base estatística.

    Args:
        data: DataFrame da base tratada.

    Returns:
        Cópia validada e preparada para os cálculos estatísticos.

    Raises:
        TypeError: Se data não for um DataFrame.
        ValueError: Se houver ausências, tipos inválidos ou duplicidades.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Os dados devem ser fornecidos em um DataFrame.")

    validate_statistical_columns(data)

    prepared_data = data.copy()

    missing_counts = (
        prepared_data[REQUIRED_STATISTICAL_COLUMNS]
        .isna()
        .sum()
    )

    columns_with_missing = missing_counts[
        missing_counts > 0
    ]

    if not columns_with_missing.empty:
        missing_text = ", ".join(
            [
                f"{column}={int(count)}"
                for column, count in columns_with_missing.items()
            ]
        )
        raise ValueError(
            f"Valores ausentes na base tratada: {missing_text}"
        )

    for column in NUMERIC_COLUMNS:
        prepared_data[column] = pd.to_numeric(
            prepared_data[column],
            errors="coerce",
        )

        if prepared_data[column].isna().any():
            raise ValueError(
                f"Valores não numéricos encontrados em {column}."
            )

    duplicate_count = int(
        prepared_data.duplicated(
            subset=["process_id", "item_id"]
        ).sum()
    )

    if duplicate_count > 0:
        raise ValueError(
            "Foram encontradas chaves duplicadas na base tratada: "
            f"{duplicate_count}"
        )

    prepared_data["publication_date"] = pd.to_datetime(
        prepared_data["publication_date"],
        format="%Y-%m-%d",
        errors="coerce",
    )

    if prepared_data["publication_date"].isna().any():
        raise ValueError(
            "Foram encontradas datas inválidas na base tratada."
        )

    return prepared_data


def classify_variables() -> dict[str, list[str]]:
    """Documenta a classificação das variáveis da camada estatística.

    Returns:
        Dicionário com os grupos de variáveis usados na análise.
    """
    return {
        "identificadores": [
            "process_id",
            "item_id",
            "organization_code",
        ],
        "data": [
            "publication_date",
        ],
        "qualitativas_nominais": CATEGORICAL_COLUMNS,
        "quantitativas": NUMERIC_COLUMNS,
        "texto_descritivo": [
            "item_description",
        ],
    }


def build_initial_diagnostic(
    data: pd.DataFrame,
) -> dict[str, int]:
    """Cria o diagnóstico inicial da granularidade da base.

    Args:
        data: DataFrame validado da base tratada.

    Returns:
        Dicionário com contagens estruturais da base.

    Raises:
        TypeError: Se data não for um DataFrame.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Os dados devem ser fornecidos em um DataFrame.")

    unique_keys = (
        data[["process_id", "item_id"]]
        .drop_duplicates()
        .shape[0]
    )

    return {
        "total_items": int(data.shape[0]),
        "distinct_processes": int(
            data["process_id"].nunique()
        ),
        "unique_process_item_keys": int(unique_keys),
        "duplicate_process_item_keys": int(
            data.duplicated(
                subset=["process_id", "item_id"]
            ).sum()
        ),
    }


def build_frequency_profile(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Calcula frequências absolutas e percentuais das categorias.

    Args:
        data: DataFrame validado da base tratada.

    Returns:
        DataFrame em formato longo com variável, categoria,
        frequência absoluta e percentual.

    Raises:
        TypeError: Se data não for um DataFrame.
        ValueError: Se alguma coluna categórica estiver ausente.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Os dados devem ser fornecidos em um DataFrame.")

    missing_columns = [
        column
        for column in CATEGORICAL_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas categóricas ausentes: {missing_text}"
        )

    frequency_tables: list[pd.DataFrame] = []

    for column in CATEGORICAL_COLUMNS:
        absolute_frequency = (
            data[column]
            .value_counts(dropna=False)
            .rename("absolute_frequency")
        )

        percentage = (
            data[column]
            .value_counts(
                normalize=True,
                dropna=False,
            )
            .mul(100)
            .round(2)
            .rename("percentage")
        )

        table = pd.concat(
            [absolute_frequency, percentage],
            axis=1,
        ).reset_index()

        table = table.rename(
            columns={
                column: "category_value",
                "index": "category_value",
            }
        )

        table.insert(0, "variable", column)

        frequency_tables.append(table)

    return pd.concat(
        frequency_tables,
        ignore_index=True,
    )


def validate_frequency_profile(
    frequency_profile: pd.DataFrame,
    expected_total: int,
) -> None:
    """Valida os totais das tabelas de frequência.

    Args:
        frequency_profile: Tabela de frequências calculada.
        expected_total: Quantidade esperada de registros por variável.

    Raises:
        TypeError: Se os argumentos tiverem tipos incompatíveis.
        ValueError: Se frequências ou percentuais não fecharem.
    """
    if not isinstance(frequency_profile, pd.DataFrame):
        raise TypeError(
            "O perfil de frequências deve ser um DataFrame."
        )

    if not isinstance(expected_total, int):
        raise TypeError(
            "O total esperado deve ser um número inteiro."
        )

    required_columns = [
        "variable",
        "category_value",
        "absolute_frequency",
        "percentage",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in frequency_profile.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas ausentes no perfil de frequências: {missing_text}"
        )

    for variable in CATEGORICAL_COLUMNS:
        variable_data = frequency_profile[
            frequency_profile["variable"] == variable
        ]

        absolute_total = int(
            variable_data["absolute_frequency"].sum()
        )

        percentage_total = float(
            variable_data["percentage"].sum()
        )

        if absolute_total != expected_total:
            raise ValueError(
                f"A frequência de {variable} não corresponde "
                f"ao total esperado: {absolute_total}."
            )

        if not np.isclose(
            percentage_total,
            100.0,
            atol=0.05,
        ):
            raise ValueError(
                f"Os percentuais de {variable} não totalizam "
                f"aproximadamente 100%: {percentage_total:.2f}%."
            )


def write_frequency_profile(
    frequency_profile: pd.DataFrame,
    output_path: str,
) -> None:
    """Grava o perfil de frequências em CSV.

    Args:
        frequency_profile: Tabela de frequências calculada.
        output_path: Caminho do arquivo de saída.

    Raises:
        TypeError: Se os argumentos tiverem tipos incompatíveis.
    """
    if not isinstance(frequency_profile, pd.DataFrame):
        raise TypeError(
            "O perfil de frequências deve ser um DataFrame."
        )

    if not isinstance(output_path, str):
        raise TypeError(
            "O caminho de saída deve ser fornecido como texto."
        )

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    frequency_profile.to_csv(
        path,
        index=False,
        encoding="utf-8",
    )


def build_numeric_profile(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Calcula medidas descritivas das variáveis quantitativas.

    Args:
        data: DataFrame validado da base tratada.

    Returns:
        DataFrame com uma linha para cada variável numérica.

    Raises:
        TypeError: Se data não for um DataFrame.
        ValueError: Se alguma coluna numérica estiver ausente,
            vazia ou contiver valor não numérico.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Os dados devem ser fornecidos em um DataFrame.")

    missing_columns = [
        column
        for column in NUMERIC_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas numéricas ausentes: {missing_text}"
        )

    profile_rows: list[dict[str, str | int | float]] = []

    for column in NUMERIC_COLUMNS:
        numeric_series = pd.to_numeric(
            data[column],
            errors="coerce",
        ).dropna()

        if numeric_series.empty:
            raise ValueError(
                f"A coluna {column} não possui valores numéricos válidos."
            )

        if numeric_series.shape[0] != data.shape[0]:
            raise ValueError(
                f"A coluna {column} contém valores ausentes "
                "ou não numéricos."
            )

        mean_value = float(numeric_series.mean())
        q1 = float(numeric_series.quantile(0.25))
        q3 = float(numeric_series.quantile(0.75))

        profile_rows.append(
            {
                "variable": column,
                "count": int(numeric_series.count()),
                "mean": round(mean_value, 2),
                "median": round(
                    float(numeric_series.median()),
                    2,
                ),
                "q1": round(q1, 2),
                "q3": round(q3, 2),
                "iqr": round(q3 - q1, 2),
                "p90": round(
                    float(numeric_series.quantile(0.90)),
                    2,
                ),
                "p95": round(
                    float(numeric_series.quantile(0.95)),
                    2,
                ),
                "mean_absolute_deviation": round(
                    float(
                        (
                            numeric_series - mean_value
                        )
                        .abs()
                        .mean()
                    ),
                    2,
                ),
                "population_variance": round(
                    float(numeric_series.var(ddof=0)),
                    2,
                ),
                "population_std": round(
                    float(numeric_series.std(ddof=0)),
                    2,
                ),
                "minimum": round(
                    float(numeric_series.min()),
                    2,
                ),
                "maximum": round(
                    float(numeric_series.max()),
                    2,
                ),
            }
        )

    return pd.DataFrame(profile_rows)


def validate_numeric_profile(
    numeric_profile: pd.DataFrame,
    expected_count: int,
) -> None:
    """Valida consistência e ordenação das medidas numéricas.

    Args:
        numeric_profile: Perfil numérico calculado.
        expected_count: Quantidade esperada de observações.

    Raises:
        TypeError: Se os argumentos tiverem tipos incompatíveis.
        ValueError: Se alguma medida estiver inconsistente.
    """
    if not isinstance(numeric_profile, pd.DataFrame):
        raise TypeError(
            "O perfil numérico deve ser um DataFrame."
        )

    if not isinstance(expected_count, int):
        raise TypeError(
            "A contagem esperada deve ser um número inteiro."
        )

    required_columns = [
        "variable",
        "count",
        "mean",
        "median",
        "q1",
        "q3",
        "iqr",
        "p90",
        "p95",
        "mean_absolute_deviation",
        "population_variance",
        "population_std",
        "minimum",
        "maximum",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in numeric_profile.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas ausentes no perfil numérico: {missing_text}"
        )

    for _, row in numeric_profile.iterrows():
        variable = str(row["variable"])

        if int(row["count"]) != expected_count:
            raise ValueError(
                f"A contagem de {variable} não corresponde "
                f"ao total esperado: {int(row['count'])}."
            )

        if not (
            float(row["minimum"])
            <= float(row["q1"])
            <= float(row["median"])
            <= float(row["q3"])
            <= float(row["maximum"])
        ):
            raise ValueError(
                f"Separatrizes inconsistentes em {variable}."
            )

        expected_iqr = round(
            float(row["q3"]) - float(row["q1"]),
            2,
        )

        if not np.isclose(
            float(row["iqr"]),
            expected_iqr,
            atol=0.01,
        ):
            raise ValueError(
                f"Intervalo interquartil inconsistente "
                f"em {variable}."
            )

        if float(row["p90"]) > float(row["p95"]):
            raise ValueError(
                f"P90 maior que P95 em {variable}."
            )

        non_negative_columns = [
            "mean_absolute_deviation",
            "population_variance",
            "population_std",
        ]

        for column in non_negative_columns:
            if float(row[column]) < 0:
                raise ValueError(
                    f"{column} não pode ser negativo "
                    f"em {variable}."
                )


def write_numeric_profile(
    numeric_profile: pd.DataFrame,
    output_path: str,
) -> None:
    """Grava o perfil numérico em arquivo CSV.

    Args:
        numeric_profile: Perfil estatístico calculado.
        output_path: Caminho do arquivo de saída.

    Raises:
        TypeError: Se os argumentos tiverem tipos incompatíveis.
    """
    if not isinstance(numeric_profile, pd.DataFrame):
        raise TypeError(
            "O perfil numérico deve ser um DataFrame."
        )

    if not isinstance(output_path, str):
        raise TypeError(
            "O caminho de saída deve ser fornecido como texto."
        )

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    numeric_profile.to_csv(
        path,
        index=False,
        encoding="utf-8",
    )


def build_group_profile(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Compara o valor total estimado por modalidade e categoria.

    Args:
        data: DataFrame validado da base tratada.

    Returns:
        DataFrame com estatísticas descritivas por grupo.

    Raises:
        TypeError: Se data não for um DataFrame.
        ValueError: Se alguma coluna necessária estiver ausente.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Os dados devem ser fornecidos em um DataFrame.")

    group_columns = [
        "purchase_modality",
        "category",
    ]

    required_columns = group_columns + [
        "estimated_total_value",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas ausentes para comparação por grupo: "
            f"{missing_text}"
        )

    group_rows: list[
        dict[str, str | int | float]
    ] = []

    for group_column in group_columns:
        group_values = sorted(
            data[group_column].dropna().unique()
        )

        for group_value in group_values:
            group_data = data[
                data[group_column] == group_value
            ]

            numeric_series = pd.to_numeric(
                group_data["estimated_total_value"],
                errors="coerce",
            ).dropna()

            if numeric_series.empty:
                raise ValueError(
                    "Grupo sem valores numéricos válidos: "
                    f"{group_column}={group_value}"
                )

            mean_value = float(numeric_series.mean())
            q1 = float(numeric_series.quantile(0.25))
            q3 = float(numeric_series.quantile(0.75))

            group_rows.append(
                {
                    "group_variable": group_column,
                    "group_value": str(group_value),
                    "count": int(numeric_series.count()),
                    "mean": round(mean_value, 2),
                    "median": round(
                        float(numeric_series.median()),
                        2,
                    ),
                    "q1": round(q1, 2),
                    "q3": round(q3, 2),
                    "iqr": round(q3 - q1, 2),
                    "p90": round(
                        float(
                            numeric_series.quantile(0.90)
                        ),
                        2,
                    ),
                    "population_std": round(
                        float(
                            numeric_series.std(ddof=0)
                        ),
                        2,
                    ),
                    "minimum": round(
                        float(numeric_series.min()),
                        2,
                    ),
                    "maximum": round(
                        float(numeric_series.max()),
                        2,
                    ),
                }
            )

    return pd.DataFrame(group_rows)


def validate_group_profile(
    group_profile: pd.DataFrame,
    expected_total: int,
) -> None:
    """Valida as contagens e medidas do perfil por grupo.

    Args:
        group_profile: Perfil estatístico por grupo.
        expected_total: Total esperado de itens por dimensão.

    Raises:
        TypeError: Se os argumentos tiverem tipos incompatíveis.
        ValueError: Se as contagens ou medidas forem inconsistentes.
    """
    if not isinstance(group_profile, pd.DataFrame):
        raise TypeError(
            "O perfil por grupo deve ser um DataFrame."
        )

    if not isinstance(expected_total, int):
        raise TypeError(
            "O total esperado deve ser um número inteiro."
        )

    required_columns = [
        "group_variable",
        "group_value",
        "count",
        "mean",
        "median",
        "q1",
        "q3",
        "iqr",
        "p90",
        "population_std",
        "minimum",
        "maximum",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in group_profile.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas ausentes no perfil por grupo: "
            f"{missing_text}"
        )

    for group_variable in [
        "purchase_modality",
        "category",
    ]:
        variable_data = group_profile[
            group_profile["group_variable"]
            == group_variable
        ]

        total_count = int(
            variable_data["count"].sum()
        )

        if total_count != expected_total:
            raise ValueError(
                f"A soma dos grupos de {group_variable} "
                f"não corresponde ao total esperado: "
                f"{total_count}."
            )

    for _, row in group_profile.iterrows():
        if not (
            float(row["minimum"])
            <= float(row["q1"])
            <= float(row["median"])
            <= float(row["q3"])
            <= float(row["maximum"])
        ):
            raise ValueError(
                "Separatrizes inconsistentes no grupo "
                f"{row['group_variable']}="
                f"{row['group_value']}."
            )

        expected_iqr = round(
            float(row["q3"]) - float(row["q1"]),
            2,
        )

        if not np.isclose(
            float(row["iqr"]),
            expected_iqr,
            atol=0.01,
        ):
            raise ValueError(
                "Intervalo interquartil inconsistente "
                f"no grupo {row['group_variable']}="
                f"{row['group_value']}."
            )

        if float(row["population_std"]) < 0:
            raise ValueError(
                "O desvio padrão não pode ser negativo "
                f"no grupo {row['group_variable']}="
                f"{row['group_value']}."
            )


def write_group_profile(
    group_profile: pd.DataFrame,
    output_path: str,
) -> None:
    """Grava o perfil estatístico por grupo em CSV.

    Args:
        group_profile: Perfil por grupo calculado.
        output_path: Caminho do arquivo de saída.

    Raises:
        TypeError: Se os argumentos tiverem tipos incompatíveis.
    """
    if not isinstance(group_profile, pd.DataFrame):
        raise TypeError(
            "O perfil por grupo deve ser um DataFrame."
        )

    if not isinstance(output_path, str):
        raise TypeError(
            "O caminho de saída deve ser fornecido como texto."
        )

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    group_profile.to_csv(
        path,
        index=False,
        encoding="utf-8",
    )


def build_outlier_candidates(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Identifica candidatos a discrepâncias pela regra do IIQ.

    Args:
        data: DataFrame validado da base tratada.

    Returns:
        DataFrame com valores fora dos limites convencionais
        de 1,5 vezes o intervalo interquartil.

    Raises:
        TypeError: Se data não for um DataFrame.
        ValueError: Se alguma coluna necessária estiver ausente.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Os dados devem ser fornecidos em um DataFrame.")

    required_columns = [
        "process_id",
        "item_id",
    ] + NUMERIC_COLUMNS

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            "Colunas ausentes para identificação de "
            f"discrepâncias: {missing_text}"
        )

    candidate_rows: list[
        dict[str, str | float]
    ] = []

    for column in NUMERIC_COLUMNS:
        numeric_series = pd.to_numeric(
            data[column],
            errors="coerce",
        )

        if numeric_series.isna().any():
            raise ValueError(
                f"A coluna {column} contém valores inválidos."
            )

        q1 = float(numeric_series.quantile(0.25))
        q3 = float(numeric_series.quantile(0.75))
        iqr = q3 - q1

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        candidate_mask = (
            (numeric_series < lower_limit)
            | (numeric_series > upper_limit)
        )

        candidates = data[candidate_mask]

        for index, record in candidates.iterrows():
            value = float(record[column])

            if value < lower_limit:
                reason = "below_lower_iqr_limit"
            else:
                reason = "above_upper_iqr_limit"

            candidate_rows.append(
                {
                    "variable": column,
                    "process_id": str(
                        record["process_id"]
                    ),
                    "item_id": str(record["item_id"]),
                    "value": round(value, 2),
                    "q1": round(q1, 2),
                    "q3": round(q3, 2),
                    "iqr": round(iqr, 2),
                    "lower_limit": round(
                        lower_limit,
                        2,
                    ),
                    "upper_limit": round(
                        upper_limit,
                        2,
                    ),
                    "reason": reason,
                }
            )

    columns = [
        "variable",
        "process_id",
        "item_id",
        "value",
        "q1",
        "q3",
        "iqr",
        "lower_limit",
        "upper_limit",
        "reason",
    ]

    return pd.DataFrame(
        candidate_rows,
        columns=columns,
    )


def validate_outlier_candidates(
    data: pd.DataFrame,
    outlier_candidates: pd.DataFrame,
) -> None:
    """Valida os candidatos sem modificar a base original.

    Args:
        data: Base tratada usada no cálculo.
        outlier_candidates: Candidatos identificados.

    Raises:
        TypeError: Se os argumentos não forem DataFrames.
        ValueError: Se algum candidato não atender à regra.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Os dados devem ser fornecidos em um DataFrame."
        )

    if not isinstance(outlier_candidates, pd.DataFrame):
        raise TypeError(
            "Os candidatos devem ser fornecidos em um DataFrame."
        )

    if data.shape[0] == 0:
        raise ValueError(
            "A base original não pode estar vazia."
        )

    for _, row in outlier_candidates.iterrows():
        value = float(row["value"])
        lower_limit = float(row["lower_limit"])
        upper_limit = float(row["upper_limit"])

        if not (
            value < lower_limit
            or value > upper_limit
        ):
            raise ValueError(
                "Candidato dentro dos limites do IIQ: "
                f"{row['variable']} | "
                f"{row['process_id']} | "
                f"{row['item_id']}."
            )


def write_outlier_candidates(
    outlier_candidates: pd.DataFrame,
    output_path: str,
) -> None:
    """Grava os candidatos a discrepâncias em CSV.

    Args:
        outlier_candidates: Tabela de candidatos.
        output_path: Caminho do arquivo de saída.

    Raises:
        TypeError: Se os argumentos tiverem tipos incompatíveis.
    """
    if not isinstance(outlier_candidates, pd.DataFrame):
        raise TypeError(
            "Os candidatos devem ser fornecidos em um DataFrame."
        )

    if not isinstance(output_path, str):
        raise TypeError(
            "O caminho de saída deve ser fornecido como texto."
        )

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    outlier_candidates.to_csv(
        path,
        index=False,
        encoding="utf-8",
    )


def write_statistical_report(
    diagnostic: dict[str, int],
    frequency_profile: pd.DataFrame,
    numeric_profile: pd.DataFrame,
    group_profile: pd.DataFrame,
    outlier_candidates: pd.DataFrame,
    output_path: str,
) -> None:
    """Gera um relatório estatístico reproduzível em Markdown.

    Args:
        diagnostic: Contagens estruturais da base.
        frequency_profile: Frequências categóricas.
        numeric_profile: Perfil das variáveis numéricas.
        group_profile: Comparações por grupo.
        outlier_candidates: Candidatos pela regra do IIQ.
        output_path: Caminho do relatório Markdown.

    Raises:
        TypeError: Se algum argumento tiver tipo incompatível.
    """
    if not isinstance(diagnostic, dict):
        raise TypeError(
            "O diagnóstico deve ser fornecido como dicionário."
        )

    dataframe_arguments = [
        frequency_profile,
        numeric_profile,
        group_profile,
        outlier_candidates,
    ]

    if not all(
        isinstance(argument, pd.DataFrame)
        for argument in dataframe_arguments
    ):
        raise TypeError(
            "Os perfis estatísticos devem ser DataFrames."
        )

    if not isinstance(output_path, str):
        raise TypeError(
            "O caminho de saída deve ser fornecido como texto."
        )

    lines: list[str] = [
        "# Relatório estatístico da base sintética",
        "",
        "## Contexto",
        "",
        "Este relatório foi gerado automaticamente a partir de "
        "`data/processed/compras_tratadas.csv`.",
        "",
        "A unidade de análise é o item de compra:",
        "",
        "> uma linha representa um item pertencente a um "
        "processo sintético.",
        "",
        "Os resultados são demonstrativos e não representam "
        "qualquer instituição real.",
        "",
        "## Diagnóstico estrutural",
        "",
        f"- Itens analisados: "
        f"{diagnostic['total_items']}",
        f"- Processos distintos: "
        f"{diagnostic['distinct_processes']}",
        f"- Chaves processo-item únicas: "
        f"{diagnostic['unique_process_item_keys']}",
        f"- Chaves duplicadas: "
        f"{diagnostic['duplicate_process_item_keys']}",
        "",
        "## Frequências categóricas",
        "",
    ]

    for variable in CATEGORICAL_COLUMNS:
        lines.append(f"### `{variable}`")
        lines.append("")

        variable_data = frequency_profile[
            frequency_profile["variable"] == variable
        ]

        for _, row in variable_data.iterrows():
            lines.append(
                f"- {row['category_value']}: "
                f"{int(row['absolute_frequency'])} itens "
                f"({float(row['percentage']):.2f}%)"
            )

        lines.append("")

    lines.extend(
        [
            "## Perfil numérico",
            "",
        ]
    )

    for _, row in numeric_profile.iterrows():
        lines.extend(
            [
                f"### `{row['variable']}`",
                "",
                f"- Contagem: {int(row['count'])}",
                f"- Média: {float(row['mean']):.2f}",
                f"- Mediana: "
                f"{float(row['median']):.2f}",
                f"- Q1: {float(row['q1']):.2f}",
                f"- Q3: {float(row['q3']):.2f}",
                f"- IIQ: {float(row['iqr']):.2f}",
                f"- P90: {float(row['p90']):.2f}",
                f"- P95: {float(row['p95']):.2f}",
                f"- Desvio médio absoluto: "
                f"{float(row['mean_absolute_deviation']):.2f}",
                f"- Variância populacional: "
                f"{float(row['population_variance']):.2f}",
                f"- Desvio padrão populacional: "
                f"{float(row['population_std']):.2f}",
                f"- Mínimo: {float(row['minimum']):.2f}",
                f"- Máximo: {float(row['maximum']):.2f}",
                "",
            ]
        )

    lines.extend(
        [
            "## Comparação do valor total estimado",
            "",
            "As comparações abaixo permanecem no nível de item.",
            "",
        ]
    )

    for group_variable in [
        "purchase_modality",
        "category",
    ]:
        lines.append(f"### Por `{group_variable}`")
        lines.append("")

        variable_data = group_profile[
            group_profile["group_variable"]
            == group_variable
        ]

        for _, row in variable_data.iterrows():
            lines.append(
                f"- {row['group_value']}: "
                f"n={int(row['count'])}, "
                f"média={float(row['mean']):.2f}, "
                f"mediana={float(row['median']):.2f}, "
                f"P90={float(row['p90']):.2f}, "
                f"desvio padrão populacional="
                f"{float(row['population_std']):.2f}"
            )

        lines.append("")

    lines.extend(
        [
            "## Candidatos a discrepâncias",
            "",
            "A identificação utiliza os limites convencionais "
            "`Q1 - 1,5 × IIQ` e `Q3 + 1,5 × IIQ`.",
            "",
            "Os registros não foram removidos nem corrigidos "
            "automaticamente.",
            "",
            f"Total de ocorrências identificadas: "
            f"{outlier_candidates.shape[0]}",
            "",
        ]
    )

    for variable in NUMERIC_COLUMNS:
        variable_data = outlier_candidates[
            outlier_candidates["variable"] == variable
        ]

        lines.append(f"### `{variable}`")
        lines.append("")

        if variable_data.empty:
            lines.append(
                "- Nenhum candidato identificado."
            )
        else:
            for _, row in variable_data.iterrows():
                lines.append(
                    f"- {row['process_id']} / "
                    f"{row['item_id']}: "
                    f"valor={float(row['value']):.2f}; "
                    f"limite superior="
                    f"{float(row['upper_limit']):.2f}"
                )

        lines.append("")

    lines.extend(
        [
            "## Limitações",
            "",
            "- A base contém somente 30 itens sintéticos.",
            "- Os grupos possuem poucas observações.",
            "- Média, percentis e dispersão podem ser fortemente "
            "influenciados pelos maiores valores.",
            "- Candidato a discrepância não significa erro.",
            "- Não existe valor homologado nesta versão da base.",
            "- Não devem ser feitas generalizações externas.",
            "",
        ]
    )

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def run_initial_profile() -> None:
    """Executa a preparação inicial da camada estatística."""
    input_path = "data/processed/compras_tratadas.csv"

    data = load_treated_data(input_path)
    prepared_data = prepare_statistical_base(data)

    diagnostic = build_initial_diagnostic(
        prepared_data
    )

    variable_classes = classify_variables()

    frequency_profile = build_frequency_profile(
        prepared_data
    )

    validate_frequency_profile(
        frequency_profile,
        expected_total=int(prepared_data.shape[0]),
    )

    write_frequency_profile(
        frequency_profile,
        "reports/statistics/frequency_profile.csv",
    )

    numeric_profile = build_numeric_profile(
        prepared_data
    )

    validate_numeric_profile(
        numeric_profile,
        expected_count=int(prepared_data.shape[0]),
    )

    write_numeric_profile(
        numeric_profile,
        "reports/statistics/numeric_profile.csv",
    )

    group_profile = build_group_profile(
        prepared_data
    )

    validate_group_profile(
        group_profile,
        expected_total=int(prepared_data.shape[0]),
    )

    write_group_profile(
        group_profile,
        "reports/statistics/group_profile.csv",
    )

    outlier_candidates = build_outlier_candidates(
        prepared_data
    )

    validate_outlier_candidates(
        prepared_data,
        outlier_candidates,
    )

    write_outlier_candidates(
        outlier_candidates,
        "reports/statistics/outlier_candidates.csv",
    )

    write_statistical_report(
        diagnostic=diagnostic,
        frequency_profile=frequency_profile,
        numeric_profile=numeric_profile,
        group_profile=group_profile,
        outlier_candidates=outlier_candidates,
        output_path=(
            "reports/statistics/"
            "statistical_report.md"
        ),
    )

    print("CAMADA ESTATÍSTICA PREPARADA")
    print("============================")
    print(f"pandas: {pd.__version__}")
    print(f"numpy: {np.__version__}")
    print(f"Itens analisados: {diagnostic['total_items']}")
    print(
        "Processos distintos: "
        f"{diagnostic['distinct_processes']}"
    )
    print(
        "Chaves processo-item únicas: "
        f"{diagnostic['unique_process_item_keys']}"
    )
    print(
        "Chaves processo-item duplicadas: "
        f"{diagnostic['duplicate_process_item_keys']}"
    )

    print("----------------------------")
    print("CLASSIFICAÇÃO DAS VARIÁVEIS")

    for group_name, columns in variable_classes.items():
        columns_text = ", ".join(columns)
        print(f"{group_name}: {columns_text}")

    print("----------------------------")
    print("FREQUÊNCIAS CATEGÓRICAS GERADAS")
    print(
        "Arquivo: "
        "reports/statistics/frequency_profile.csv"
    )

    for variable in CATEGORICAL_COLUMNS:
        category_count = int(
            frequency_profile[
                frequency_profile["variable"] == variable
            ].shape[0]
        )

        print(
            f"{variable}: "
            f"{category_count} categorias"
        )

        print("----------------------------")
    print("PERFIL NUMÉRICO GERADO")
    print(
        "Arquivo: "
        "reports/statistics/numeric_profile.csv"
    )

    for _, row in numeric_profile.iterrows():
        print(
            f"{row['variable']}: "
            f"média={row['mean']:.2f} | "
            f"mediana={row['median']:.2f} | "
            f"P90={row['p90']:.2f} | "
            f"P95={row['p95']:.2f}"
        )

    print("----------------------------")
    print("COMPARAÇÕES POR GRUPO GERADAS")
    print(
        "Arquivo: "
        "reports/statistics/group_profile.csv"
    )

    for group_variable in [
        "purchase_modality",
        "category",
    ]:
        group_count = int(
            group_profile[
                group_profile["group_variable"]
                == group_variable
            ].shape[0]
        )

        print(
            f"{group_variable}: "
            f"{group_count} grupos"
        )

    print("----------------------------")
    print("CANDIDATOS A DISCREPÂNCIAS")
    print(
        "Arquivo: "
        "reports/statistics/outlier_candidates.csv"
    )
    print(
        f"Ocorrências identificadas: "
        f"{outlier_candidates.shape[0]}"
    )

    for variable in NUMERIC_COLUMNS:
        candidate_count = int(
            outlier_candidates[
                outlier_candidates["variable"]
                == variable
            ].shape[0]
        )

        print(
            f"{variable}: "
            f"{candidate_count} candidatos"
        )

    print("----------------------------")
    print("RELATÓRIO ESTATÍSTICO GERADO")
    print(
        "Arquivo: "
        "reports/statistics/statistical_report.md"
    )

if __name__ == "__main__":
    run_initial_profile()