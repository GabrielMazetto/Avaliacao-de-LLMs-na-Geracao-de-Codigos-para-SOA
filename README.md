# Avaliação de LLMs na Geração de Códigos para SOA

## Sobre o Projeto

Este repositório documenta um estudo prático para avaliar e comparar a qualidade do código gerado por dois Grandes Modelos de Linguagem (LLMs) de ponta: **Gemini 2.5 Pro** e **ChatGPT-5**.

O desafio central consistiu em gerar uma API completa em Python para uma Arquitetura Orientada a Serviços (SOA), expondo quatro modelos de IA simulados e protegida por autenticação via token. O objetivo foi analisar não apenas se os modelos poderiam gerar código funcional, mas também o quão bem esse código aderia a boas práticas de segurança e validação de dados a partir de um único prompt.

## Metodologia

1.  Um **prompt único e detalhado**, descrevendo o problema de negócio e os requisitos técnicos, foi submetido a ambos os modelos.
2.  As **soluções de código completas** foram salvas sem nenhuma alteração.
3.  Uma **suíte de 15 testes sistemáticos** foi desenvolvida e executada para validar rigorosamente cada API, cobrindo:
    *   Segurança da autenticação (tokens inválidos, ausentes e formato incorreto).
    *   Validação de regras de negócio (e.g., dados fora de um intervalo válido).
    *   Validação de tipos de dados (e.g., strings onde se esperam números).
    *   Tratamento de casos de borda (e.g., entradas vazias).

## Principais Achados

Os resultados revelaram um trade-off interessante entre as soluções geradas:

*   **Nenhuma solução foi perfeita:** Ambos os modelos geraram código funcional, mas com falhas distintas que seriam críticas em um ambiente de produção.
*   **Gemini 2.5 Pro:** Apresentou uma excelente validação de dados de negócio, passando em todos os testes relacionados. No entanto, falhou em um teste de segurança ao não validar estritamente o formato do cabeçalho de autorização.
*   **ChatGPT-5:** Implementou uma camada de autenticação mais segura, passando em todos os testes de segurança. Contudo, falhou em 3 testes de validação de dados, aceitando entradas inválidas que poderiam levar a erros ou comportamento inesperado no sistema.

O estudo conclui que, embora os LLMs sejam aceleradores de desenvolvimento extremamente poderosos, a supervisão, o conhecimento crítico e a validação por parte de um especialista humano continuam sendo indispensáveis para garantir a qualidade, a segurança e a confiabilidade do software.

## Estrutura do Repositório

*   **/projeto_ia_servicos**: Contém o código completo gerado pelo Gemini 2.5 Pro, além de um script de testes.
*   **/ia_service**: Contém o código completo gerado pelo ChatGPT-5, além de um script de testes.
*   **Resposta Gemini 2.5 Pro.pdf**: A resposta exata dada pelo modelo Gemini 2.5 Pro.
*   **Resposta ChatGPT 5.pdf**: A resposta exata dada pelo modelo ChatGPT 5.
*   **Relatorio_Avaliacao_LLMs.pdf**: O relatório final detalhado deste estudo.
