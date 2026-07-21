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

---

## Camada estatística

A camada estatística utiliza exclusivamente:

```text
data/processed/compras_tratadas.csv
```

A unidade de análise permanece no nível de item:

> uma linha representa um item pertencente a um processo sintético.

As métricas desta camada não devem ser interpretadas como métricas por processo.

## Classificação das variáveis

### Identificadores

| Campo | Classificação | Uso |
|---|---|---|
| `process_id` | Identificador | Identifica o processo sintético |
| `item_id` | Identificador | Identifica o item dentro do processo |
| `organization_code` | Identificador categórico | Identifica a organização fictícia |

### Data

| Campo | Classificação | Uso |
|---|---|---|
| `publication_date` | Data | Data de publicação do item |

### Variáveis qualitativas nominais

| Campo | Classificação | Uso estatístico |
|---|---|---|
| `purchase_modality` | Qualitativa nominal | Frequências e comparação por modalidade |
| `category` | Qualitativa nominal | Frequências e comparação por categoria |
| `status` | Qualitativa nominal | Frequências por situação |

### Variáveis quantitativas

| Campo | Classificação | Uso estatístico |
|---|---|---|
| `quantity` | Quantitativa | Perfil de quantidade por item |
| `estimated_unit_value` | Quantitativa contínua | Perfil do valor unitário estimado por item |
| `estimated_total_value` | Quantitativa contínua derivada | Perfil do valor total estimado por item |

### Texto descritivo

| Campo | Classificação | Uso |
|---|---|---|
| `item_description` | Texto descritivo | Descrição sintética do item |

## Regras das variáveis quantitativas

### `quantity`

Representa a quantidade prevista para o item.

Regras:

- deve ser numérica;
- deve ser maior que zero;
- é analisada no nível de item;
- não deve ser somada entre unidades de medida incompatíveis em uma futura base pública.

### `estimated_unit_value`

Representa o valor estimado de uma unidade do item.

Regras:

- deve ser numérico;
- deve ser maior que zero;
- não representa o valor total do item;
- não deve ser somado como indicador financeiro agregado.

### `estimated_total_value`

Representa o valor total estimado do item.

Fórmula:

```text
estimated_total_value = quantity × estimated_unit_value
```

Regras:

- é calculado durante o tratamento;
- não existe no arquivo bruto;
- pode ser usado em somas e distribuições no nível de item;
- não representa valor homologado;
- não deve ser interpretado como valor total por processo sem agregação prévia.

## Campo não disponível

### `valor_homologado`

Este campo não existe na versão atual da base.

Nenhuma coluna existente deve ser renomeada ou reinterpretada como valor homologado.

A métrica só poderá ser incorporada quando uma futura fonte pública apresentar um campo final com significado, cobertura e regra de negócio documentados.

## Métricas estatísticas documentadas

Para as variáveis quantitativas são calculadas:

- contagem;
- média;
- mediana;
- primeiro quartil;
- terceiro quartil;
- intervalo interquartil;
- percentil 90;
- percentil 95;
- desvio médio absoluto;
- variância populacional;
- desvio padrão populacional;
- mínimo;
- máximo.

A variância e o desvio padrão usam:

```text
ddof=0
```

Isso significa que as medidas são tratadas como populacionais dentro do universo sintético desta versão.

## Frequências categóricas

São calculadas frequências absolutas e percentuais para:

- `purchase_modality`;
- `category`;
- `status`.

As frequências representam itens.

Um processo com dois itens contribui com duas ocorrências.

## Comparações por grupo

A variável analisada nas comparações é:

```text
estimated_total_value
```

Os grupos utilizados são:

- `purchase_modality`;
- `category`.

Para cada grupo são calculados:

- contagem;
- média;
- mediana;
- Q1;
- Q3;
- intervalo interquartil;
- P90;
- desvio padrão populacional;
- mínimo;
- máximo.

## Candidatos a discrepâncias

A identificação utiliza:

```text
limite inferior = Q1 - 1,5 × IIQ
limite superior = Q3 + 1,5 × IIQ
```

Uma observação é registrada como candidata quando:

```text
valor < limite inferior
```

ou:

```text
valor > limite superior
```

As variáveis verificadas são:

- `quantity`;
- `estimated_unit_value`;
- `estimated_total_value`.

A classificação como candidata não significa:

- erro;
- fraude;
- inconsistência confirmada;
- necessidade automática de correção;
- necessidade automática de remoção.

Os registros permanecem na base tratada.

## Arquivos estatísticos derivados

| Arquivo | Conteúdo |
|---|---|
| `reports/statistics/frequency_profile.csv` | Frequências absolutas e percentuais |
| `reports/statistics/numeric_profile.csv` | Perfil das variáveis quantitativas |
| `reports/statistics/group_profile.csv` | Comparações por modalidade e categoria |
| `reports/statistics/outlier_candidates.csv` | Candidatos a discrepâncias |
| `reports/statistics/statistical_report.md` | Relatório consolidado e reproduzível |

## Limitações da camada estatística

- A base contém 30 itens válidos.
- Todos os registros são sintéticos.
- Os grupos possuem poucas observações.
- P90 e P95 são demonstrativos.
- Os resultados não representam uma população externa.
- Não existe valor homologado.
- Não há análise temporal robusta.
- Não há mistura entre nível de item e nível de processo.