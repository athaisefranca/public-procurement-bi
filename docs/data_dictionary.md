# Dicionário de dados

## 1. Visão geral

Este documento descreve a estrutura da base sintética inicial da Frente 2 — Business Intelligence em Compras Públicas.

A base foi criada exclusivamente para demonstrar, de forma segura, procedimentos de leitura, validação, limpeza, transformação e controle de qualidade em Python.

Todos os processos, órgãos, itens, descrições, categorias, valores e situações serão fictícios. A base não representa compras realizadas por uma instituição real.

## 2. Unidade de análise

Cada linha da base representa um item pertencente a um processo sintético de compra pública.

Um processo pode possuir mais de um item. Por isso, `process_id` pode aparecer em várias linhas.

A combinação entre `process_id` e `item_id` deverá ser única.

Exemplo:

```text
Processo P001
├── Item I001
└── Item I002
```

## 3. Estrutura da base bruta

| Coluna | Tipo esperado após tratamento | Obrigatória | Descrição | Exemplo sintético |
|---|---|---:|---|---|
| `process_id` | `str` | Sim | Identificador sintético do processo de compra. | `P001` |
| `item_id` | `str` | Sim | Identificador sintético do item dentro do processo. | `I001` |
| `publication_date` | `str` no formato `AAAA-MM-DD` | Sim | Data sintética de publicação do processo. | `2026-01-15` |
| `organization_code` | `str` | Sim | Código fictício da organização compradora. | `ORG01` |
| `purchase_modality` | `str` | Sim | Modalidade sintética da contratação. | `Pregão` |
| `category` | `str` | Sim | Categoria genérica do material ou serviço. | `Mobiliário` |
| `item_description` | `str` | Sim | Descrição fictícia do item comprado. | `Cadeira de escritório` |
| `quantity` | `float` | Sim | Quantidade prevista do item. | `20.0` |
| `estimated_unit_value` | `float` | Sim | Valor unitário estimado, em reais. | `450.00` |
| `status` | `str` | Sim | Situação sintética do processo ou item. | `Publicado` |

## 4. Cabeçalho do arquivo CSV

```csv
process_id,item_id,publication_date,organization_code,purchase_modality,category,item_description,quantity,estimated_unit_value,status
```

## 5. Regras gerais

### 5.1 Campos obrigatórios

As dez colunas são obrigatórias.

Um registro deverá ser rejeitado quando qualquer campo obrigatório estiver vazio após a remoção de espaços externos.

### 5.2 Identificação dos registros

A combinação entre `process_id` e `item_id` deverá ser única.

Exemplo de chave válida:

```text
P001 + I001
```

A repetição da mesma combinação indicará possível duplicidade.

Nesta primeira versão, os identificadores serão sintéticos e seguirão padrões simples:

```text
process_id: P001, P002, P003
item_id: I001, I002, I003
organization_code: ORG01, ORG02, ORG03
```

### 5.3 Data de publicação

A entrada bruta poderá conter datas no formato:

```text
DD/MM/AAAA
```

Após o tratamento, a data deverá ser gravada no formato:

```text
AAAA-MM-DD
```

Datas impossíveis ou com formato inválido deverão causar a rejeição do registro.

Exemplos:

```text
15/01/2026 -> 2026-01-15
31/02/2026 -> inválida
```

### 5.4 Quantidade

`quantity` deverá:

- ser convertível para `float`;
- ser maior que zero;
- não estar vazia.

Exemplos:

```text
10 -> válida
2.5 -> válida
0 -> inválida
-3 -> inválida
abc -> inválida
```

### 5.5 Valor unitário estimado

`estimated_unit_value` deverá:

- ser convertível para `float`;
- ser maior que zero;
- não estar vazio.

A base bruta utilizará ponto como separador decimal.

Exemplos:

```text
1500.00 -> válido
89.90 -> válido
0 -> inválido
-10.50 -> inválido
texto -> inválido
```

### 5.6 Textos

Os campos textuais serão tratados com remoção de espaços externos.

Os valores de modalidade, categoria e situação serão comparados com listas controladas.

Não serão aplicadas transformações complexas nem classificações automáticas nesta versão.

## 6. Valores controlados

### 6.1 Modalidades permitidas

- `Pregão`
- `Dispensa`
- `Concorrência`

### 6.2 Categorias permitidas

- `Material de escritório`
- `Equipamentos de informática`
- `Serviços de manutenção`
- `Mobiliário`

### 6.3 Situações permitidas

- `Publicado`
- `Em andamento`
- `Concluído`
- `Cancelado`

## 7. Campo calculado futuro desta entrega

O arquivo bruto não conterá uma coluna de valor total estimado.

Durante a transformação, poderá ser calculado:

```text
estimated_total_value = quantity * estimated_unit_value
```

O campo será derivado apenas após a validação de `quantity` e `estimated_unit_value`.

## 8. Colunas deliberadamente excluídas

Nesta primeira versão não serão incluídos:

- nome de fornecedor;
- CNPJ ou CPF;
- responsável;
- e-mail ou telefone;
- número de documento oficial;
- link de processo;
- comentários;
- justificativas;
- unidade administrativa detalhada;
- códigos oficiais reais;
- valor homologado;
- datas de conclusão;
- quantidade de participantes;
- informações jurídicas.

Esses campos não são necessários para demonstrar a fundação técnica atual e poderiam aumentar a complexidade ou o risco de exposição indevida.

## 9. Natureza dos dados

Todos os dados desta primeira entrega serão sintéticos.

Os registros deverão ser plausíveis apenas para permitir testes de estrutura, validação e transformação. Nenhum registro deverá copiar ou adaptar uma compra profissional real.

## 10. Versão

| Versão | Data | Alteração |
|---|---|---|
| `0.1` | `2026-07-17` | Definição inicial das colunas, unidade de análise e regras básicas. |