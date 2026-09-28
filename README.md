# 🧮 Processador Aritmético Vetorial de Base Direta

Projeto desenvolvido para a disciplina **Computação Numérica** na Universidade Federal do Rio Grande do Norte (UFRN).

## 🎯 Visão Geral
Este repositório contém a implementação de um processador aritmético abstrato projetado para realizar conversões e operações elementares em qualquer sistema de numeração posicional (Bases 2 a 36). Diferente da arquitetura tradicional de hardware, que utiliza a base binária como "pivô" intermediário (causando falhas de precisão e truncamento pelo padrão IEEE 754), o nosso sistema computa vetores de caracteres simbólicos nativamente nas bases de origem e destino, utilizando uma ALU (Unidade Lógica e Aritmética) construída em Dicionários Hash.

## 🏆 Prova de Conceito (O Fim do Ruído Digital)
- **O Problema do 0.1 + 0.2:** No hardware tradicional (Python Float64 / IEEE 754), $0.1 + 0.2$ resulta em `0.30000000000000004` devido à perda irreversível de bits na coerção binária de decimais irracionais. Nossa arquitetura vetorial abstrata retorna o valor límpido e matematicamente exato: `0.3`.
- **Preservação de Dízimas Periódicas:** Ao lidarmos com operações infinitas como $1/3$, o hardware padrão trunca o número na 16ª casa decimal. Nosso algoritmo utiliza rastreamento avançado (Dicionário de Estados Hash) para detectar ciclagens algébricas e consolida matematicamente a dízima com a notação formal de parênteses: `0.(3)`.

## 📁 Estrutura do Repositório
- 📄 `main.py` — Ponto de Entrada / Interface de Linha de Comando (CLI) para acesso às conversões, aritmética vetorial e Suíte de Testes Comparativos.
- 📄 `direct_converter.py` e `direct_operations.py` — *Facades* orquestradoras de Alto Nível (Controlam roteamento de sinais, alinhamento *zero-padding* e ponto flutuante).
- 📄 `vector_math.py` e `arithmetic_tables.py` — O "Coração Matemático" de Baixo Nível. Simulador de ALU operando matrizes em tempo $O(1)$.
- 📂 `docs/`
  - `arquitetura.md` — Fluxograma estrutural do fluxo de dados e classes do sistema modelado em Mermaid.
- 📄 `fundamentacao_teorica.md` — Documentação teórica intensiva cobrindo o Método de Horner, Multiplicações Sucessivas e o rigoroso transporte de *Carry* e *Borrow* vetorial.
- 📄 `relatorio_final_projeto_u1.tex` — Artigo acadêmico formatado em LaTeX defendendo a metodologia do processamento posicional abstraído do hardware.

## 🚀 Como Executar Localmente

O projeto foi escrito em Python purista, com **zero dependências proprietárias** (não requer instalação de Numpy ou Pandas).

```bash
# Clone o repositório
git clone https://github.com/Jacsonrn/direct-base-arithmetic.git
cd direct-base-arithmetic

# Execute a CLI Interativa
python main.py
```

## 👨‍💻 Autor
**Jacson Arruda Ribeiro**  
Universidade Federal do Rio Grande do Norte (UFRN) — Instituto Metrópole Digital (IMD)
