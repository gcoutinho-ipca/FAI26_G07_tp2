# Inventário das fontes do Projeto 02 (FAI, G07)

Fontes lidas na íntegra (texto de todas as páginas e imagem das páginas com fórmulas, diagramas ou código):

| Abreviatura | Ficheiro | Páginas |
|---|---|---|
| **GUIA** | `docs/material/FAI92_Project02_Guide.txt` (export em texto dos slides do Google Slides) | 10 slides |
| **FAI31** | `docs/material/FAI31_LearningFromExamples.pdf` | 30 |
| **FAI32** | `docs/material/FAI32_MLAlgorithms.pdf` | 50 |
| **FAI33** | `docs/material/FAI33_DataPrep.pdf` | 36 |
| **FAI34** | `docs/material/FAI34_ModelPerformance.pdf` | 30 |

Notação de referência: `FAI32 p.28` = ficheiro FAI32, página/slide 28. `[CG]` = conhecimento geral, não está no material.

> **Nota sobre o material.** O material do docente é composto só por slides teóricos. **Não há notebooks nem código de aula**, exceto dois excertos de código em FAI33 p.8-9. Também não há nenhuma referência a scikit-learn ou a outra biblioteca de ML. Isto condiciona a regra «usar apenas bibliotecas do inventário»: ver a secção D (Q1).

---

## A) Requisitos do guia

### A.1 Requisitos

| ID | Requisito | Fonte |
|---|---|---|
| **R1** | Implementar abordagens e métodos distintos de ML para um problema concreto | GUIA s.2 |
| **R2** | Usar **um ou dois datasets públicos** para classificação, clustering e regras de associação (ver Q4) | GUIA s.2 |
| **R3** | Datasets relacionados com **«Housing»** e **«Home credit»** (sugestão: Kaggle) | GUIA s.7 |
| **R4** | Código e documentação **integrados num Jupyter Notebook**. ⚠️ Substituído por **O2**: dois notebooks | GUIA s.4 |
| **R5** | Submeter um **ZIP com todos os ficheiros** do projeto no Moodle, dentro do prazo | GUIA s.4 |
| **R6** | Plataforma: repositório GitHub **privado** chamado **`FAI26_P02_G07`**, com o outro membro do grupo e o docente como colaboradores (ou pasta Google Drive com o mesmo nome) | GUIA s.3 |
| **R7** | Introdução: identificar o grupo (**nome e número de cada aluno**) | GUIA s.6 |
| **R8** | Introdução: contexto e objetivo do projeto | GUIA s.6 |
| **R9** | Introdução: **contribuição individual** de cada aluno. Cada aluno fica com uma tarefa principal: (a) aprendizagem supervisionada com 2 métodos de classificação; (b) aprendizagem não supervisionada com k-means | GUIA s.6 |
| **R10** | Dataset(s): indicar a **fonte** | GUIA s.7 |
| **R11** | Dataset(s): apresentar uma **EDA** | GUIA s.7 |
| **R12** | Dataset(s): incluir os **metadados** | GUIA s.7 |
| **R13** | Supervisionado: definir os **objetivos de negócio** | GUIA s.8 |
| **R14** | Supervisionado: escolher **dois algoritmos** (exemplo do guia: árvores de decisão e random forests). ⚠️ Em conflito com **O2**, que só refere a árvore de decisão: ver Q13 | GUIA s.8 |
| **R15** | Para **cada** método (2 secções): explicar a **preparação dos dados** | GUIA s.8 |
| **R16** | Para cada método: **aplicar** o algoritmo e **avaliar** os modelos | GUIA s.8 |
| **R17** | Para cada método: **otimizar os hiperparâmetros** | GUIA s.8 |
| **R18** | Para cada método: documentar os resultados **intermédios e finais** | GUIA s.8 |
| **R19** | Supervisionado: **análise dos resultados** com base em **métricas de desempenho** | GUIA s.8 |
| **R20** | Não supervisionado: indicar a fonte, uma descrição breve e os metadados do dataset | GUIA s.9 |
| **R21** | Clustering: definir o **objetivo de negócio** | GUIA s.9 |
| **R22** | Clustering: explicar a **preparação dos dados** | GUIA s.9 |
| **R23** | Clustering: **aplicar e avaliar o K-Means** | GUIA s.9 |
| **R24** | Clustering: **otimizar os hiperparâmetros** | GUIA s.9 |
| **R25** | Clustering: **analisar as características de cada cluster** | GUIA s.9 |
| **R26** | Clustering: documentar os resultados intermédios e finais | GUIA s.9 |
| **R27** | O projeto é **apresentado e defendido** pelos alunos (fora do notebook) | GUIA s.2, s.4 |
| n.a. | A estrutura do notebook pode ser adaptada às características do projeto | GUIA s.6 |

### A.2 Critérios de avaliação e pesos

**O guia não indica critérios de avaliação, pesos nem prazo** (ver Q8).

---

## B) Técnicas, algoritmos, métricas e bibliotecas do material

### B.1 Processo de ML e conceitos gerais

| Conceito | Fonte |
|---|---|
| Etapas: definição do dataset → preparação dos dados → seleção do modelo → treino → avaliação → afinação de hiperparâmetros → previsão/classificação | FAI31 p.11 |
| Processo supervisionado: amostra → análise → treino de vários modelos com afinação de hiperparâmetros → avaliação → teste → generalização | FAI31 p.17 |
| Processo não supervisionado: modelos 1…N → interpretação → dados agrupados ou associados | FAI31 p.20 |
| Tabela de técnicas por tipo de variável (supervisionado: árvore de decisão, ANN, SVM, k-NN, regressão logística, Naive Bayes; não supervisionado: K-Means, PCA, análise de correspondências) | FAI31 p.15, p.29 |
| Classificação em 2 passos: construir o modelo (treino) → usá-lo (teste ou dados novos) | FAI32 p.4-7 |

### B.2 Algoritmos de classificação

| Algoritmo | O que o material diz | Fonte |
|---|---|---|
| **k-NN** | Classe dominante entre os k vizinhos; distância euclidiana `d = sqrt(Σ(t_i − q_i)²)`; lazy learning; maldição da dimensionalidade; robusto a ruído | FAI32 p.8-12 |
| **Árvores de decisão** (ID3, C4.5) | Indução recursiva a partir da raiz; escolha do atributo por **ganho de informação**, com entropia `E = −Σ p_i log2(p_i)`; **índice de Gini** como alternativa; critérios de paragem; conversão em regras | FAI32 p.14-20 |
| **Poda** (pré-poda / pós-poda) | Para controlar o overfitting nas árvores | FAI34 p.22 |
| **Ensembles: Bagging** | Amostras bootstrap, k classificadores e votação | FAI34 p.28 |
| **Random Forest** | Bagging de árvores com escolha aleatória de atributos, para reduzir a variância | FAI34 p.29 |
| **Boosting** | Pesos dos exemplos reajustados conforme o erro | FAI34 p.29 |
| **Stacking** | Combina modelos de classes diferentes | FAI34 p.29 |
| Regressão logística, Naive Bayes, SVM, ANN | **Só aparecem pelo nome** num diagrama ou tabela, sem explicação | FAI31 p.15, p.29 |

### B.3 Clustering

| Conceito | Fonte |
|---|---|
| Definição de cluster; classificação vs. clustering | FAI32 p.22-23 |
| Qualidade: alta semelhança dentro do cluster, baixa entre clusters; comparação entre métodos | FAI32 p.24 |
| Requisitos de um método (escalabilidade, ruído e outliers, dimensionalidade, interpretabilidade…) | FAI32 p.25 |
| Função de distância: euclidiana para atributos numéricos; 0/1 para nominais; **pesos por atributo** | FAI32 p.26 |
| Critério do particionamento: **minimizar a soma dos quadrados das distâncias** de cada ponto ao centro do seu cluster (SSE) | FAI32 p.27 |
| **Algoritmo K-Means**: k dado à partida, centros aleatórios (*seeds*), atribuição ao centro mais próximo, recálculo das médias, repetir até não haver reatribuições | FAI32 p.28-32 |
| Limitações: sensível a outliers, só atributos numéricos, é preciso escolher k, clusters convexos, mínimos locais | FAI32 p.33-34 |
| K-Medoids / PAM / CLARA / CLARANS (alternativa robusta a outliers) | FAI32 p.33-36 |

### B.4 Regras de associação (só se forem incluídas: Q4)

| Conceito | Fonte |
|---|---|
| Itemset, suporte, confiança, regra forte | FAI32 p.38-41 |
| Algoritmo Apriori: geração de candidatos e poda | FAI32 p.42-46 |
| FP-Growth | FAI32 p.48 |
| Métricas: **support, confidence, lift, leverage, conviction** | FAI32 p.49 |

### B.5 EDA e preparação dos dados

| Técnica | Fonte |
|---|---|
| Objetivo da EDA: estrutura, distribuições, outliers, valores em falta, relações | FAI33 p.4 |
| Univariada (estatísticas, **histogramas**, **box plots**), bivariada (com a variável alvo), multivariada (cross-tabulation, gráficos) | FAI33 p.5-6 |
| Fases: compreender os dados originais → transformá-los → compreender os dados transformados | FAI33 p.7-8 |
| Visão geral em pandas: `head(10)`, `info()`, `describe()`, valores únicos das colunas `object` | FAI33 p.9 |
| **Metadados**: tipo (binário, nominal, ordinal, numérico, data) e **papel** (input, target, id/auxiliar, ignore, weight), com descrição de cada atributo | FAI33 p.12 |
| Transformações: nulos, datas, discretização, erros e outliers, conversão de nominais | FAI33 p.13 |
| **Valores em falta**: ignorar os registos, tratá-los como categoria ou atribuir um valor por omissão (**média** ou **mediana**) | FAI33 p.14 |
| Datas em formato numérico contínuo: `DateNum = ano + (dia_do_ano − 0.5) / dias_do_ano` | FAI33 p.15 |
| Ordinais → números que mantêm a ordem | FAI33 p.16-17 |
| Nominais sem ordem → **one-hot encoding** (uma coluna binária por valor) | FAI33 p.17 |
| **Discretização**: largura igual ou frequência igual | FAI33 p.18-19 |
| **Seleção de atributos**: (1) eliminar os que variam pouco; (2) eliminar os quase constantes sem relação com a classe; (3) detetar **falsos preditores** | FAI33 p.21 |
| Métodos filter / wrapper / embedded; atributos derivados; feature engineering | FAI33 p.22-25 |
| Falsos preditores: atributos com ~100% de capacidade preditiva, na raiz da árvore | FAI33 p.26 |
| **Classes desequilibradas**: separar **30%** para validação final; equilibrar 50/50 os ~70% restantes (subamostragem da maioria); avaliação final nos dados originais | FAI33 p.27-30 |
| **Amostragem estratificada** | FAI33 p.30, p.33 |

### B.6 Divisão dos dados e validação

| Técnica | Fonte |
|---|---|
| Conjuntos de treino, teste e validação | FAI33 p.21 |
| **Hold-out**: 2/3 treino, 1/3 teste; repeated hold-out | FAI33 p.32 |
| **K-fold cross-validation** (estratificada), **k = 10** como escolha habitual; validação cruzada estratificada repetida (10×10) | FAI33 p.33-34 |
| Leave-one-out (só para conjuntos muito pequenos) | FAI33 p.35 |

### B.7 Métricas de avaliação

| Métrica | Fórmula / descrição | Fonte |
|---|---|---|
| **Matriz de confusão** (2 classes e N classes) | TP, FN, FP, TN; caso multiclasse com uma matriz por classe (um contra os restantes) | FAI34 p.9-10, p.16-17 |
| **Accuracy** | (TP+TN)/N; preferível com classes equilibradas | FAI34 p.10, p.12 |
| Erro relativo total / **error rate** | (FN+FP)/N | FAI34 p.10; FAI33 p.30 |
| Erro relativo por classe | FP/(TN+FP); FN/(TP+FN) | FAI34 p.10 |
| **Precision** | TP/(TP+FP) | FAI34 p.11 |
| **Recall** (sensibilidade) | TP/(TP+FN) | FAI34 p.11 |
| **F1-score** | 2·P·R/(P+R); preferível com classes desequilibradas | FAI34 p.12 |
| TPR, FPR, **curva ROC** | TPR = TP/(TP+FN); FPR = FP/(FP+TN) | FAI34 p.14 |
| **AUC** | Área sob a curva ROC | FAI34 p.15 |
| Consistência / completude | Conceitos qualitativos | FAI34 p.7-8 |
| MSE, MAE, RMSE, RMSRE, MAPE | Só para alvo contínuo (**não se aplica** à classificação) | FAI34 p.5-6 |
| Lift curve sobre o conjunto de validação não usado | Referida | FAI33 p.30 |

### B.8 Ajuste do modelo

| Conceito | Fonte |
|---|---|
| Overfitting/underfitting: comparar o desempenho no **treino** e no **teste** | FAI34 p.19-21 |
| Bias/variância (árvores e k-NN têm variância alta) | FAI34 p.23-25 |
| Técnicas contra o overfitting: reduzir a complexidade, mais regularização, mais dados | FAI34 p.26 |
| Curva do erro de treino e de teste em função da complexidade do modelo | FAI34 p.27 |
| Afinação de hiperparâmetros (só nos diagramas do processo, **sem método concreto**) | FAI31 p.11, p.17 |

### B.9 Bibliotecas e funções

| Biblioteca / função | Fonte |
|---|---|
| `numpy as np`, `pandas as pd` | FAI33 p.8 |
| `matplotlib.pyplot as plt`, `seaborn as sns` | FAI33 p.8 |
| `from collections import Counter` | FAI33 p.8 |
| `import warnings; warnings.filterwarnings("ignore")` | FAI33 p.8 |
| `df.head(10)`, `df.info()`, `df.describe()`, `df[col].unique()` | FAI33 p.9 |
| **scikit-learn, mlxtend, scipy** | **Não aparecem no material** (ver Q1) |

---

## C) Notação, terminologia e estilo de código do docente

| Aspeto | O que existe no material | Fonte |
|---|---|---|
| Aliases dos imports | `np`, `pd`, `plt`, `sns` | FAI33 p.8 |
| Imports agrupados com um comentário por grupo | `# linear algebra and data processing libraries`, `# Graphics Visualization`, `# Utils` | FAI33 p.8 |
| Avisos desligados | `warnings.filterwarnings("ignore")` | FAI33 p.8 |
| Nome do DataFrame | `train_df` | FAI33 p.9 |
| Comentário antes de cada bloco, a dizer o objetivo | `# Print top examples`, `# Display basic information about the DataFrame`… | FAI33 p.9 |
| Saída com `print(...)` e f-strings | `print(f"\nUnique values for {column}:")` | FAI33 p.9 |
| Terminologia | *training/test/validation data set*, *hold-out*, *k-fold cross validation*, *stratified sample*, *false predictors*, *hyperparameters tuning*, *seeds* (centros iniciais do k-means), *TP/FN/FP/TN*, *Precision (P)*, *Sensitivity (Recall) (R)*, *F1 Score*, *ROC*, *AUC* | vários |
| Notação | `k` (vizinhos e clusters), `C+`/`C−` (classes), `p_i` (proporções), `t_i`/`q_i` (atributos na distância), `h(x_i)` (previsão) | FAI32 p.11, p.16; FAI34 p.5-17 |
| Exemplo de referência | Titanic EDA (Kaggle) | FAI33 p.9 |
| **Seeds fixas, proporções de split em código, estrutura de células** | **Não existem no material**. Só há as proporções teóricas (2/3 para treino e 1/3 para teste; 30% de validação; k=10) | n.a. |

---

## D) Lacunas e decisões que precisam da tua validação

| # | Questão | Proposta mais próxima do material |
|---|---|---|
| **Q1** | O material não tem nenhuma biblioteca de ML. Sem uma, não é possível treinar DT, RF ou K-Means de forma razoável | Usar **scikit-learn** `[CG]`, limitado às classes que implementam exatamente os conceitos do inventário (`train_test_split` com `stratify`, `StratifiedKFold`/`cross_val_score` com k=10, `DecisionTreeClassifier`, `RandomForestClassifier`, `KNeighborsClassifier`, `KMeans`, métricas `confusion_matrix`, `accuracy/precision/recall/f1`, `roc_curve`, `roc_auc_score`) |
| **Q2** | Que 2 algoritmos de classificação? | **Árvore de decisão + Random Forest**: são o exemplo do guia (s.8) e estão explicados em FAI32 p.14-20 e FAI34 p.28-29. Alternativa: k-NN + árvore de decisão (ambos em FAI32) |
| **Q3** | Como otimizar os hiperparâmetros? O material não indica nenhum método concreto | Ciclo explícito sobre os valores candidatos (ex.: `max_depth`, `min_samples_leaf`, `criterion` entropy/gini, `n_estimators`), com avaliação por **10-fold CV estratificada** (FAI33 p.33-34) e a curva treino vs. teste (FAI34 p.27). `GridSearchCV` faz o mesmo de forma automática `[CG]`: preferes o ciclo explícito ou o `GridSearchCV`? |
| **Q4** | O guia (s.2) refere **regras de associação**, mas as secções do notebook (s.6, s.8, s.9) só pedem classificação e k-means | Proposta: **não incluir** regras de associação, porque não fazem parte das tarefas por aluno. Se incluíres, o Apriori precisa do `mlxtend` `[CG]` ou de uma implementação própria |
| **Q5** | K-Means: como escolher k e avaliar? O material só dá o critério SSE (FAI32 p.27) | **Método do cotovelo sobre o SSE** (`inertia_`), que deriva diretamente de FAI32 p.27. O coeficiente de silhueta seria `[CG]`. Incluímos a silhueta (assinalada) ou ficamos só pelo SSE? |
| **Q6** | Escala dos dados: o k-NN e o K-Means dependem da distância euclidiana (FAI32 p.11, p.26), mas o material não fala em normalização | Normalizar as variáveis antes do K-Means, justificando com FAI32 p.26 («a importância de cada atributo é diferente») `[CG]` |
| **Q7** | Datasets: «Housing» e «Home credit» (Kaggle). Qual usar e para quê? | Ex.: *Home Credit Default Risk* (Kaggle, alvo `TARGET` desequilibrado, ~8% positivos) para a classificação, e um dataset de habitação (ex.: *Housing Prices*) para o K-Means. Fico à espera da tua escolha, ou procuro e proponho 2-3 opções concretas |
| **Q8** | O guia não tem critérios de avaliação, pesos nem prazo | Confirmar no Moodle |
| **Q9** | **Nome do repositório**: o guia exige `FAI26_P02_G07` e privado; o atual é `FAI26_G07_tp2` | Renomear no GitHub (*Settings → Rename*), confirmar que é privado e adicionar o Rúbem e o docente |
| **Q10** | **Autoria**: as tuas instruções dizem «autor (Gilberto)», mas o guia exige nome e número de todos os alunos e a contribuição individual (s.6) | Capa com os dois alunos (Gilberto Coutinho 3083, Rúbem Mendes 4563, como no TP1) e a divisão das tarefas: quem faz o supervisionado e quem faz o K-Means? |
| **Q11** | Versões das bibliotecas: o docente não indica nenhuma | Usar as versões fixadas no TP1 (`pandas 3.0.6`, `numpy 2.5.4`, `matplotlib 3.11.2`) e acrescentar `seaborn` e `scikit-learn`, listando-as numa célula inicial |
| **Q12** | Classes desequilibradas (provável no Home Credit) | Seguir FAI33 p.28-30: separar 30% para validação final, equilibrar os restantes 70% por subamostragem e avaliar no conjunto original; métrica principal **F1** (FAI34 p.12) |

---

## E) Orientações verbais do docente: MANDATÓRIAS

Fonte: indicação oral do docente, transmitida pelo Gilberto a 04/11/2026 (abreviatura **ORAL**).
**Regra:** se uma destas orientações entrar em conflito com o guia escrito, prevalece a orientação oral. O próprio guia permite adaptar a estrutura do notebook (GUIA s.6). Os conflitos ficam assinalados com ⚠️.

| ID | Orientação | Consequência no trabalho |
|---|---|---|
| **O1** | O trabalho deve ser **simples** | Sem extras fora do inventário: nada de ensembles adicionais, pipelines complexos ou regras de associação (fecha o Q4: **não incluir**) |
| **O2** | **Dois notebooks**: **NB1** com preparação dos dados, EDA e **árvore de decisão**; **NB2** com o **K-Means** | Substitui o R4 («um notebook»). Cada notebook tem de correr sozinho, do início ao fim |
| **O3** | Os notebooks devem permitir **«jogar» com as variáveis** e analisar os vários resultados | Os parâmetros ficam no topo, numa célula de configuração (atributos escolhidos, `max_depth`, `k`…). Cada experiência fica registada numa tabela de resultados e é comentada |
| **O4** | Seguir o **diagrama do processo CRISP-DM** | Cada notebook está organizado pelas fases do CRISP-DM (ver E.1) |
| **O5** | **Sem bibliotecas de ML**: os modelos são implementados «à mão», com código comentado para se perceber a lógica | Árvore de decisão (ID3, FAI32 p.15-16) e K-Means (FAI32 p.28-32) escritos de raiz, tal como a divisão treino/teste, a validação cruzada e as métricas. Só se usam as bibliotecas do docente (FAI33 p.8): `numpy`, `pandas`, `matplotlib`, `seaborn`. **Fecha o Q1: sem scikit-learn.** Heurística e parâmetros configuráveis (`criterio` entropia/Gini, profundidade máxima, mínimo de exemplos por nó, nº de intervalos da discretização, `k`, iterações, *seeds*). Todo o código comentado linha a linha. O código é testado primeiro no exemplo «Restaurant» do docente (FAI32 p.17-18: a raiz esperada é *Patrons*) |

### E.1 CRISP-DM: fases e onde ficam no trabalho

O CRISP-DM (*Cross-Industry Standard Process for Data Mining*) é o modelo de processo de *data mining*, nome que se dava antes ao que hoje se chama ML aplicado / ciência de dados. É um **ciclo iterativo**: em qualquer fase pode-se voltar atrás, por exemplo da modelação para a preparação dos dados. Está descrito em Provost & Fawcett (2013), cap. 2, livro da bibliografia do docente (FAI32 p.2), e em Chapman et al. (2000), *CRISP-DM 1.0* `[CG]`. Equivale ao processo de ML do docente em FAI31 p.11 e p.17.

| Fase CRISP-DM | O que se faz | Requisitos | Material do docente | NB1 (árvore) | NB2 (K-Means) |
|---|---|---|---|---|---|
| 1. **Business Understanding** | Objetivo de negócio e critério de sucesso | R8, R13, R21 | FAI31 p.11 | ✔ | ✔ |
| 2. **Data Understanding** | Fonte, metadados, EDA | R10-R12, R20 | FAI33 p.4-12 | ✔ (EDA completa) | ✔ (resumida) |
| 3. **Data Preparation** | Valores em falta, encoding, seleção de atributos, divisão dos dados, desequilíbrio | R15, R22 | FAI33 p.13-35 | ✔ | ✔ (normalização) |
| 4. **Modeling** | Aplicar o algoritmo e afinar os hiperparâmetros | R16, R17, R23, R24 | FAI32 p.14-20 / p.27-34 | ✔ | ✔ |
| 5. **Evaluation** | Métricas e verificação do objetivo de negócio | R16, R18, R19, R25, R26 | FAI34 | ✔ | ✔ |
| 6. **Deployment** | Conclusões e uso dos resultados | R27 | n.a. | Conclusão | Conclusão |

### E.2 Estrutura de cada notebook

1. Capa: grupo e contribuição individual (R7, R9)
2. Configuração: imports (FAI33 p.8), versões e os **parâmetros para «jogar»** (O3)
3. Fases CRISP-DM 1 a 6, cada uma numa secção com o mesmo nome
4. Tabela das experiências realizadas e discussão (O3)
5. Referências (ficheiro + página)

### E.3 Conflitos e decisões que daqui resultam

| # | Questão |
|---|---|
| **Q13** | O guia pede **2 algoritmos** de classificação (R14); a orientação oral só refere a **árvore de decisão**. Fazemos só a árvore? Ou a árvore mais um segundo algoritmo (ex.: Random Forest) no NB1? Confirmar com o docente |
| **Q15** | Com o O5, o dataset tem de ser **pequeno o suficiente** para uma árvore em Python puro: até alguns milhares de linhas e cerca de 10 atributos. O Home Credit completo (~307 mil linhas × ~120 colunas) só serve com uma amostra e uma seleção de atributos. E o ID3 exige atributos discretos (FAI32 p.15), por isso os contínuos têm de ser discretizados (FAI33 p.18-19) |
| **Q14** | Os dois notebooks usam o **mesmo dataset**? Se sim, o NB2 lê os dados já preparados pelo NB1, ou repete a preparação? |
