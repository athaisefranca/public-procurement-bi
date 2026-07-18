# Public Procurement BI

Projeto de portfólio da Frente 2 — Business Intelligence em Compras Públicas.

## Objetivo

Construir, de forma progressiva e reproduzível, um fluxo completo de dados aplicado a compras públicas, incluindo obtenção, diagnóstico de qualidade, limpeza, transformação, validação, modelagem, consultas, indicadores e dashboard.

## Estágio atual

O projeto está na fase de fundação técnica.

A primeira entrega implementa um pequeno pipeline em Python capaz de:

- ler um arquivo CSV sintético;
- validar a presença de colunas obrigatórias;
- verificar campos vazios;
- validar datas, quantidades e valores;
- validar modalidades, categorias e situações;
- detectar chaves duplicadas;
- separar registros válidos e inválidos;
- gerar um arquivo tratado;
- gerar um arquivo de rejeitados;
- produzir um relatório simples de qualidade.

Nesta fase ainda não são utilizados:

- pandas;
- SQL;
- Power Query;
- DAX;
- Power BI;
- modelagem dimensional completa.

Esses elementos serão incorporados gradualmente conforme o avanço dos cursos e do projeto.

## Dados

A primeira versão utiliza exclusivamente dados sintéticos.

Nenhuma planilha profissional original, classificação interna, comentário, responsável real, documento institucional, dado pessoal ou identificador protegido é utilizado ou publicado.

A base sintética foi criada apenas para testar leitura, validação, transformação, rejeição de registros e controle de qualidade.

## Unidade de análise

Cada linha da base representa um item pertencente a um processo sintético de compra pública.

Um processo pode possuir mais de um item. Por isso, `process_id` pode aparecer em várias linhas.

A combinação entre `process_id` e `item_id` deve ser única.

## Estrutura do repositório

```text
public-procurement-bi/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   │   └── compras_sinteticas.csv
│   ├── processed/
│   │   └── compras_tratadas.csv
│   └── rejected/
│       └── compras_rejeitadas.csv
├── docs/
│   ├── data_dictionary.md
│   └── decision_log.md
├── reports/
│   └── quality/
│       └── quality_report.txt
├── src/
│   ├── transform.py
│   └── validate.py
└── tests/
```

## Tecnologias iniciais

- Python local
- Biblioteca padrão do Python
- Visual Studio Code
- PowerShell
- Git
- GitHub

## Arquivo de entrada

O pipeline utiliza:

```text
data/raw/compras_sinteticas.csv
```

A base contém 12 registros sintéticos, incluindo casos válidos e erros inseridos intencionalmente para testar o comportamento do pipeline.

## Colunas da base sintética

```text
process_id
item_id
publication_date
organization_code
purchase_modality
category
item_description
quantity
estimated_unit_value
status
```

Após a transformação, é criado também o campo:

```text
estimated_total_value
```

Esse campo é calculado por:

```text
estimated_total_value = quantity * estimated_unit_value
```

## Regras de validação

O pipeline verifica:

- existência do arquivo de entrada;
- presença das colunas obrigatórias;
- campos obrigatórios vazios;
- datas no formato `DD/MM/AAAA`;
- validade real da data;
- quantidades maiores que zero;
- valores unitários maiores que zero;
- modalidade pertencente à lista permitida;
- categoria pertencente à lista permitida;
- situação pertencente à lista permitida;
- duplicidade da combinação `process_id + item_id`.

## Valores controlados

### Modalidades permitidas

- `Pregão`
- `Dispensa`
- `Concorrência`

### Categorias permitidas

- `Material de escritório`
- `Equipamentos de informática`
- `Serviços de manutenção`
- `Mobiliário`

### Situações permitidas

- `Publicado`
- `Em andamento`
- `Concluído`
- `Cancelado`

## Execução

Na raiz do projeto, execute:

```powershell
python -m src.transform
```

A execução deve apresentar:

```text
Pipeline concluído com sucesso.
Registros lidos: 12
Registros válidos: 5
Registros rejeitados: 7
```

## Saídas geradas

O pipeline gera:

```text
data/processed/compras_tratadas.csv
data/rejected/compras_rejeitadas.csv
reports/quality/quality_report.txt
```

## Arquivo tratado

O arquivo:

```text
data/processed/compras_tratadas.csv
```

contém somente registros aprovados pelas regras de validação.

As principais transformações são:

- remoção de espaços externos;
- conversão da data para `AAAA-MM-DD`;
- conversão de quantidade para `float`;
- conversão do valor unitário para `float`;
- cálculo do valor total estimado.

## Arquivo de rejeitados

O arquivo:

```text
data/rejected/compras_rejeitadas.csv
```

mantém os dados brutos dos registros inválidos e acrescenta a coluna:

```text
rejection_reason
```

Essa coluna registra o motivo da rejeição.

Exemplos de erros testados:

- data impossível;
- quantidade igual a zero;
- quantidade negativa;
- valor numérico inválido;
- modalidade não permitida;
- campo obrigatório vazio;
- chave duplicada.

## Relatório de qualidade

O arquivo:

```text
reports/quality/quality_report.txt
```

registra:

```text
Total de registros lidos: 12
Registros válidos: 5
Registros rejeitados: 7
```

## Resultado da primeira entrega

A primeira versão do pipeline produziu:

- 12 registros lidos;
- 5 registros válidos;
- 7 registros rejeitados.

Os erros foram inseridos intencionalmente para testar as regras documentadas.

## Organização do código

### `src/validate.py`

Responsável por:

- colunas obrigatórias;
- campos obrigatórios;
- data;
- números positivos;
- valores controlados;
- validação completa de um registro.

### `src/transform.py`

Responsável por:

- leitura do CSV;
- padronização de textos;
- conversão de data;
- transformação de registros;
- identificação de duplicidades;
- separação entre válidos e rejeitados;
- gravação dos arquivos;
- geração do relatório de qualidade;
- execução do pipeline.

## Testes executados

Foram realizados:

- teste de sintaxe com `python -m py_compile`;
- teste manual de data válida;
- teste manual de data inválida;
- teste de número positivo;
- teste de quantidade igual a zero;
- teste de texto em campo numérico;
- teste de modalidade permitida;
- teste de modalidade não permitida;
- teste de registro válido;
- teste de transformação de um registro;
- teste de leitura do CSV;
- teste de separação entre registros válidos e rejeitados;
- execução completa do pipeline;
- conferência dos três arquivos de saída;
- verificação de que `src/__pycache__/` está ignorado pelo Git.

## Limitações atuais

Esta versão utiliza apenas conhecimentos presentes nas duas consolidações de Python já concluídas.

Ainda não fazem parte do projeto:

- pandas;
- NumPy operacional;
- SQL;
- bancos de dados;
- APIs;
- modelagem dimensional;
- Power Query;
- DAX;
- Power BI;
- testes automatizados com frameworks;
- dados públicos reais de compras.

## Segurança

O projeto utiliza somente dados sintéticos.

Não são utilizados:

- planilhas profissionais originais;
- classificações internas;
- comentários reais;
- responsáveis reais;
- documentos institucionais;
- dados pessoais;
- contatos;
- identificadores protegidos;
- informações profissionais sigilosas.

## Próximas etapas

1. Revisar a documentação da primeira entrega.
2. Registrar os testes finais.
3. Versionar os arquivos de saída.
4. Fazer commit e push.
5. Incorporar novos conteúdos somente após a conclusão de cursos compatíveis.