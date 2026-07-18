"""Funções de validação da base sintética de compras públicas."""

from datetime import datetime


REQUIRED_COLUMNS: list[str] = [
    "process_id",
    "item_id",
    "publication_date",
    "organization_code",
    "purchase_modality",
    "category",
    "item_description",
    "quantity",
    "estimated_unit_value",
    "status",
]

ALLOWED_MODALITIES: list[str] = [
    "Pregão",
    "Dispensa",
    "Concorrência",
]

ALLOWED_CATEGORIES: list[str] = [
    "Material de escritório",
    "Equipamentos de informática",
    "Serviços de manutenção",
    "Mobiliário",
]

ALLOWED_STATUSES: list[str] = [
    "Publicado",
    "Em andamento",
    "Concluído",
    "Cancelado",
]


def validate_required_columns(columns: list[str]) -> None:
    """Verifica se todas as colunas obrigatórias estão presentes.

    Args:
        columns: Lista de nomes das colunas encontradas no arquivo.

    Raises:
        TypeError: Se columns não for uma lista.
        ValueError: Se uma ou mais colunas obrigatórias estiverem ausentes.
    """
    if not isinstance(columns, list):
        raise TypeError("As colunas devem ser fornecidas em uma lista.")

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in columns
    ]

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(
            f"Colunas obrigatórias ausentes: {missing_text}"
        )


def validate_required_fields(record: dict[str, str]) -> list[str]:
    """Identifica campos obrigatórios vazios em um registro.

    Args:
        record: Registro representado por um dicionário.

    Returns:
        Lista com mensagens de erro. Retorna lista vazia quando não há erro.

    Raises:
        TypeError: Se record não for um dicionário.
        KeyError: Se uma coluna obrigatória não existir no registro.
    """
    if not isinstance(record, dict):
        raise TypeError("O registro deve ser um dicionário.")

    errors: list[str] = []

    for column in REQUIRED_COLUMNS:
        if column not in record:
            raise KeyError(f"Campo ausente no registro: {column}")

        if record[column].strip() == "":
            errors.append(f"Campo obrigatório vazio: {column}")

    return errors


def validate_date(value: str) -> list[str]:
    """Valida uma data no formato DD/MM/AAAA.

    Args:
        value: Texto contendo a data.

    Returns:
        Lista vazia quando a data é válida ou uma mensagem de erro.

    Raises:
        TypeError: Se value não for uma string.
    """
    if not isinstance(value, str):
        raise TypeError("A data deve ser fornecida como texto.")

    try:
        datetime.strptime(value.strip(), "%d/%m/%Y")
    except ValueError:
        return [f"Data inválida: {value}"]

    return []


def validate_positive_number(value: str, field_name: str) -> list[str]:
    """Valida se um texto representa um número maior que zero.

    Args:
        value: Texto que deverá ser convertido para float.
        field_name: Nome do campo usado na mensagem de erro.

    Returns:
        Lista vazia quando o valor é válido ou uma mensagem de erro.

    Raises:
        TypeError: Se value ou field_name não forem strings.
    """
    if not isinstance(value, str):
        raise TypeError("O valor numérico deve ser fornecido como texto.")

    if not isinstance(field_name, str):
        raise TypeError("O nome do campo deve ser fornecido como texto.")

    try:
        number = float(value.strip())
    except ValueError:
        return [f"Valor numérico inválido em {field_name}: {value}"]

    if number <= 0:
        return [f"{field_name} deve ser maior que zero: {value}"]

    return []


def validate_allowed_value(
    value: str,
    allowed_values: list[str],
    field_name: str,
) -> list[str]:
    """Valida se um valor pertence a uma lista controlada.

    Args:
        value: Valor que será verificado.
        allowed_values: Lista de valores aceitos.
        field_name: Nome do campo usado na mensagem de erro.

    Returns:
        Lista vazia quando o valor é permitido ou uma mensagem de erro.

    Raises:
        TypeError: Se os argumentos possuírem tipos incompatíveis.
    """
    if not isinstance(value, str):
        raise TypeError("O valor deve ser fornecido como texto.")

    if not isinstance(allowed_values, list):
        raise TypeError("Os valores permitidos devem estar em uma lista.")

    if not isinstance(field_name, str):
        raise TypeError("O nome do campo deve ser fornecido como texto.")

    normalized_value = value.strip()

    if normalized_value not in allowed_values:
        return [f"Valor não permitido em {field_name}: {value}"]

    return []


def validate_record(record: dict[str, str]) -> list[str]:
    """Executa todas as validações aplicáveis a um registro.

    Args:
        record: Registro bruto representado por um dicionário.

    Returns:
        Lista com todos os erros encontrados.
    """
    errors: list[str] = []

    required_field_errors = validate_required_fields(record)
    errors.extend(required_field_errors)

    if required_field_errors:
        return errors

    errors.extend(validate_date(record["publication_date"]))

    errors.extend(
        validate_positive_number(
            record["quantity"],
            "quantity",
        )
    )

    errors.extend(
        validate_positive_number(
            record["estimated_unit_value"],
            "estimated_unit_value",
        )
    )

    errors.extend(
        validate_allowed_value(
            record["purchase_modality"],
            ALLOWED_MODALITIES,
            "purchase_modality",
        )
    )

    errors.extend(
        validate_allowed_value(
            record["category"],
            ALLOWED_CATEGORIES,
            "category",
        )
    )

    errors.extend(
        validate_allowed_value(
            record["status"],
            ALLOWED_STATUSES,
            "status",
        )
    )

    return errors