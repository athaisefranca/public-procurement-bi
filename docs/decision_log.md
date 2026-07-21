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

---

## 2026-07-21 — Comparações por grupo e candidatos a discrepâncias

### Objetivo

Comparar a distribuição do valor total estimado entre modalidades e categorias e identificar observações candidatas a discrepâncias pela regra do intervalo interquartil.

### Arquivos criados ou alterados

- `src/statistical_profile.py`
- `reports/statistics/group_profile.csv`
- `reports/statistics/outlier_candidates.csv`
- `reports/statistics/statistical_report.md`
- `docs/decision_log.md`

### Funções implementadas

- `build_group_profile()`
- `validate_group_profile()`
- `write_group_profile()`
- `build_outlier_candidates()`
- `validate_outlier_candidates()`
- `write_outlier_candidates()`
- `write_statistical_report()`

### Comparações realizadas

A variável `estimated_total_value` foi comparada por:

- `purchase_modality`;
- `category`.

Para cada grupo foram calculados:

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

### Resultados por modalidade

- Concorrência: 9 itens, média 45.020,56 e mediana 9.250,00.
- Dispensa: 9 itens, média 6.905,56 e mediana 5.250,00.
- Pregão: 12 itens, média 11.648,17 e mediana 8.000,00.

A soma das contagens por modalidade foi igual a 30 itens.

### Resultados por categoria

- Equipamentos de informática: 8 itens, média 34.768,75 e mediana 11.200,00.
- Material de escritório: 8 itens, média 1.446,62 e mediana 859,00.
- Mobiliário: 7 itens, média 9.777,14 e mediana 9.000,00.
- Serviços de manutenção: 7 itens, média 35.564,29 e mediana 22.000,00.

A soma das contagens por categoria foi igual a 30 itens.

### Regra para candidatos a discrepâncias

Foram usados os limites convencionais:

```text
limite inferior = Q1 - 1,5 × IIQ
limite superior = Q3 + 1,5 × IIQ
```

Os registros encontrados são candidatos a observações discrepantes, não erros confirmados.

Nenhum item foi removido, corrigido ou alterado automaticamente.

### Ocorrências identificadas

Foram identificadas 12 ocorrências:

- `quantity`: 6;
- `estimated_unit_value`: 3;
- `estimated_total_value`: 3.

Uma ocorrência representa a combinação entre um item e uma variável. Um mesmo item pode aparecer em mais de uma variável.

### Candidatos em `quantity`

- P002 / I001: 100
- P011 / I001: 80
- P019 / I001: 500
- P023 / I001: 120
- P027 / I001: 200
- P031 / I001: 1.000

Limite superior calculado: 53,38.

### Candidatos em `estimated_unit_value`

- P013 / I001: 22.000,00
- P022 / I001: 95.000,00
- P025 / I001: 150.000,00

Limite superior calculado: 9.708,12.

### Candidatos em `estimated_total_value`

- P001 / I001: 35.000,00
- P022 / I001: 190.000,00
- P025 / I001: 150.000,00

Limite superior calculado: 29.823,75.

### Interpretação

As diferenças entre média e mediana e os elevados desvios padrão indicam forte influência dos maiores valores em alguns grupos.

Como a base é pequena e sintética, esses resultados servem para demonstrar as técnicas estatísticas e não sustentam conclusões externas.

### Regra de granularidade

Todas as comparações permanecem no nível de item.

Os valores não foram agregados por processo e nenhuma distribuição de itens foi apresentada como distribuição de processos.

### Relatório reproduzível

Foi criado `reports/statistics/statistical_report.md`, gerado automaticamente a partir da base tratada.

O relatório reúne:

- diagnóstico estrutural;
- frequências categóricas;
- perfil numérico;
- comparações por grupo;
- candidatos a discrepâncias;
- limitações.

### Segurança

A análise utiliza exclusivamente dados sintéticos. Nenhum valor ou resultado representa uma compra ou instituição real.

### Próxima etapa

Executar os testes finais, atualizar o README e o dicionário de dados e concluir a entrega estatística.

---

## 2026-07-21 — Encerramento da camada de perfil estatístico

### Objetivo

Concluir a aplicação do curso Estatística com Python: Frequências e Medidas à Frente 2 — Business Intelligence em Compras Públicas.

A entrega foi integrada ao repositório existente, sem criação de projeto paralelo e sem antecipar SQL, Power Query, DAX ou Power BI.

### Escopo concluído

Foram concluídas as seguintes etapas:

- ampliação controlada da base sintética;
- preparação da camada estatística;
- frequências absolutas e percentuais;
- perfil das variáveis quantitativas;
- comparações por modalidade e categoria;
- identificação de candidatos a discrepâncias;
- geração de relatório estatístico reproduzível;
- testes finais do fluxo completo;
- atualização do README;
- atualização do dicionário de dados.

### Pipeline final

O fluxo atual do projeto é:

```text
data/raw/compras_sinteticas.csv
        ↓
src/validate.py
        ↓
src/transform.py
        ↓
data/processed/compras_tratadas.csv
data/rejected/compras_rejeitadas.csv
reports/quality/quality_report.txt
        ↓
src/statistical_profile.py
        ↓
reports/statistics/frequency_profile.csv
reports/statistics/numeric_profile.csv
reports/statistics/group_profile.csv
reports/statistics/outlier_candidates.csv
reports/statistics/statistical_report.md
```

### Arquivos criados ou atualizados na entrega

Código:

- `src/statistical_profile.py`

Dados sintéticos e derivados:

- `data/raw/compras_sinteticas.csv`
- `data/processed/compras_tratadas.csv`
- `data/rejected/compras_rejeitadas.csv`

Relatórios:

- `reports/quality/quality_report.txt`
- `reports/statistics/frequency_profile.csv`
- `reports/statistics/numeric_profile.csv`
- `reports/statistics/group_profile.csv`
- `reports/statistics/outlier_candidates.csv`
- `reports/statistics/statistical_report.md`

Documentação:

- `README.md`
- `docs/data_dictionary.md`
- `docs/decision_log.md`
- `requirements.txt`

### Resultado final do tratamento

- Registros brutos: 37
- Registros válidos: 30
- Registros rejeitados: 7
- Processos distintos: 28
- Chaves `process_id + item_id` duplicadas na base tratada: 0

### Resultado final da camada estatística

- Linhas do perfil de frequências: 11
- Linhas do perfil numérico: 3
- Linhas do perfil por grupo: 7
- Ocorrências candidatas a discrepâncias: 12
- Candidatos registrados dentro dos limites do IIQ: 0

### Frequências implementadas

Foram calculadas frequências absolutas e percentuais de:

- `purchase_modality`;
- `category`;
- `status`.

As frequências representam itens e fecham em 30 observações e 100% para cada variável.

### Métricas quantitativas implementadas

Para:

- `quantity`;
- `estimated_unit_value`;
- `estimated_total_value`;

foram calculados:

- contagem;
- média;
- mediana;
- Q1;
- Q3;
- intervalo interquartil;
- P90;
- P95;
- desvio médio absoluto;
- variância populacional;
- desvio padrão populacional;
- mínimo;
- máximo.

### Comparações por grupo

A variável `estimated_total_value` foi comparada por:

- modalidade;
- categoria.

As comparações permanecem no nível de item.

### Candidatos a discrepâncias

A identificação utiliza:

```text
limite inferior = Q1 - 1,5 × IIQ
limite superior = Q3 + 1,5 × IIQ
```

Foram identificadas:

- 6 ocorrências em `quantity`;
- 3 ocorrências em `estimated_unit_value`;
- 3 ocorrências em `estimated_total_value`.

Nenhum registro foi removido, corrigido ou substituído automaticamente.

### Granularidade

A unidade de análise permanece:

> uma linha representa um item pertencente a um processo sintético.

A contagem de processos é feita separadamente por `process_id` distinto.

Nenhuma distribuição de itens é apresentada como distribuição de processos.

### Testes finais executados

Foram executados:

```powershell
python -m py_compile src\validate.py
python -m py_compile src\transform.py
python -m py_compile src\statistical_profile.py
python -m src.transform
python -m src.statistical_profile
```

Também foram conferidos:

- número de registros brutos, tratados e rejeitados;
- número de processos distintos;
- ausência de chaves duplicadas;
- quantidade de linhas dos relatórios;
- fechamento das frequências absolutas;
- fechamento dos percentuais;
- fechamento das contagens por grupo;
- candidatos realmente fora dos limites calculados;
- reprodução dos arquivos derivados;
- ausência de alterações inesperadas no Git.

### Resultado dos testes

Todos os testes apresentaram o comportamento esperado.

O repositório permaneceu reproduzível e consistente após a execução completa.

### Segurança

A entrega utiliza exclusivamente dados sintéticos.

Não foram utilizados:

- planilhas profissionais originais;
- dados pessoais;
- comentários internos;
- documentos institucionais;
- fornecedores reais;
- responsáveis reais;
- identificadores sensíveis;
- números de processos reais;
- valores profissionais reais.

Os resultados não representam fatos sobre órgãos, instituições ou compras reais.

### Limites da entrega

Não foram implementados nesta etapa:

- valor homologado;
- base pública oficial;
- análise temporal robusta;
- SQL;
- banco de dados;
- modelagem dimensional;
- Power Query;
- DAX;
- Power BI;
- dashboard;
- remoção automática de discrepâncias.

### Decisão de encerramento

A camada de perfil estatístico da Frente 2 está concluída.

A próxima evolução deverá ocorrer somente quando um novo curso trouxer conteúdo aplicável às camadas futuras do projeto.

### Próximas evoluções previstas

- seleção e documentação de uma base pública oficial;
- avaliação de cobertura e granularidade da fonte;
- adaptação do pipeline ao novo esquema;
- análise temporal;
- banco de dados e SQL;
- modelagem dimensional;
- Power Query;
- DAX;
- Power BI;
- páginas executivas, analíticas e de qualidade.