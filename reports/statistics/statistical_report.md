# Relatório estatístico da base sintética

## Contexto

Este relatório foi gerado automaticamente a partir de `data/processed/compras_tratadas.csv`.

A unidade de análise é o item de compra:

> uma linha representa um item pertencente a um processo sintético.

Os resultados são demonstrativos e não representam qualquer instituição real.

## Diagnóstico estrutural

- Itens analisados: 30
- Processos distintos: 28
- Chaves processo-item únicas: 30
- Chaves duplicadas: 0

## Frequências categóricas

### `purchase_modality`

- Pregão: 12 itens (40.00%)
- Dispensa: 9 itens (30.00%)
- Concorrência: 9 itens (30.00%)

### `category`

- Equipamentos de informática: 8 itens (26.67%)
- Material de escritório: 8 itens (26.67%)
- Serviços de manutenção: 7 itens (23.33%)
- Mobiliário: 7 itens (23.33%)

### `status`

- Publicado: 9 itens (30.00%)
- Concluído: 9 itens (30.00%)
- Em andamento: 7 itens (23.33%)
- Cancelado: 5 itens (16.67%)

## Perfil numérico

### `quantity`

- Contagem: 30
- Média: 74.43
- Mediana: 10.00
- Q1: 4.00
- Q3: 23.75
- IIQ: 19.75
- P90: 128.00
- P95: 365.00
- Desvio médio absoluto: 103.56
- Variância populacional: 38626.65
- Desvio padrão populacional: 196.54
- Mínimo: 1.00
- Máximo: 1000.00

### `estimated_unit_value`

- Contagem: 30
- Média: 10453.68
- Mediana: 1045.00
- Q1: 111.25
- Q3: 3950.00
- IIQ: 3838.75
- P90: 9850.00
- P95: 62150.00
- Desvio médio absoluto: 15709.26
- Variância populacional: 964866094.37
- Desvio padrão populacional: 31062.29
- Mínimo: 0.35
- Máximo: 150000.00

### `estimated_total_value`

- Contagem: 30
- Média: 20237.10
- Mediana: 8820.00
- Q1: 3367.50
- Q3: 13950.00
- IIQ: 10582.50
- P90: 27980.00
- P95: 98250.00
- Desvio médio absoluto: 21865.16
- Variância populacional: 1698996151.89
- Desvio padrão populacional: 41218.88
- Mínimo: 350.00
- Máximo: 190000.00

## Comparação do valor total estimado

As comparações abaixo permanecem no nível de item.

### Por `purchase_modality`

- Concorrência: n=9, média=45020.56, mediana=9250.00, P90=158000.00, desvio padrão populacional=67767.37
- Dispensa: n=9, média=6905.56, mediana=5250.00, P90=11100.00, desvio padrão populacional=3920.29
- Pregão: n=12, média=11648.17, mediana=8000.00, P90=27000.00, desvio padrão populacional=11131.90

### Por `category`

- Equipamentos de informática: n=8, média=34768.75, mediana=11200.00, P90=81500.00, desvio padrão populacional=59368.47
- Material de escritório: n=8, média=1446.62, mediana=859.00, P90=3391.00, desvio padrão populacional=1226.88
- Mobiliário: n=7, média=9777.14, mediana=9000.00, P90=15108.00, desvio padrão populacional=4052.77
- Serviços de manutenção: n=7, média=35564.29, mediana=22000.00, P90=76320.00, desvio padrão populacional=47391.38

## Candidatos a discrepâncias

A identificação utiliza os limites convencionais `Q1 - 1,5 × IIQ` e `Q3 + 1,5 × IIQ`.

Os registros não foram removidos nem corrigidos automaticamente.

Total de ocorrências identificadas: 12

### `quantity`

- P002 / I001: valor=100.00; limite superior=53.38
- P011 / I001: valor=80.00; limite superior=53.38
- P019 / I001: valor=500.00; limite superior=53.38
- P023 / I001: valor=120.00; limite superior=53.38
- P027 / I001: valor=200.00; limite superior=53.38
- P031 / I001: valor=1000.00; limite superior=53.38

### `estimated_unit_value`

- P013 / I001: valor=22000.00; limite superior=9708.12
- P022 / I001: valor=95000.00; limite superior=9708.12
- P025 / I001: valor=150000.00; limite superior=9708.12

### `estimated_total_value`

- P001 / I001: valor=35000.00; limite superior=29823.75
- P022 / I001: valor=190000.00; limite superior=29823.75
- P025 / I001: valor=150000.00; limite superior=29823.75

## Limitações

- A base contém somente 30 itens sintéticos.
- Os grupos possuem poucas observações.
- Média, percentis e dispersão podem ser fortemente influenciados pelos maiores valores.
- Candidato a discrepância não significa erro.
- Não existe valor homologado nesta versão da base.
- Não devem ser feitas generalizações externas.
