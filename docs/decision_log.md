## 2026-07-17 — Primeira execução completa do pipeline

### Implementação concluída

Foram implementadas as funções de:

- leitura do arquivo CSV;
- validação do cabeçalho;
- transformação de um registro;
- validação de registros;
- identificação de duplicidades;
- separação entre válidos e rejeitados;
- gravação dos arquivos de saída;
- geração do relatório de qualidade.

### Arquivos gerados

- `data/processed/compras_tratadas.csv`
- `data/rejected/compras_rejeitadas.csv`
- `reports/quality/quality_report.txt`

### Resultado da execução

- Total de registros lidos: 12
- Registros válidos: 5
- Registros rejeitados: 7

### Testes executados

- compilação de `src/validate.py` com `python -m py_compile`;
- compilação de `src/transform.py` com `python -m py_compile`;
- teste manual de data válida e inválida;
- teste manual de número positivo, zero e texto inválido;
- teste manual de modalidade permitida e não permitida;
- teste manual de registro válido;
- teste manual de transformação de um registro;
- teste manual de leitura do CSV;
- teste manual de separação entre válidos e rejeitados;
- execução completa com `python -m src.transform`;
- conferência dos três arquivos de saída;
- verificação de que `src/__pycache__/` está ignorado pelo Git.

### Decisão de execução

O pipeline deverá ser executado a partir da raiz do projeto com:

```powershell
python -m src.transform

---

## 2026-07-21 — Ampliação da base sintética para perfil estatístico

### Objetivo

Ampliar a base sintética da Frente 2 para permitir a aplicação dos conteúdos do curso Estatística com Python: Frequências e Medidas.

### Alterações realizadas

- A base bruta passou de 12 para 37 registros.
- O número de registros válidos passou de 5 para 30.
- Os 7 registros inválidos originais foram preservados.
- A estrutura das colunas não foi alterada.
- A granularidade continua sendo de um item por linha.
- Foram adicionados valores variados de quantidade, valor unitário e valor total estimado.
- Foram ampliadas as ocorrências de modalidades, categorias e situações.
- Foram incluídos valores altos plausíveis para permitir testes de assimetria e identificação de candidatos a discrepâncias.

### Resultado do pipeline

- Registros lidos: 37
- Registros válidos: 30
- Registros rejeitados: 7

### Validações executadas

- conferência da quantidade de registros brutos;
- conferência da quantidade de registros tratados;
- conferência da quantidade de registros rejeitados;
- revisão dos sete motivos de rejeição;
- confirmação de que a combinação entre processo e item continua sendo a chave da base;
- confirmação de que o pipeline anterior não apresentou regressão.

### Segurança

- Todos os novos registros são sintéticos.
- Nenhum dado profissional, pessoal ou institucional real foi utilizado.
- Os valores foram criados somente para demonstração estatística.
- Os resultados não representam fatos sobre qualquer instituição real.

### Próxima etapa

Criar a camada de perfil estatístico em `src/statistical_profile.py`, usando a base tratada no nível de item.

---

## 2026-07-21 — Preparação da camada estatística

### Objetivo

Preparar a estrutura técnica responsável por ler, validar e classificar a base tratada antes da geração das métricas estatísticas.

### Arquivos criados ou alterados

- `src/statistical_profile.py`
- `requirements.txt`
- `reports/statistics/.gitkeep`

### Dependências utilizadas

- pandas 3.0.3
- NumPy 2.5.1

As dependências foram instaladas no ambiente virtual local do projeto.

### Funções implementadas

- `load_treated_data()`
- `validate_statistical_columns()`
- `prepare_statistical_base()`
- `classify_variables()`
- `build_initial_diagnostic()`
- `run_initial_profile()`

### Validações implementadas

- existência do arquivo tratado;
- base não vazia;
- presença das colunas estatísticas obrigatórias;
- ausência de valores nulos nas colunas necessárias;
- conversão das variáveis quantitativas para valores numéricos;
- validação da data de publicação;
- verificação da unicidade da combinação `process_id + item_id`;
- confirmação da granularidade de item.

### Classificação das variáveis

Identificadores:

- `process_id`
- `item_id`
- `organization_code`

Data:

- `publication_date`

Qualitativas nominais:

- `purchase_modality`
- `category`
- `status`

Quantitativas:

- `quantity`
- `estimated_unit_value`
- `estimated_total_value`

Texto descritivo:

- `item_description`

### Resultado da execução

- Itens analisados: 30
- Processos distintos: 28
- Chaves processo-item únicas: 30
- Chaves processo-item duplicadas: 0

### Comando de execução

```powershell
python -m src.statistical_profile
```

### Decisão de granularidade

A camada estatística continuará usando o nível de item:

> uma linha representa um item pertencente a um processo sintético de compra.

A contagem de processos será realizada separadamente por `process_id` distinto. Nenhuma distribuição de itens será apresentada como se representasse uma distribuição de processos.

### Limites desta fase

Ainda não foram implementados:

- frequências absolutas ou percentuais;
- médias e medianas;
- quartis e percentis;
- medidas de dispersão;
- identificação de candidatos a discrepâncias;
- comparações por grupo;
- gráficos.

Esses cálculos serão acrescentados nas fases seguintes.

### Segurança

A camada utiliza exclusivamente a base sintética já versionada no projeto. Nenhum dado profissional, pessoal ou institucional real foi utilizado.

### Próxima etapa

Implementar as frequências absolutas e percentuais de modalidade, categoria e situação.

---

## 2026-07-21 — Frequências categóricas da base tratada

### Objetivo

Gerar frequências absolutas e percentuais das principais variáveis qualitativas nominais da base tratada.

### Arquivos criados ou alterados

- `src/statistical_profile.py`
- `reports/statistics/frequency_profile.csv`
- `docs/decision_log.md`

### Variáveis analisadas

- `purchase_modality`
- `category`
- `status`

### Funções implementadas

- `build_frequency_profile()`
- `validate_frequency_profile()`
- `write_frequency_profile()`

### Estrutura da saída

O arquivo `frequency_profile.csv` contém:

- `variable`
- `category_value`
- `absolute_frequency`
- `percentage`

### Resultado das frequências

Modalidade:

- Pregão: 12 itens — 40,00%
- Dispensa: 9 itens — 30,00%
- Concorrência: 9 itens — 30,00%

Categoria:

- Equipamentos de informática: 8 itens — 26,67%
- Material de escritório: 8 itens — 26,67%
- Serviços de manutenção: 7 itens — 23,33%
- Mobiliário: 7 itens — 23,33%

Situação:

- Publicado: 9 itens — 30,00%
- Concluído: 9 itens — 30,00%
- Em andamento: 7 itens — 23,33%
- Cancelado: 5 itens — 16,67%

### Validações executadas

Para cada variável categórica:

- a soma das frequências absolutas foi igual a 30;
- a soma dos percentuais foi igual a 100%;
- todas as categorias presentes na base foram incluídas;
- nenhuma linha foi excluída ou duplicada no cálculo.

### Regra de granularidade

As frequências representam itens, e não processos.

Um processo com mais de um item contribui com uma ocorrência para cada item existente. A contagem distinta de processos permanece uma métrica separada.

### Segurança

As frequências foram calculadas exclusivamente sobre dados sintéticos. Os resultados não representam comportamento de qualquer instituição real.

### Próxima etapa

Calcular o perfil estatístico das variáveis quantitativas:

- `quantity`
- `estimated_unit_value`
- `estimated_total_value`

---

## 2026-07-21 — Perfil das variáveis quantitativas

### Objetivo

Calcular medidas de posição, separatrizes e dispersão para as variáveis quantitativas da base tratada.

### Arquivos criados ou alterados

- `src/statistical_profile.py`
- `reports/statistics/numeric_profile.csv`
- `docs/decision_log.md`

### Variáveis analisadas

- `quantity`
- `estimated_unit_value`
- `estimated_total_value`

### Funções implementadas

- `build_numeric_profile()`
- `validate_numeric_profile()`
- `write_numeric_profile()`

### Medidas calculadas

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

### Decisão sobre dispersão

A base sintética ampliada representa todo o universo criado para esta versão do projeto.

Por esse motivo, o relatório principal utiliza:

- variância populacional com `ddof=0`;
- desvio padrão populacional com `ddof=0`.

As medidas não devem ser interpretadas como estimativas de uma população externa ou de uma instituição real.

### Resultados de `quantity`

- Contagem: 30
- Média: 74,43
- Mediana: 10,00
- Q1: 4,00
- Q3: 23,75
- IIQ: 19,75
- P90: 128,00
- P95: 365,00
- Desvio médio absoluto: 103,56
- Variância populacional: 38.626,65
- Desvio padrão populacional: 196,54
- Mínimo: 1,00
- Máximo: 1.000,00

### Resultados de `estimated_unit_value`

- Contagem: 30
- Média: 10.453,68
- Mediana: 1.045,00
- Q1: 111,25
- Q3: 3.950,00
- IIQ: 3.838,75
- P90: 9.850,00
- P95: 62.150,00
- Desvio médio absoluto: 15.709,26
- Variância populacional: 964.866.094,37
- Desvio padrão populacional: 31.062,29
- Mínimo: 0,35
- Máximo: 150.000,00

### Resultados de `estimated_total_value`

- Contagem: 30
- Média: 20.237,10
- Mediana: 8.820,00
- Q1: 3.367,50
- Q3: 13.950,00
- IIQ: 10.582,50
- P90: 27.980,00
- P95: 98.250,00
- Desvio médio absoluto: 21.865,16
- Variância populacional: 1.698.996.151,89
- Desvio padrão populacional: 41.218,88
- Mínimo: 350,00
- Máximo: 190.000,00

### Validações executadas

Para cada variável:

- a contagem foi igual a 30;
- mínimo, Q1, mediana, Q3 e máximo ficaram em ordem coerente;
- o intervalo interquartil correspondeu a `Q3 - Q1`;
- P90 não foi superior a P95;
- desvio médio absoluto, variância e desvio padrão não apresentaram valores negativos;
- todas as observações foram numéricas e não nulas.

### Leitura preliminar

Nas três variáveis, a média ficou acima da mediana.

Esse comportamento é compatível com distribuições assimétricas à direita, influenciadas por alguns valores elevados. A constatação é apenas descritiva e será aprofundada na etapa de candidatos a discrepâncias.

### Regra de granularidade

Todas as estatísticas representam itens.

- `quantity` representa quantidade por item;
- `estimated_unit_value` representa valor unitário por item;
- `estimated_total_value` representa quantidade multiplicada pelo valor unitário do item.

Nenhuma dessas distribuições representa valores por processo.

### Limitação

A base possui somente 30 registros sintéticos. P90 e P95 são válidos como demonstração técnica, mas não sustentam generalizações externas.

### Segurança

Todos os resultados foram produzidos com dados sintéticos e não representam compras, valores ou comportamentos de qualquer instituição real.

### Próxima etapa

Comparar `estimated_total_value` por modalidade e categoria e identificar candidatos a discrepâncias pela regra do intervalo interquartil, sem remover registros automaticamente.