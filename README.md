
===============================================
♪ Empório da Música - AI Customer Service Agent
=============================================== 

♪ VISÃO GERAL ♪ 

Este projeto implementa um agente de atendimento para a loja fictícia Empório da Música.

O agente é capaz de responder perguntas sobre:

- Produtos disponíveis
- Status de pedidos
- Promoções ativas
- Políticas da loja
- Situações especiais, como produtos sem estoque, descontinuados e em pré-venda

O objetivo é criar uma experiência simples de atendimento ao cliente, reunindo informações distribuídas em diferentes fontes e fornecendo respostas consistentes de acordo com as regras de negócio definidas no desafio.

♪ TECNOLOGIAS UTILIZADAS ♪

- Python 3.14
- Pandas
- RapidFuzz
- Pytest
- Processamento de PDF
- CLI (Command Line Interface)
- Arquitetura

Para desenvolver o agente optei por separar as responsabilidades de acordo com o domínio das informações consultadas:

Perguntas sobre produtos → são respondidas pelo catálogo.
Perguntas sobre pedidos → consultam a base de pedidos.
Perguntas sobre promoções → acessam a base promocional.
Questões sobre trocas, devoluções, garantia e frete → são respondidas a partir do manual da loja.

Essa organização mantém o código simples, facilita manutenção futura e melhora a consistência das respostas.


          Usuário
             │
             ▼
      Customer Agent
             │
┌────────────┼─────────────┐
▼            ▼             ▼
ProductTool OrderTool PromotionTool
     │       │             │
products.csv orders.csv promotions.csv
 
            │
            ▼
        PolicyRAG
            │
            ▼
    politicas_da_loja.pdf

Cada componente possui uma responsabilidade clara, reduzindo a complexidade do sistema e facilitando futuras evoluções.

♪ DIFERENCIAIS ♪

- Busca aproximada utilizando RapidFuzz.
- Sugestão de alternativas para produtos sem estoque.
- Tratamento de produtos descontinuados.
- Tratamento de produtos em pré-venda.
- Separação clara de responsabilidades por domínio.
- Cobertura de testes automatizados.
- Estrutura preparada para futura integração com LLM.


♪ DECISÕES TÉCNICAS ♪

→ Abordagem

Optei por uma solução baseada em dados estruturados, na qual cada consulta é direcionada para o componente responsável por aquele domínio.

Por exemplo:

Perguntas sobre produtos → consultam o catálogo.
Perguntas sobre pedidos  → consultam a base de pedidos.
Perguntas sobre promoções  → consultam a tabela de promoções.
Perguntas sobre políticas  → utilizam o manual da loja.

Essa abordagem foi escolhida porque os dados fornecidos no desafio já estavam organizados e estruturados, permitindo respostas precisas sem a necessidade de adicionar complexidade desnecessária ao projeto.

→ Modelo e Provedor

Inicialmente considerei utilizar um Large Language Model (LLM) para responder às perguntas dos clientes.

Após analisar os requisitos e os dados fornecidos, concluí que a maior parte das consultas poderia ser respondida diretamente através dos arquivos CSV e do manual da loja.

Dessa forma, optei por uma solução mais simples, transparente e fácil de executar pelos avaliadores, sem exigir:

- Chaves de API
- Créditos em provedores externos
- Configurações adicionais

A solução foi estruturada de forma modular, permitindo a futura integração de um LLM sem alterações significativas na camada de dados.

→ Interface de Interação

Foi utilizada uma interface CLI (Command Line Interface).

Motivações:

- Simplicidade
- Facilidade de avaliação
- Foco na lógica do agente
- Baixa dependência de infraestrutura

Exemplo:

Cliente:
Qual o status do pedido 8?
 
Assistente:
Seu pedido já foi enviado e está em transporte.
Persistência de Histórico

Não foi implementada persistência de conversas.

Durante o desenvolvimento, priorizei os principais objetivos do desafio:

- Consulta de produtos
- Consulta de pedidos
- Consulta de promoções
- Consulta de políticas

Para os cenários propostos as consultas são independentes e não exigem manutenção de contexto entre interações.

Em um cenário de produção, a persistência de histórico poderia ser adicionada para permitir atendimento contextual e retomada de conversas anteriores.

→ Tratamento dos Dados

Os dados estruturados foram carregados utilizando Pandas.

Foram implementadas validações para:

- Produtos sem estoque
- Produtos descontinuados
- Produtos em pré-venda ("coming soon")
- Produtos fora do catálogo da empresa

Também foi utilizada busca aproximada com RapidFuzz para melhorar a experiência do usuário.

Exemplo:

Entrada:
Takamine GD20
 
Resultado encontrado:
Takamine GD20 Dreadnought Natural


♪ FUNCIONALIDADES IMPLEMENTADAS ♪

→ Consulta de Produtos

Exemplo:

Cliente:
Takamine GD20
 
Resposta:
 
Produto: Takamine GD20 Dreadnought Natural
Preço: R$ 2199,00
Estoque: 5
Status: Disponível

→ Consulta de Pedidos

Exemplo:

Cliente:
Qual o status do pedido 8?
 
Resposta:
 
Pedido: 8
Status: Seu pedido já foi enviado e está em transporte.
Código de rastreamento: BRJL5544332BR

→ Consulta de Promoções

Exemplo:

Cliente:
Quais promoções estão ativas?
 
Resposta:
 
Produto
Preço original
Desconto
Preço promocional


→ Consulta de Políticas

Exemplo:

Cliente:
Posso devolver um produto?
 
Resposta:
Compras online podem ser devolvidas em até 7 dias corridos após o recebimento.
Regras de Negócio Implementadas


→ Produto sem estoque

Quando um produto possui estoque igual a zero, o agente sugere alternativas da mesma categoria.


→ Produto descontinuado

Quando um produto está descontinuado, o agente informa a situação e sugere modelos semelhantes.


→ Produto em pré-venda

Produtos marcados como coming_soon recebem tratamento específico.


→ Itens fora do catálogo

O agente reconhece itens não comercializados pela loja, como:

- Cordas
- Cabos
- Pedais
- Cases
- Amplificadores
- Palhetas

Nesses casos, responde adequadamente conforme as regras definidas no manual.


♪ ESTRUTURA DO PROJETO ♪


emporio-musica-agent/
│
├── data/
│ ├── categories.csv
│ ├── customers.csv
│ ├── order_items.csv
│ ├── orders.csv
│ ├── politicas_da_loja.pdf
│ ├── products.csv
│ └── promotions.csv
│
├── examples/
│
├── src/
│ ├── data_loader.py
│ ├── rag.py
│ └── tools.py
│
├── tests/
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt


♪ COMO EXECUTAR ♪ 

Abra seu Prompt de Comando / PowerShell e siga os passos à seguir:

1. Criar ambiente virtual

python -m venv ambiente_virtual

2. Ativar ambiente virtual

ambiente_virtual\Scripts\activate
 
3. Instalar dependências

pip install -r requirements.txt

4. Executar o projeto

python main.py


♪ TESTES ♪ 

Para executar os testes automatizados:

Em seu Prompt de Comando, digite:

python -m pytest

Os testes validam:

- Consulta de produtos
- Busca aproximada
- Pedidos
- Promoções
- Políticas da loja


→ Resultado atual

platform win32 -- Python 3.14
collected 7 items
 
7 passed
Limitações
Não possui memória conversacional.
Não utiliza LLM para geração de respostas.
A consulta ao manual utiliza regras simples em vez de embeddings vetoriais.
Não possui interface web.
O Que Eu Faria Com Mais Tempo


Prioridades para uma evolução futura:

- Integração com LLM utilizando Function Calling
- RAG vetorial baseado em embeddings
- LangGraph para orquestração do agente
- Interface web
- Memória conversacional
- Testes de integração


♪ USO DE ASSISTENTE DE IA ♪

Foi utilizado o Copilot como ferramenta de apoio durante o desenvolvimento para:

- Esclarecimento de dúvidas técnicas
- Discussão de arquitetura
- Revisão da documentação
- Organização da estrutura do projeto
- Apoio na implementação

Todas as decisões de arquitetura, adaptações dos componentes e validações dos resultados foram realizadas manualmente.

♪ CONCLUSÃO ♪

A solução proposta atende aos requisitos do desafio por meio de uma arquitetura simples, modular e de fácil manutenção, priorizando a confiabilidade, transparência e facilidade de avaliação. Além de cumprir os cenários solicitados, a estrutura do projeto foi preparada para futuras evoluções, incluindo integração com LLMs, RAG vetorial e interfaces mais avançadas.