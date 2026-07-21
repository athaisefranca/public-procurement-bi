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
if __name__ == "__main__":
    run_initial_profile()