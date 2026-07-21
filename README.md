# Business Intelligence em Compras Públicas

Pipeline reproduzível para tratamento, validação e perfil estatístico de dados sintéticos de compras públicas, desenvolvido em Python com foco em qualidade, granularidade e transparência analítica.

> **Dados sintéticos por segurança.** O projeto demonstra método, organização e capacidade analítica sem reproduzir planilhas profissionais, dados pessoais ou informações institucionais reais.

---

## O problema

Como transformar uma base de itens de compras públicas em informações confiáveis, evitando registros inválidos, duplicidades, mistura de granularidades e interpretações distorcidas por valores extremos?

Bases administrativas podem conter problemas de preenchimento, diferentes níveis de detalhe e distribuições muito assimétricas. Antes da criação de indicadores ou dashboards, é necessário validar a estrutura, documentar as regras e conhecer o comportamento dos dados.

## Resultado

O pipeline processou 37 registros sintéticos:

- 30 itens válidos;
- 7 registros rejeitados;
- 28 processos distintos;
- nenhuma chave processo-item duplicada.

O valor total estimado por item apresentou média de **20.237,10** e mediana de **8.820,00**. A diferença entre as duas medidas indica influência de poucos itens com valores elevados.

Foram identificadas **12 ocorrências candidatas a discrepâncias** pelo critério de 1,5 × intervalo interquartil. Esses registros foram mantidos na base, pois candidato a discrepância não significa erro.

| Indicador | Resultado |
|---|---:|
| Registros brutos | 37 |
| Itens válidos | 30 |
| Registros rejeitados | 7 |
| Processos distintos | 28 |
| Chaves duplicadas na base tratada | 0 |
| Média do valor total estimado | 20.237,10 |
| Mediana do valor total estimado | 8.820,00 |
| P90 do valor total estimado | 27.980,00 |
| P95 do valor total estimado | 98.250,00 |
| Ocorrências candidatas a discrepâncias | 12 |

---

## O que o projeto faz

- **Valida a entrada** — existência do arquivo, colunas obrigatórias, campos vazios, datas, números positivos e valores categóricos permitidos.
- **Detecta duplicidades** — a combinação entre `process_id` e `item_id` deve ser única.
- **Separa registros inválidos** — linhas rejeitadas são preservadas com o respectivo motivo.
- **Transforma registros válidos** — padroniza textos, converte datas e números e calcula o valor total estimado.
- **Gera relatório de qualidade** — registra quantidades lidas, válidas e rejeitadas.
- **Calcula frequências categóricas** — frequências absolutas e percentuais de modalidade, categoria e situação.
- **Produz perfil numérico** — média, mediana, quartis, intervalo interquartil, P90, P95 e medidas de dispersão.
- **Compara grupos** — distribuição do valor total estimado por modalidade e categoria.
- **Identifica candidatos a discrepâncias** — aplicação da regra de 1,5 × IIQ sem remoção automática.
- **Gera relatório estatístico** — consolida resultados, granularidade e limitações em Markdown.

## Granularidade

A unidade de análise principal é o item de compra.

> Uma linha representa um item pertencente a um processo sintético.

Um processo pode conter mais de um item. Por isso:

- a quantidade de itens corresponde ao número de linhas válidas;
- a quantidade de processos é calculada por `process_id` distinto;
- distribuições de itens não são apresentadas como distribuições de processos;
- valores de diferentes granularidades não são misturados.

A chave da base tratada é composta por:

```text
process_id + item_id
```

## Variáveis analisadas

### Qualitativas

- `purchase_modality`
- `category`
- `status`

### Quantitativas

- `quantity`
- `estimated_unit_value`
- `estimated_total_value`

O campo `estimated_total_value` é calculado por:

```text
estimated_total_value = quantity × estimated_unit_value
```

Não existe valor homologado nesta versão do projeto.

## Frequências categóricas

A base tratada apresenta a seguinte distribuição por modalidade:

| Modalidade | Itens | Participação |
|---|---:|---:|
| Pregão | 12 | 40,00% |
| Dispensa | 9 | 30,00% |
| Concorrência | 9 | 30,00% |

Distribuição por categoria:

| Categoria | Itens | Participação |
|---|---:|---:|
| Equipamentos de informática | 8 | 26,67% |
| Material de escritório | 8 | 26,67% |
| Serviços de manutenção | 7 | 23,33% |
| Mobiliário | 7 | 23,33% |

Distribuição por situação:

| Situação | Itens | Participação |
|---|---:|---:|
| Publicado | 9 | 30,00% |
| Concluído | 9 | 30,00% |
| Em andamento | 7 | 23,33% |
| Cancelado | 5 | 16,67% |

## Perfil numérico

| Variável | Média | Mediana | Q1 | Q3 | P90 | P95 | Desvio padrão |
|---|---:|---:|---:|---:|---:|---:|---:|
| Quantidade | 74,43 | 10,00 | 4,00 | 23,75 | 128,00 | 365,00 | 196,54 |
| Valor unitário estimado | 10.453,68 | 1.045,00 | 111,25 | 3.950,00 | 9.850,00 | 62.150,00 | 31.062,29 |
| Valor total estimado | 20.237,10 | 8.820,00 | 3.367,50 | 13.950,00 | 27.980,00 | 98.250,00 | 41.218,88 |

A média ficou acima da mediana nas três variáveis. Esse comportamento é compatível com distribuições assimétricas à direita, influenciadas pelos maiores valores.

A variância e o desvio padrão utilizados são populacionais, com `ddof=0`, pois os dados representam todo o universo sintético criado para esta versão.

## Comparação por modalidade

| Modalidade | Itens | Média do valor total | Mediana | P90 | Desvio padrão |
|---|---:|---:|---:|---:|---:|
| Concorrência | 9 | 45.020,56 | 9.250,00 | 158.000,00 | 67.767,37 |
| Dispensa | 9 | 6.905,56 | 5.250,00 | 11.100,00 | 3.920,29 |
| Pregão | 12 | 11.648,17 | 8.000,00 | 27.000,00 | 11.131,90 |

A modalidade Concorrência apresenta média muito superior à mediana, influenciada pelos maiores valores sintéticos da base.

## Comparação por categoria

| Categoria | Itens | Média do valor total | Mediana | P90 | Desvio padrão |
|---|---:|---:|---:|---:|---:|
| Equipamentos de informática | 8 | 34.768,75 | 11.200,00 | 81.500,00 | 59.368,47 |
| Material de escritório | 8 | 1.446,62 | 859,00 | 3.391,00 | 1.226,88 |
| Mobiliário | 7 | 9.777,14 | 9.000,00 | 15.108,00 | 4.052,77 |
| Serviços de manutenção | 7 | 35.564,29 | 22.000,00 | 76.320,00 | 47.391,38 |

Equipamentos de informática e Serviços de manutenção apresentam maior dispersão e influência de valores elevados.

## Candidatos a discrepâncias

Os limites são calculados por:

```text
limite inferior = Q1 - 1,5 × IIQ
limite superior = Q3 + 1,5 × IIQ
```

Foram identificadas:

- 6 ocorrências em `quantity`;
- 3 ocorrências em `estimated_unit_value`;
- 3 ocorrências em `estimated_total_value`.

Uma ocorrência representa a combinação entre item e variável. O mesmo item pode aparecer em mais de uma variável.

Nenhum registro foi removido, corrigido ou substituído automaticamente.

## Estrutura

```text
data/raw/compras_sinteticas.csv
    Base bruta sintética e imutável.

data/processed/compras_tratadas.csv
    Registros aprovados e transformados.

data/rejected/compras_rejeitadas.csv
    Registros rejeitados e respectivos motivos.

src/validate.py
    Regras de validação dos registros.

src/transform.py
    Leitura, transformação, separação e gravação dos dados.

src/statistical_profile.py
    Perfil estatístico, comparações e relatório reproduzível.

reports/quality/quality_report.txt
    Resumo da qualidade do pipeline.

reports/statistics/frequency_profile.csv
    Frequências absolutas e percentuais.

reports/statistics/numeric_profile.csv
    Medidas de posição, separatrizes e dispersão.

reports/statistics/group_profile.csv
    Comparações do valor total por modalidade e categoria.

reports/statistics/outlier_candidates.csv
    Candidatos a discrepâncias pela regra do IIQ.

reports/statistics/statistical_report.md
    Relatório consolidado gerado automaticamente.

docs/data_dictionary.md
    Definições, tipos e regras dos campos.

docs/decision_log.md
    Registro das decisões de desenvolvimento.
```

## Como executar

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute o tratamento:

```powershell
python -m src.transform
```

Execute o perfil estatístico:

```powershell
python -m src.statistical_profile
```

Arquivos da pasta `reports/statistics` serão criados ou atualizados automaticamente.

## Testes e validações

Foram executadas verificações de:

- sintaxe dos três módulos;
- existência e estrutura dos arquivos;
- campos obrigatórios;
- datas e valores numéricos;
- valores categóricos controlados;
- duplicidades;
- contagens das camadas bruta, tratada e rejeitada;
- totais das frequências;
- fechamento dos percentuais;
- ordenação de mínimo, quartis, mediana e máximo;
- cálculo do intervalo interquartil;
- consistência de P90 e P95;
- medidas de dispersão não negativas;
- contagens por modalidade e categoria;
- candidatos fora dos limites do IIQ;
- reprodução completa dos relatórios.

Resultados finais:

```text
Registros brutos: 37
Itens válidos: 30
Registros rejeitados: 7
Processos distintos: 28
Chaves duplicadas: 0
Linhas do perfil de frequências: 11
Linhas do perfil numérico: 3
Linhas do perfil por grupo: 7
Ocorrências candidatas a discrepâncias: 12
Candidatos dentro dos limites: 0
```

## Decisões técnicas

**Por que dados sintéticos.** O projeto foi inspirado em experiências com organização e análise de dados administrativos, mas foi integralmente reconstruído para preservar segurança, privacidade e sigilo.

**Por que preservar a camada bruta.** A entrada não é sobrescrita. Isso permite rastrear a origem dos registros e reproduzir o tratamento.

**Por que separar rejeições.** Registros inválidos não desaparecem silenciosamente. Eles são preservados com o motivo da rejeição.

**Por que item como unidade de análise.** Um processo pode conter vários itens. Fixar a granularidade evita dupla contagem e indicadores incorretos.

**Por que média e mediana.** Distribuições monetárias podem ser assimétricas. A mediana ajuda a representar o valor típico sem depender apenas da média.

**Por que não remover discrepâncias.** Um valor extremo pode ser válido. A regra do IIQ apenas seleciona candidatos para investigação.

## Limitações

- A base possui somente 30 itens válidos.
- Todos os dados são sintéticos.
- Os grupos possuem poucas observações.
- Os percentis são demonstrativos e sensíveis ao tamanho da base.
- Os resultados não representam instituições ou compras reais.
- Não existe valor homologado.
- Não existe base pública oficial integrada.
- Não há análise temporal robusta.
- Não há banco de dados ou SQL.
- Não há modelagem dimensional.
- Não há Power Query, DAX ou Power BI.
- Não há remoção automática de valores extremos.

## Próximos passos

1. Selecionar uma base pública oficial e documentar fonte, período e licença.
2. Avaliar granularidade, cobertura e qualidade da fonte pública.
3. Adaptar o pipeline para o novo esquema sem perder a camada sintética de testes.
4. Criar análises temporais quando houver período suficiente.
5. Implementar banco de dados e consultas SQL.
6. Desenvolver modelagem dimensional.
7. Integrar Power Query e Power BI em uma etapa futura.
8. Criar páginas executivas, analíticas e de qualidade.

---

**Tecnologias:** Python · pandas · NumPy

Desenvolvido por [Thaise França Coelho](https://www.linkedin.com/in/athaisefranca)