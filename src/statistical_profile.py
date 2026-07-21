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


def run_initial_profile() -> None:
    """Executa a preparação inicial da camada estatística."""
    input_path = "data/processed/compras_tratadas.csv"

    data = load_treated_data(input_path)
    prepared_data = prepare_statistical_base(data)

    diagnostic = build_initial_diagnostic(
        prepared_data
    )

    variable_classes = classify_variables()

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


if __name__ == "__main__":
    run_initial_profile()