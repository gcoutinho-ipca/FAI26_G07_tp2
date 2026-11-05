# Pendentes — Projeto 02 (FAI, G07)

Ponto de situação a 04/11/2026. O detalhe e as fontes de cada ponto estão em [`inventario.md`](inventario.md): secção D (Q1–Q12) e secção E (orientações orais O1–O4, Q13–Q14).

## Guidelines mandatórias (orientação oral do docente, 04/11/2026)

> Prevalecem sobre o guia escrito. Detalhe em `inventario.md`, secção E.

- **O1:** trabalho **simples**
- **O2:** **dois notebooks**: NB1 = preparação + EDA + árvore de decisão · NB2 = K-Means
- **O3:** poder **«jogar» com as variáveis**: parâmetros no topo e registo das experiências
- **O5:** **sem bibliotecas de ML**: árvore de decisão (ID3) e K-Means implementados à mão, com tudo comentado e a heurística parametrizável. Só numpy, pandas, matplotlib e seaborn
- **O4:** cada notebook segue as fases do **CRISP-DM** (Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment)

Método de trabalho: **bloco a bloco**, perceber cada passo antes de avançar.

## Estado

- [x] Guia e slides do docente em `docs/material/`
- [x] Inventário das fontes: `docs/inventario.md`
- [x] Orientações orais do docente registadas (secção E do inventário)
- [x] Bloco 1: ambiente `.venv` com numpy 2.5.4, pandas 3.1.1, matplotlib 3.11.2, seaborn 0.13.2, jupyter
- [ ] **Bloco 2: impureza (entropia/Gini) e ganho de informação, testados no exemplo «Restaurant»** ← em curso
- [ ] Bloco 3: construção recursiva da árvore (ID3)
- [ ] Escolher o dataset (Q7, Q14, Q15)
- [ ] NB1 (fases CRISP-DM 1–6) com a árvore de decisão
- [ ] NB2 (fases CRISP-DM 1–6) com o K-Means
- [ ] Execução completa dos dois notebooks (`nbconvert --execute`) e auto-verificação

## 1. Decisões a tomar (Gilberto + Rúbem)

| # | Decisão | Proposta | Decisão final |
|---|---|---|---|
| Q1 | Biblioteca de ML | Nenhuma: implementação própria (O5) | **Sem scikit-learn** ✔ |
| Q2 | Algoritmos de classificação | Árvore de decisão (O2). O segundo algoritmo depende do Q13 | Árvore de decisão ✔ |
| Q3 | Afinação dos hiperparâmetros | Ciclo explícito + 10-fold CV estratificada (FAI33 p.34). É mais legível para «jogar» (O3) | |
| Q4 | Incluir regras de associação? | Não | **Não** (O1, O2) ✔ |
| Q5 | Escolha de k no K-Means | Cotovelo sobre o SSE (FAI32 p.27) | |
| Q6 | Normalizar antes do K-Means | Sim (FAI32 p.26) | |
| Q7 | **Datasets**: «Housing» / «Home credit» | Opção A: Home Credit no NB1, California Housing no NB2 | |
| Q10 | **Divisão das tarefas** (uma tarefa principal por aluno) | NB1: ______ · NB2: ______ | |
| Q11 | Versões das bibliotecas | Fixar as do `.venv` num `requirements.txt` (sem scikit-learn) | |
| Q12 | Classes desequilibradas | FAI33 p.28–30: 30% para validação, 70% equilibrado 50/50, métrica principal F1 | |
| Q13 | **Só árvore de decisão, ou árvore + um 2.º algoritmo?** (guia R14 vs O2) | Confirmar com o docente | |
| Q15 | Dataset pequeno o suficiente para Python puro (amostra + seleção de atributos se for o Home Credit) | Ver inventário E.3 | |
| Q14 | Mesmo dataset nos dois notebooks? | Depende do Q7 | |

## 2. Tarefas administrativas

- [ ] **Renomear o repositório** no GitHub de `FAI26_G07_tp2` para **`FAI26_P02_G07`** (guia s.3) e atualizar o remote:
      `git remote set-url origin https://github.com/gcoutinho-ipca/FAI26_P02_G07.git`
- [ ] Confirmar que o repositório é **privado**; adicionar o **Rúbem** e o **docente** como colaboradores
- [ ] Confirmar no Moodle os **critérios de avaliação, os pesos e o prazo**
- [ ] Acrescentar `.venv/` e `data/` ao `.gitignore`

## 3. Trabalho por notebook (fases CRISP-DM)

**NB1: preparação, EDA e árvore de decisão** (responsável: ______)
- [ ] 1 Business Understanding: contexto e objetivos de negócio (R8, R13)
- [ ] 2 Data Understanding: fonte, metadados e EDA (R10–R12)
- [ ] 3 Data Preparation: valores em falta, encoding, seleção de atributos, divisão, desequilíbrio (R15)
- [ ] 4 Modeling: árvore de decisão e afinação dos hiperparâmetros (R16, R17)
- [ ] 5 Evaluation: matriz de confusão, métricas, treino vs. teste (R18, R19)
- [ ] 6 Deployment / Conclusão + tabela das experiências (O3)

**NB2: K-Means** (responsável: ______)
- [ ] 1 Business Understanding: objetivo de negócio do clustering (R21)
- [ ] 2 Data Understanding: fonte, descrição e metadados (R20)
- [ ] 3 Data Preparation: seleção de atributos numéricos e normalização (R22)
- [ ] 4 Modeling: K-Means e escolha de k pelo cotovelo/SSE (R23, R24)
- [ ] 5 Evaluation: características de cada cluster (R25, R26)
- [ ] 6 Deployment / Conclusão + tabela das experiências (O3)

**Final**
- [ ] Referências e rastreabilidade (requisito → célula) nos dois notebooks
- [ ] ZIP para o Moodle (R5) e preparação da defesa (R27)
