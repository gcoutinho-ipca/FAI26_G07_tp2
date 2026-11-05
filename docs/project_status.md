# Status do Projeto - FAI, G07 (Projeto 02)

**Data de última atualização:** 05 de Novembro de 2026
Estado: Fase de Data Understanding concluída. Plano de limpeza (Notebook 1) definido.
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

## 3. Pipeline de Trabalho Proposto

O fluxo de trabalho será dividido em dois núcleos principais de execução para garantir a reprodutibilidade e o rigor metodológico.

### **Notebook 1: Data Treatment & Engineering (Limpeza e Preparação)**
Este notebook terá como objetivo transformar o dataset bruto num conjunto de dados pronto para modelação.
- **Fases CRISP-DM:** Data Understanding e Data Preparation.
- **Tarefas principais:**
    - Importação e limpeza de tipos de dados (correção de `object` e `mixed types`).
    - Tratamento de valores em falta (Imputação por média/mediana ou eliminação de colunas/linhas insuficientes).
    - Conversão de variáveis categóricas em numéricas (*One-Hot Encoding* ou *Label Encoding* manual).
    - **Feature Engineering:** Criação de variáveis e seleção de atributos relevantes (evitar *falsos preditores*).
    - **Normalização/Escalonamento:** Essencial para o K-Means.
    - **Divisão de Dados:** Separação em conjuntos de Treino, Validação (30%) e Teste (Hold-out) com estratificação.
    - **Exportação:** Gravação do dataset limpo e transformado para o Notebook 2.

### **Notebook 2: ML Analysis (Modelação e Avaliação)**
Este notebook executará os algoritmos implementados "à mão" sobre os dados preparados no Notebook 1.
- **Fases CRISP-DM:** Modeling e Evaluation.
- **Tarefas principais:**
    - **Tarefa Supervisionada (NB1):** Implementação de Árvore de Decisão (ID3) e avaliação via Matriz de Confusão, F1-Score, Precisão e Recall.
    - **Tarefa Não Supervisionada (NB2):** Implementação de K-Means, determinação de $k$ (Método do Cotovelo/SSE) e análise de clusters.
    - **Otimização:** Execução de ciclos de ajuste de hiperparâmetros (profundidade, critério de divisão) via validação cruzada manual.
    - **Documentação:** Tabela de experiências e discussão de resultados.

---

## 4. Regras de Ouro (Desenvolvimento)
1.  **Zero Scikit-Learn:** Apenas `numpy`, `pandas`, `matplotlib` e `seaborn` para o núcleo de ML.
2.  **Implementação Manual:** Algoritmos, métricas e validação cruzada devem ser escritos de raiz.
3.  **Parâmetros Configuráveis:** As variáveis de decisão (seeds, $k$, profundidade) devem estar no topo de cada notebook.
4.  **Rastreabilidade:** Todas as decisões de limpeza de dados devem ser justificadas com base na análise estatística (EDA).
