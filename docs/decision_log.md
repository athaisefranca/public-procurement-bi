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