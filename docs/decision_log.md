# Registro de decisões

## 2026-07-17 — Fundação inicial do projeto

### Contexto

Início da continuidade da Frente 2 — Business Intelligence em Compras Públicas.

O projeto será desenvolvido progressivamente, sem criar projetos paralelos para cada curso concluído.

### Decisões tomadas

- Nome do repositório: `public-procurement-bi`.
- Branch principal: `main`.
- Primeira etapa restrita à fundação técnica do pipeline.
- Uso exclusivo de dados sintéticos nesta primeira entrega.
- Uso apenas da biblioteca padrão do Python.
- Separação entre dados brutos, tratados, rejeitados, código e documentação.
- Uso de funções, type hints, docstrings e exceções desde o início.
- Não utilização, nesta fase, de pandas, SQL, Power Query, DAX, Power BI ou modelagem dimensional completa.
- A camada `data/raw` será preservada e não deverá ser sobrescrita pelo pipeline.
- Registros inválidos serão separados em `data/rejected`.
- Relatórios de qualidade serão armazenados em `reports/quality`.

### Motivo

A estrutura permite aplicar os conhecimentos atuais de Python de forma concreta e segura, sem antecipar conteúdos ainda não estudados suficientemente.

### Segurança

O projeto não utilizará:

- planilhas profissionais originais;
- classificações internas;
- comentários ou responsáveis reais;
- documentos institucionais;
- dados pessoais desnecessários;
- identificadores profissionais protegidos.

### Pendências

- Definir as colunas da base sintética.
- Criar o dicionário de dados.
- Criar o arquivo bruto inicial.
- Definir regras de validação e transformação.
- Implementar e testar o pipeline.

## 2026-07-17 — Definição da estrutura da base sintética

### Unidade de análise

Cada linha representará um item pertencente a um processo sintético de compra pública.

Um processo poderá possuir vários itens. A combinação entre `process_id` e `item_id` deverá ser única.

### Colunas definidas

- `process_id`
- `item_id`
- `publication_date`
- `organization_code`
- `purchase_modality`
- `category`
- `item_description`
- `quantity`
- `estimated_unit_value`
- `status`

### Decisões de escopo

- Todas as dez colunas serão obrigatórias.
- A primeira base utilizará somente dados sintéticos.
- Não serão incluídos fornecedores, responsáveis, documentos, contatos ou identificadores reais.
- A base bruta não conterá valor total estimado.
- O valor total poderá ser calculado durante a transformação.
- Modalidades, categorias e situações utilizarão listas pequenas de valores controlados.
- A estrutura permanece limitada aos conhecimentos das duas consolidações de Python.

### Próxima etapa

Criar o arquivo `data/raw/compras_sinteticas.csv` com registros válidos e registros intencionalmente problemáticos para testar as regras documentadas.

## 2026-07-17 — Regras de validação da base sintética

### Estrutura do arquivo

- O arquivo de entrada deve existir.
- O cabeçalho deve conter todas as dez colunas obrigatórias.
- A ausência de qualquer coluna deverá interromper o processamento com erro claro.

### Campos obrigatórios

Todos os campos deverão possuir valor após a remoção de espaços externos.

### Chave do registro

A combinação entre `process_id` e `item_id` deverá ser única.

Registros com chave repetida serão rejeitados como duplicados.

### Data de publicação

- O formato de entrada deverá ser `DD/MM/AAAA`.
- A data deverá existir no calendário.
- O formato tratado será `AAAA-MM-DD`.

### Quantidade

- Deverá ser convertível para `float`.
- Deverá ser maior que zero.

### Valor unitário estimado

- Deverá ser convertível para `float`.
- Deverá ser maior que zero.

### Valores controlados

Modalidades permitidas:

- `Pregão`
- `Dispensa`
- `Concorrência`

Categorias permitidas:

- `Material de escritório`
- `Equipamentos de informática`
- `Serviços de manutenção`
- `Mobiliário`

Situações permitidas:

- `Publicado`
- `Em andamento`
- `Concluído`
- `Cancelado`

### Resultado da validação

- Registros sem erros seguirão para a camada tratada.
- Registros com um ou mais erros seguirão para a camada de rejeitados.
- Cada registro rejeitado deverá armazenar todos os motivos encontrados.

### Exceções previstas

- `FileNotFoundError`: arquivo de entrada não encontrado.
- `KeyError`: campo esperado ausente durante o acesso ao registro.
- `ValueError`: data, quantidade ou valor inválido.
- `TypeError`: argumento de tipo incompatível fornecido a uma função.