# Status do Projeto - FAI, G07 (Projeto 02)

**Data de última atualização:** 05 de Novembro de 2026
Estado: Data Understanding inicial concluída. Revisão da preparação dos dados em curso.
**Dataset Utilizado:** `data/archive/portugal_listinigs.csv`

## 1. Objetivo do Projeto
Implementação manual (sem uso de `scikit-learn`) de algoritmos de **Aprendizagem Supervisionada (Árvore de Decisão/ID3)** e **Não Supervisionada (K-Means)**, seguindo o ciclo de vida **CRISP-DM**. O projeto foca na compreensão profunda dos algoritmos e no rigor no tratamento de dados.

---

## 2. Análise do Dataset (`portugal_listinigs.csv`)

### 2.1. Perfil Geral
- **Registos:** 190.867 linhas.
- **Variáveis:** 23 colunas (mistura de tipos numéricos, categóricos e strings).
- **Distribuição de Preço:** Alta assimetria (mediana ~240k vs média ~401k), indicando presença de *outliers* de alto valor.

### 2.2. Diagnóstico de Dados (Integridade)
Foram identificadas lacunas críticas que exigem tratamento na fase de **Data Preparation**:

| Variável | Nulos (Aprox.) | Impacto no Projeto |
| :--- | :--- | :--- |
| `ConservationStatus` | 157.884 | Alto (Dificulta agrupamento por estado) |
| `Floor` | 162.938 | Alto (Dado desbalanceado/incompleto) |
| `LotSize` | 124.626 | Médio (Requer imputação ou remoção) |
| `BuiltArea` | 114.889 | Médio (Requer imputação ou remoção) |
| `PublishDate` | 107.953 | Baixo (Pode ser ignorado se não for alvo) |
| `NumberOfBedrooms` | 103.337 | Médio (Crucial para modelos de habitação) |
| `NumberOfWC` | 112.464 | Médio (Crucial para modelos de habitação) |

---

## 3. Pipeline de Trabalho (alinhado com a orientação oral O2)

São dois notebooks e cada um corre sozinho, do início ao fim, seguindo as 6 fases do CRISP-DM (O4). Os detalhes estão em `inventario.md`, secção E.

### **NB1: Preparação, EDA e Árvore de Decisão (ID3)**
- **Fases CRISP-DM:** 1 a 6.
- **Data Preparation:** valores em falta, discretização dos atributos contínuos (o ID3 exige atributos discretos, FAI32 p.15), seleção de atributos (evitar *falsos preditores*), amostra e divisão estratificada (Q15, Q12).
- **Modeling:** ID3 implementado à mão, com critério entropia/Gini e profundidade configuráveis, testado primeiro no exemplo «Restaurant» (FAI32 p.17-18).
- **Evaluation:** matriz de confusão, accuracy, precision, recall, F1, treino vs. teste (FAI34).

### **NB2: K-Means**
- **Fases CRISP-DM:** 1 a 6 (Data Understanding resumida).
- **Data Preparation:** atributos numéricos, tratamento de outliers e normalização (FAI32 p.26).
- **Modeling:** K-Means implementado à mão; escolha de $k$ pelo cotovelo sobre o SSE (FAI32 p.27).
- **Evaluation:** características de cada cluster (R25).

Em ambos: parâmetros no topo e tabela de experiências (O3).

> **Nota:** `notebook_1_data_treatment.py` (rascunho inicial) fica como rascunho de referência e não é usado tal como está. Está a ser revisto por partes (ver `pendentes.md`).

---

## 3A. Tratamento de dados do NB1: o que já está decidido

> **Para o Rúbem:** esta secção resume os filtros e as transformações aprovados até agora, pela ordem em que são aplicados. A justificação completa de cada passo está em [`decisoes.md`](decisoes.md). Este texto passa para a fase *Data Preparation* do NB1 quando o notebook for criado.

| Passo | O quê | Linhas no fim | Decisão |
|---|---|---|---|
| 0 | Dataset original `portugal_listinigs.csv` | 190 867 | n.a. |
| 1 | Ficam só `Type` = Apartment ou House, com `Price` preenchido | 122 271 | D04 |
| 2 | Saem os distritos com menos de 100 anúncios (`MIN_ANUNCIOS_DISTRITO = 100`); são 9 distritos | 122 097 | D06 |
| 3 | Alvo `caro` = 1 se `Price` > mediana do distrito, senão 0 (os 665 anúncios com o preço igual à mediana ficam 0). Resultado: 50,4% barato / 49,6% caro. Depois disto, `Price` sai dos atributos | 122 097 | D03, D05 |
| 4 | Ficam só os **8 atributos** escolhidos e o alvo: `Type`, `TotalArea`, `LivingArea`, `NumberOfBathrooms`, `Parking`, `ConstructionYear`, `EnergyCertificate`, `Elevator` | 122 097 | D07 |
| 5 | Saem as linhas com nulo em `NumberOfBathrooms` ou em `Elevator` | 121 679 | D09 |
| ⏳ | **`ConstructionYear` (14,6% de nulos): para decidir com o Rúbem.** O nulo tem 71,8% caros, por isso não é aleatório. As opções e os dados estão na D08 | | D08 |
| ... | Por decidir: erros e outliers (ex.: `NumberOfBathrooms` com o máximo de 3 020 e 84 casos com mais de 10), discretização dos contínuos para o ID3, amostra e divisão treino/teste | | |

**Porque é que estes 8 e não outros (resumo da D07):** todos têm 15% de nulos ou menos e mostram relação com o alvo. As colunas com mais de 50% de nulos, as que têm centenas ou milhares de valores (`City`, `Town`), as redundantes e o próprio `Price` ficaram de fora. A lista completa dos excluídos, com o motivo de cada um, está na D07 de [`decisoes.md`](decisoes.md).

**Nota:** como o limiar é a mediana do próprio distrito, o alvo fica ~50/50 dentro de cada distrito. Por isso o `District`, sozinho, quase não prevê o alvo.

---

## 4. Regras de Ouro (Desenvolvimento)
1.  **Zero Scikit-Learn:** Apenas `numpy`, `pandas`, `matplotlib` e `seaborn` para o núcleo de ML.
2.  **Implementação Manual:** Algoritmos, métricas e validação cruzada devem ser escritos de raiz.
3.  **Parâmetros Configuráveis:** As variáveis de decisão (seeds, $k$, profundidade) devem estar no topo de cada notebook.
4.  **Rastreabilidade:** Todas as decisões de limpeza de dados devem ser justificadas com base na análise estatística (EDA).
5.  **Código comentado:** todo o código é comentado de forma a explicar a lógica de cada passo (O5).
6.  **Registo de decisões:** todas as decisões ficam em [`decisoes.md`](decisoes.md) antes de serem implementadas.
