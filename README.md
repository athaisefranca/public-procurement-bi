# Public Procurement BI

Projeto de portfólio da Frente 2 — Business Intelligence em Compras Públicas.

## Objetivo

Construir, de forma progressiva e reproduzível, um fluxo completo de dados aplicado a compras públicas, incluindo obtenção, diagnóstico de qualidade, limpeza, transformação, validação, modelagem, consultas, indicadores e dashboard.

## Estágio atual

O projeto está na fase de fundação técnica.

A primeira entrega será um pequeno pipeline em Python capaz de:

- ler um arquivo CSV sintético;
- validar a presença de colunas obrigatórias;
- padronizar textos;
- converter datas, quantidades e valores;
- separar registros válidos e inválidos;
- gerar um arquivo tratado;
- produzir um relatório simples de qualidade.

Nesta fase ainda não serão utilizados:

- pandas;
- SQL;
- Power Query;
- DAX;
- Power BI;
- modelagem dimensional completa.

Esses elementos serão incorporados gradualmente conforme o avanço dos cursos e do projeto.

## Dados

A primeira versão utiliza exclusivamente dados sintéticos.

Nenhuma planilha profissional original, classificação interna, comentário, responsável real, documento institucional, dado pessoal ou identificador protegido será utilizado ou publicado.

## Estrutura do repositório

```text
data/
├── raw/
├── processed/
└── rejected/

docs/
├── data_dictionary.md
└── decision_log.md

reports/
└── quality/

src/
├── transform.py
└── validate.py

tests/
```

## Tecnologias iniciais

- Python local
- Biblioteca padrão do Python
- Visual Studio Code
- PowerShell
- Git e GitHub

## Próximas etapas

1. Definir a estrutura da base sintética.
2. Criar o dicionário de dados.
3. Criar o arquivo CSV bruto.
4. Implementar validações.
5. Implementar transformações.
6. Gerar arquivos tratados, rejeitados e relatório de qualidade.