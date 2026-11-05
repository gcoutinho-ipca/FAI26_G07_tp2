# Pendentes do Projeto 02 (FAI, G07)

Ponto de situação a **05/11/2026**. Este é o ficheiro de entrada: diz o que já está feito, o que falta decidir e o que falta fazer, em blocos pequenos.

## Como ler a documentação

| Ficheiro | Para que serve |
|---|---|
| `pendentes.md` (este) | Onde estamos e qual é o próximo bloco |
| [`decisoes.md`](decisoes.md) | Registo de **todas** as decisões (D01, D02…), com as alternativas e a justificação |
| [`project_status.md`](project_status.md) | Visão geral do projeto e, na **secção 3A**, os passos do tratamento de dados do NB1 por ordem |
| [`inventario.md`](inventario.md) | Requisitos do guia (R1-R27), conteúdo dos slides (FAI31-34) e orientações orais (O1-O5) |

**Método de trabalho:** um bloco de cada vez. Cada bloco é pequeno e só avança depois de os dois percebermos o que foi feito. Antes de cada bloco tomam-se as decisões necessárias, que vão logo para o `decisoes.md`.

## Guidelines mandatórias (orientação oral do docente, 04/11/2026)

> Prevalecem sobre o guia escrito. Detalhe em `inventario.md`, secção E.

- **O1:** trabalho **simples**
- **O2:** **dois notebooks**: NB1 = preparação + EDA + árvore de decisão · NB2 = K-Means
- **O3:** poder **«jogar» com as variáveis**: parâmetros no topo e registo das experiências
- **O4:** cada notebook segue as fases do **CRISP-DM** (Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment)
- **O5:** **sem bibliotecas de ML**: árvore de decisão (ID3) e K-Means implementados à mão, com a heurística parametrizável. Só numpy, pandas, matplotlib e seaborn
- **Regra do grupo:** todo o código é **comentado de forma explicativa**, para se perceber a lógica de cada passo

---

## 1. O que já está feito

| Quando | O quê | Onde |
|---|---|---|
| 04/11 | Guia e slides do docente, inventário das fontes e orientações orais | `docs/material/`, `inventario.md` |
| 04/11 | Ambiente `.venv` (numpy 2.5.4, pandas 3.1.1, matplotlib 3.11.2, seaborn 0.13.2, jupyter) | `.venv/` |
| 04/11 | Dataset escolhido para o NB1: `portugal_listinigs.csv` (190 867 linhas, 23 colunas) e EDA inicial | `data/archive/`, `src/eda_inicial.py` |
| 05/11 | Plano dos notebooks alinhado com a O2 | D01 |
| 05/11 | O rascunho inicial de preparação (`notebook_1_data_treatment.py`) fica só como referência | D02 |
| 05/11 | **Alvo do ID3:** caro/barato face à mediana do preço **por distrito** | D03, D05 |
| 05/11 | **Universo:** só Apartment + House com preço, sem os distritos com menos de 100 anúncios | D04, D06 |
| 05/11 | **8 atributos:** `Type`, `TotalArea`, `LivingArea`, `NumberOfBathrooms`, `Parking`, `ConstructionYear`, `EnergyCertificate`, `Elevator` | D07 |
| 05/11 | Removidas as linhas com nulo em `NumberOfBathrooms` ou `Elevator`: ficam **121 679 linhas**, com o alvo **49,6% caro** | D09 |

**Ainda não há código do modelo.** Até aqui só se tomaram decisões, confirmadas com contas sobre os dados reais.

---

## 2. O que falta decidir

### 2.1 Para decidir já (bloqueiam os próximos blocos)

| # | Decisão | Proposta | Quem |
|---|---|---|---|
| **D08** | Nulos do `ConstructionYear` (14,6%; o nulo tem 71,8% caros) | Categoria «Desconhecido» (FAI33 p.14). Os dados e as opções estão em `decisoes.md` | **Gilberto + Rúbem** |
| Q10 | Divisão das tarefas: quem fica com o NB1 (árvore) e quem fica com o NB2 (K-Means) (R9) | NB1: ______ · NB2: ______ | Gilberto + Rúbem |

### 2.2 Para decidir quando lá chegarmos

| # | Decisão | Proposta | Bloco |
|---|---|---|---|
| Q17 | Erros e outliers (`NumberOfBathrooms` com o máximo de 3 020; áreas extremas; picos nos anos 1937 e 1951) | Ver os dados no bloco P4 | P4 |
| Q18 | Discretização dos contínuos para o ID3: largura igual ou frequência igual, e quantos intervalos | Frequência igual (quantis), com o nº de intervalos como parâmetro (FAI33 p.18-19) | P5 |
| Q15 | Tamanho da amostra para a árvore em Python puro | Testar a velocidade com uma amostra estratificada e decidir com base nisso | P6 |
| Q12 | Classes desequilibradas | Provavelmente desnecessário, porque o alvo está 49,6/50,4. Fica só a separação dos 30% para o teste final (FAI33 p.28) | P6 |
| Q3 | Afinação dos hiperparâmetros | Ciclo explícito sobre os valores candidatos + 10-fold CV estratificada (FAI33 p.34) | A9 |
| Q13 | Só a árvore, ou a árvore e um 2.º algoritmo? (guia R14 vs O2) | **Confirmar com o docente** | A9 |
| Q14 | O NB2 usa o mesmo dataset? Com que atributos? | Por decidir no bloco K1 | K1 |
| Q5 | Escolha de k no K-Means | Cotovelo sobre o SSE (FAI32 p.27) | K4 |
| Q6 | Normalizar antes do K-Means | Sim (FAI32 p.26). Primeiro tratar os outliers, que senão comprimem a escala | K2 |
| Q11 | Versões das bibliotecas | Fixar as do `.venv` num `requirements.txt` | N1 |

### 2.3 Já decididas (histórico)

| # | Decisão | Resultado |
|---|---|---|
| Q1 | Biblioteca de ML | Nenhuma: implementação própria (O5) ✔ |
| Q2 | Algoritmo de classificação | Árvore de decisão ID3 (O2) ✔ |
| Q4 | Regras de associação | Não (O1, O2) ✔ |
| Q7 | Dataset do NB1 | `portugal_listinigs.csv` ✔ |
| Q16 | Alvo do ID3 | Caro/barato por distrito ✔ (D03-D06) |

---

## 3. O que falta fazer, em blocos

Cada bloco é pequeno: um objetivo, um resultado que se possa verificar e uma decisão (se for precisa). Estado: ✔ feito · ◐ em curso · ☐ por fazer.

### P: Preparação dos dados do NB1

| Bloco | Objetivo | Depende de | Resultado | Estado |
|---|---|---|---|---|
| P1 | Definir o alvo e o universo | n.a. | D03-D06 | ✔ |
| P2 | Escolher os atributos | P1 | D07 | ✔ |
| P3 | Valores em falta | P2 | D09 ✔ · **D08 pendente** | ◐ |
| P4 | Erros e outliers | P3 | Decisão Q17 | ☐ |
| P5 | Discretizar os contínuos (área, ano, casas de banho) | P4 | Decisão Q18 + função de discretização comentada | ☐ |
| P6 | Amostra e divisão estratificada treino/teste (70/30) feita à mão | P5 | Função de divisão comentada | ☐ |

### A: Algoritmo da árvore de decisão (não depende dos dados)

| Bloco | Objetivo | Teste | Estado |
|---|---|---|---|
| A1 | Função de **entropia** `E = −Σ p_i log2(p_i)` (FAI32 p.16) | Exemplo «Restaurant» com as contas feitas à mão | ☐ |
| A2 | Função do **índice de Gini** (alternativa à entropia) | Restaurant | ☐ |
| A3 | **Ganho de informação** de um atributo | Restaurant: *Patrons* tem o maior ganho (FAI32 p.17-18) | ☐ |
| A4 | Escolher o melhor atributo num nó | Restaurant: raiz = *Patrons* | ☐ |
| A5 | **Construção recursiva** da árvore (ID3), com os critérios de paragem (profundidade máxima, mínimo de exemplos) | Restaurant: árvore igual à dos slides | ☐ |
| A6 | Prever um exemplo novo (percorrer a árvore) e imprimir a árvore como regras | Restaurant | ☐ |
| A7 | Métricas à mão: matriz de confusão, accuracy, precision, recall, F1 (FAI34) | Matriz pequena com as contas feitas à mão | ☐ |
| A8 | 10-fold CV estratificada à mão (FAI33 p.33-34) | Confirmar que cada fold mantém a proporção das classes | ☐ |
| A9 | Afinação dos hiperparâmetros (Q3) e decisão do Q13 | Tabela de experiências (O3) | ☐ |

### N: Montagem do NB1

| Bloco | Objetivo | Estado |
|---|---|---|
| N1 | Esqueleto do notebook: capa (R7, R9), configuração com os parâmetros no topo (O3), secções CRISP-DM 1-6 | ☐ |
| N2 | Preencher as fases 1-3 com P1-P6 e a EDA (texto da secção 3A do `project_status.md`) | ☐ |
| N3 | Fases 4-5: treinar no dataset real, avaliar, comparar treino vs. teste (FAI34 p.19-21) | ☐ |
| N4 | Fase 6: conclusões e tabela das experiências | ☐ |

### K: NB2, K-Means

| Bloco | Objetivo | Estado |
|---|---|---|
| K1 | Decidir o dataset e os atributos (Q14) e o objetivo de negócio do clustering (R21) | ☐ |
| K2 | Outliers e normalização feita à mão (Q6) | ☐ |
| K3 | K-Means à mão (FAI32 p.28-32): *seeds*, atribuição, recálculo dos centros, paragem | ☐ |
| K4 | SSE e método do cotovelo para escolher k (Q5) | ☐ |
| K5 | Caracterizar cada cluster (R25) | ☐ |
| K6 | Notebook NB2 com as fases CRISP-DM 1-6 | ☐ |

### F: Final

- [ ] Correr os dois notebooks do início ao fim (`nbconvert --execute`)
- [ ] Referências e rastreabilidade (requisito → célula)
- [ ] ZIP para o Moodle (R5) e preparação da defesa (R27)

---

## 4. Tarefas administrativas

- [ ] **Renomear o repositório** no GitHub de `FAI26_G07_tp2` para **`FAI26_P02_G07`** (guia s.3) e atualizar o remote:
      `git remote set-url origin https://github.com/gcoutinho-ipca/FAI26_P02_G07.git`
- [ ] Confirmar que o repositório é **privado**; adicionar o **Rúbem** e o **docente** como colaboradores
- [ ] Confirmar no Moodle os **critérios de avaliação, os pesos e o prazo**
- [x] `.venv/` no `.gitignore`
