"""Funções de transformação da base sintética de compras públicas."""

import csv
from datetime import datetime
from pathlib import Path

from src.validate import validate_record, validate_required_columns


def normalize_text(value: str) -> str:
    """Remove espaços externos de um campo textual.

    Args:
        value: Texto que será padronizado.

    Returns:
        Texto sem espaços externos.

    Raises:
        TypeError: Se value não for uma string.
    """
    if not isinstance(value, str):
        raise TypeError("O valor deve ser fornecido como texto.")

    return value.strip()


def transform_date(value: str) -> str:
    """Converte uma data de DD/MM/AAAA para AAAA-MM-DD.

    Args:
        value: Data válida no formato DD/MM/AAAA.

    Returns:
        Data no formato AAAA-MM-DD.

    Raises:
        TypeError: Se value não for uma string.
        ValueError: Se a data possuir formato ou valor inválido.
    """
    if not isinstance(value, str):
        raise TypeError("A data deve ser fornecida como texto.")

    parsed_date = datetime.strptime(value.strip(), "%d/%m/%Y")
    return parsed_date.strftime("%Y-%m-%d")


def transform_record(
    record: dict[str, str],
) -> dict[str, str | float]:
    """Valida e transforma um registro bruto de compra sintética.

    Args:
        record: Registro bruto representado por um dicionário.

    Returns:
        Novo dicionário com textos padronizados, data convertida,
        números transformados e valor total calculado.

    Raises:
        TypeError: Se record não for um dicionário.
        ValueError: Se o registro possuir uma ou mais regras inválidas.
    """
    if not isinstance(record, dict):
        raise TypeError("O registro deve ser um dicionário.")

    errors = validate_record(record)

    if errors:
        error_message = "; ".join(errors)
        raise ValueError(error_message)

    quantity = float(record["quantity"].strip())
    estimated_unit_value = float(
        record["estimated_unit_value"].strip()
    )

    transformed_record: dict[str, str | float] = {
        "process_id": normalize_text(record["process_id"]),
        "item_id": normalize_text(record["item_id"]),
        "publication_date": transform_date(
            record["publication_date"]
        ),
        "organization_code": normalize_text(
            record["organization_code"]
        ),
        "purchase_modality": normalize_text(
            record["purchase_modality"]
        ),
        "category": normalize_text(record["category"]),
        "item_description": normalize_text(
            record["item_description"]
        ),
        "quantity": quantity,
        "estimated_unit_value": estimated_unit_value,
        "estimated_total_value": round(
            quantity * estimated_unit_value,
            2,
        ),
        "status": normalize_text(record["status"]),
    }

    return transformed_record


def read_csv_records(file_path: str) -> list[dict[str, str]]:
    """Lê registros de um arquivo CSV.

    Args:
        file_path: Caminho do arquivo CSV de entrada.

    Returns:
        Lista de registros representados por dicionários.

    Raises:
        TypeError: Se file_path não for uma string.
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o arquivo não possuir cabeçalho ou
            não estiver em UTF-8.
    """
    if not isinstance(file_path, str):
        raise TypeError(
            "O caminho do arquivo deve ser fornecido como texto."
        )

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {file_path}"
        )

    try:
        with path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError(
                    "O arquivo CSV não possui cabeçalho."
                )

            validate_required_columns(reader.fieldnames)

            records = [dict(record) for record in reader]

    except UnicodeDecodeError as error:
        raise ValueError(
            "Não foi possível ler o arquivo com codificação UTF-8."
        ) from error

    return records


def process_records(
    records: list[dict[str, str]],
) -> tuple[
    list[dict[str, str | float]],
    list[dict[str, str]],
]:
    """Valida, transforma e separa registros válidos e rejeitados.

    Args:
        records: Lista de registros brutos.

    Returns:
        Tupla contendo os registros transformados e os rejeitados.

    Raises:
        TypeError: Se records não for uma lista.
    """
    if not isinstance(records, list):
        raise TypeError(
            "Os registros devem ser fornecidos em uma lista."
        )

    valid_records: list[dict[str, str | float]] = []
    rejected_records: list[dict[str, str]] = []
    seen_keys: list[str] = []

    for record in records:
        process_id = record["process_id"].strip()
        item_id = record["item_id"].strip()
        record_key = f"{process_id}|{item_id}"

        errors: list[str] = []

        if record_key in seen_keys:
            errors.append(
                "Chave duplicada: "
                f"process_id={process_id}, item_id={item_id}"
            )
        else:
            seen_keys.append(record_key)

        try:
            transformed_record = transform_record(record)
        except (ValueError, TypeError, KeyError) as error:
            errors.append(str(error))
        else:
            if not errors:
                valid_records.append(transformed_record)

        if errors:
            rejected_record = {
                column: record[column]
                for column in record
            }
            rejected_record["rejection_reason"] = "; ".join(
                errors
            )
            rejected_records.append(rejected_record)

    return valid_records, rejected_records


def write_csv_records(
    file_path: str,
    records: list[dict[str, str | float]],
) -> None:
    """Grava registros em um arquivo CSV.

    Args:
        file_path: Caminho do arquivo de saída.
        records: Lista de registros que serão gravados.

    Raises:
        TypeError: Se os argumentos possuírem tipos incompatíveis.
        ValueError: Se a lista de registros estiver vazia.
    """
    if not isinstance(file_path, str):
        raise TypeError(
            "O caminho do arquivo deve ser fornecido como texto."
        )

    if not isinstance(records, list):
        raise TypeError(
            "Os registros devem ser fornecidos em uma lista."
        )

    if not records:
        raise ValueError("Não há registros para gravar.")

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(records[0].keys())

    with path.open(
        mode="w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(records)


def write_quality_report(
    file_path: str,
    total_records: int,
    valid_records: int,
    rejected_records: int,
) -> None:
    """Grava um relatório textual simples de qualidade.

    Args:
        file_path: Caminho do relatório.
        total_records: Quantidade total de registros lidos.
        valid_records: Quantidade de registros válidos.
        rejected_records: Quantidade de registros rejeitados.

    Raises:
        TypeError: Se file_path não for texto.
        ValueError: Se alguma contagem for negativa.
    """
    if not isinstance(file_path, str):
        raise TypeError(
            "O caminho do relatório deve ser fornecido como texto."
        )

    counts = [
        total_records,
        valid_records,
        rejected_records,
    ]

    for count in counts:
        if count < 0:
            raise ValueError(
                "As contagens não podem ser negativas."
            )

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    report_lines = [
        "RELATÓRIO DE QUALIDADE",
        "=====================",
        f"Total de registros lidos: {total_records}",
        f"Registros válidos: {valid_records}",
        f"Registros rejeitados: {rejected_records}",
    ]

    report_text = "\n".join(report_lines)

    with path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        file.write(report_text)


def run_pipeline() -> None:
    """Executa o pipeline completo da primeira entrega."""
    input_path = "data/raw/compras_sinteticas.csv"
    processed_path = "data/processed/compras_tratadas.csv"
    rejected_path = "data/rejected/compras_rejeitadas.csv"
    report_path = "reports/quality/quality_report.txt"

    records = read_csv_records(input_path)

    valid_records, rejected_records = process_records(
        records
    )

    write_csv_records(
        processed_path,
        valid_records,
    )

    write_csv_records(
        rejected_path,
        rejected_records,
    )

    write_quality_report(
        report_path,
        total_records=len(records),
        valid_records=len(valid_records),
        rejected_records=len(rejected_records),
    )

    print("Pipeline concluído com sucesso.")
    print(f"Registros lidos: {len(records)}")
    print(f"Registros válidos: {len(valid_records)}")
    print(f"Registros rejeitados: {len(rejected_records)}")


if __name__ == "__main__":
    run_pipeline()