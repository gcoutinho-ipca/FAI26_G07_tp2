"""
Preparação do dataset final do Projeto 02 (FAI, G07).

Junta os anúncios de imóveis (Kaggle, portugal_listinigs.csv) com os
indicadores do PORDATA por concelho, limpa os dados e calcula o alvo.
O resultado é data/processed/dataset_final.csv, que o NB1 (árvore de
decisão) e o NB2 (K-Means) leem.

Cada passo aplica uma decisão registada em docs/decisoes.md (Dnn).
Os limites e parâmetros estão todos na secção CONFIGURAÇÃO, para se
poder «jogar» com eles (orientação oral O3).

Execução (na raiz do projeto):
    .venv/Scripts/python.exe src/preparar_dataset.py
"""

# linear algebra and data processing libraries
import numpy as np
import pandas as pd

# Utils
import sys
import unicodedata
from pathlib import Path

# A consola do Windows não escreve acentos por omissão; forçamos UTF-8
sys.stdout.reconfigure(encoding="utf-8")


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

RAIZ = Path(__file__).resolve().parent.parent
FICHEIRO_ANUNCIOS = RAIZ / "data" / "archive" / "portugal_listinigs.csv"
PASTA_PORDATA = RAIZ / "data" / "pordata"
FICHEIRO_SAIDA = RAIZ / "data" / "processed" / "dataset_final.csv"

# D18: só apartamentos. ATENÇÃO: o resto do script assume este universo
# (avaliação bancária dos apartamentos e um só conjunto de limiares no
# alvo). Acrescentar «House» aqui exigia rever os passos 4 e 5.
TIPOS_A_MANTER = ["Apartment"]

# D20: regras de plausibilidade. Um valor fora destes limites é tratado
# como erro de introdução no portal e a linha sai.
PRECO_MIN, PRECO_MAX = 10_000, 10_000_000          # euros
AREA_UTIL_MIN, AREA_UTIL_MAX = 20, 1_000           # m² (LivingArea)
WC_MIN, WC_MAX = 1, 10                             # casas de banho (0 é um nulo disfarçado)

# D20: rótulos do certificado energético que não dizem a classe energética
# do imóvel. As linhas com estes rótulos saem.
CERTIFICADOS_SEM_CLASSE = ["NC", "No Certificate", "Not available"]

# D20: o mesmo apartamento aparece repetido quando foi anunciado nos dois
# portais ou republicado. Se True, fica só um anúncio por grupo de linhas
# iguais nas colunas de CHAVE_REPETIDOS.
REMOVER_REPETIDOS_ENTRE_PORTAIS = True
CHAVE_REPETIDOS = ["District", "City", "Town", "Price", "LivingArea", "Tipologia",
                    "NumberOfBathrooms", "Parking", "ConstructionYear",
                    "EnergyCertificate", "Elevator"]

# D15: percentis do rácio que separam as 5 classes do alvo
PERCENTIS_CLASSES = [0.25, 0.50, 0.75, 0.90]
NOMES_CLASSES = ["barato", "medio", "medio-alto", "caro", "muito caro"]

# D12: indicadores do PORDATA que entram, com o ano mais recente de cada um.
# Formato: nome da coluna final -> (parte do nome do ficheiro, subcategoria, ano)
# A subcategoria é None quando o quadro só tem uma série.
INDICADORES_PORDATA = {
    "aval_m2_apartamento": ("avaliação-bancária", "Apartamentos", "2025"),
    "aval_m2_total":       ("avaliação-bancária", "Total", "2025"),
    "poder_compra":        ("Poder-de-compra", None, "2023"),
    "alojamentos_km2":     ("alojamentos-familiares-clássicos-por-km2", None, "2022"),
    "individuos_alojamento": ("indivíduos-por-alojamento", None, "2022"),
}

# D12: nomes de concelho que no portal e no PORDATA se escrevem de forma
# diferente (já sem acentos e em minúsculas, ver normalizar_nome)
CORRESPONDENCIAS_CONCELHOS = {
    "lagoa (algarve)": "lagoa",
    "lagoa (sao miguel)": "lagoa [r.a.a.]",
    "praia da vitoria": "vila da praia da vitoria",
    "calheta de s. jorge": "calheta [r.a.a.]",
}


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def normalizar_nome(texto):
    """Tira acentos, espaços nas pontas e maiúsculas, para que
    'Setúbal' e 'setubal' sejam a mesma chave na junção."""
    sem_acentos = unicodedata.normalize("NFKD", str(texto))
    sem_acentos = sem_acentos.encode("ascii", "ignore").decode()
    return sem_acentos.lower().strip()


def ler_indicador_pordata(parte_nome, subcategoria, ano):
    """Lê um quadro do PORDATA e devolve duas séries indexadas pelo
    nome normalizado do município:
      - o valor do próprio município;
      - o valor da NUTS III a que pertence (substituto quando o município
        não tem dado).

    O quadro do PORDATA não é uma tabela simples: tem um cabeçalho em
    várias linhas e as linhas de dados misturam Portugal, NUTS I, II, III
    e municípios. Por isso localizamos as linhas pelo conteúdo e não por
    posição fixa."""
    ficheiro = next(f for f in PASTA_PORDATA.glob("*.xlsx") if parte_nome in f.name)
    quadro = pd.read_excel(ficheiro, sheet_name="Quadro", header=None)
    quadro = quadro.dropna(axis=1, how="all")        # o Excel traz 256 colunas, quase todas vazias

    # A linha dos anos começa por «Âmbito Geográfico»; a das subcategorias
    # (ex.: Total, Apartamentos, Moradias) fica imediatamente acima
    primeira_coluna = quadro.iloc[:, 0].astype(str).str.strip()
    linha_anos = primeira_coluna[primeira_coluna == "Âmbito Geográfico"].index[0]
    anos = quadro.loc[linha_anos].astype(str)
    subcats = quadro.loc[linha_anos - 1].ffill()     # a subcategoria só aparece na 1.ª coluna do grupo

    # Escolhemos a coluna do ano pedido (e da subcategoria, se houver)
    colunas = [c for c in quadro.columns[2:]
               if anos[c] == ano and (subcategoria is None or str(subcats[c]) == subcategoria)]
    coluna = colunas[0]

    nivel = primeira_coluna.values                   # «NUTS III», «Município», ...
    nomes = quadro.iloc[:, 1].map(normalizar_nome).values
    # O PORDATA usa 0 quando não há dado (ex.: concelhos com poucas
    # avaliações bancárias). Um preço por m² ou uma densidade de 0 não
    # existem, por isso o 0 passa a nulo.
    valores = pd.to_numeric(quadro[coluna], errors="coerce").replace(0, np.nan).values

    valor_municipio, valor_nuts3 = {}, {}
    nuts3_atual = np.nan
    for nv, nome, valor in zip(nivel, nomes, valores):
        if nv == "NUTS III":
            nuts3_atual = valor                      # os municípios seguintes pertencem a esta NUTS III
        elif nv == "Município":
            valor_municipio[nome] = valor
            valor_nuts3[nome] = nuts3_atual
    return pd.Series(valor_municipio), pd.Series(valor_nuts3)


def registar(passos, descricao, df):
    """Guarda o número de linhas depois de cada passo, para o resumo final."""
    passos.append((descricao, len(df)))
    # separador de milhares com espaço (norma portuguesa), só no número
    numero = f"{len(df):,}".replace(",", " ")
    print(f"{numero:>8} linhas | {descricao}")


# =============================================================================
# 1. LEITURA E UNIVERSO
# =============================================================================

passos = []
df = pd.read_csv(FICHEIRO_ANUNCIOS, low_memory=False)
registar(passos, "dataset original", df)

# D18: só apartamentos, e só os que têm preço (sem preço não há alvo)
df = df[df["Type"].isin(TIPOS_A_MANTER) & df["Price"].notna()]
registar(passos, "só apartamentos com preço (D18)", df)

# D20 (2): duplicados exatos. Comparamos todas as colunas originais, antes
# de escolher atributos, para só apagar anúncios repetidos de facto
df = df.drop_duplicates()
registar(passos, "sem duplicados exatos (D20)", df)


# =============================================================================
# 2. TIPOLOGIA (D19)
# =============================================================================
# O dataset junta dois portais. Num, a tipologia (T0, T1, ...) vem em
# NumberOfBedrooms; no outro, esse campo está vazio e a tipologia vem em
# TotalRooms. A EDA confirmou-o: a área mediana por valor é a mesma nos
# dois (T2: 84 vs 85 m²; T3: 115 vs 117 m²). Juntamos os dois campos.
df["Tipologia"] = df["NumberOfBedrooms"].fillna(df["TotalRooms"])


# =============================================================================
# 3. REGRAS DE PLAUSIBILIDADE (D20, 1)
# =============================================================================
# Cada regra marca as linhas com valores impossíveis. Usamos between(),
# que inclui os limites. Um nulo dá False em between(), por isso as linhas
# com nulo em NumberOfBathrooms também saem aqui (o que já era a D09).
valido = (
    df["Price"].between(PRECO_MIN, PRECO_MAX)
    & df["LivingArea"].between(AREA_UTIL_MIN, AREA_UTIL_MAX)
    & df["NumberOfBathrooms"].between(WC_MIN, WC_MAX)
    # um apartamento com 2 quartos e 0 casas de banho não existe: o 0 é o
    # valor que o portal grava quando o campo não foi preenchido
    & ~df["EnergyCertificate"].isin(CERTIFICADOS_SEM_CLASSE)
)
df = df[valido]
registar(passos, "regras de plausibilidade (D20)", df)

# D09 / D20 (3): nulos nos atributos que não podem ficar vazios
df = df.dropna(subset=["Elevator", "Tipologia"])
registar(passos, "sem nulos em Elevator e Tipologia (D09, D20)", df)

# D20 (2b): repetidos entre portais. Os duplicados exatos já saíram, mas o
# mesmo apartamento publicado nos dois portais difere só nos campos que um
# portal tem e o outro não (Garage, PublishDate, ...). Comparamos então só
# as colunas que descrevem o imóvel. Na EDA, 99,7% destes grupos tinham a
# mesma freguesia. Sem este passo, o mesmo imóvel podia cair no treino e no
# teste e inflacionar a accuracy. O drop_duplicates trata dois nulos como iguais.
#
# Exceção: num empreendimento novo, frações diferentes podem ter o mesmo
# preço e as mesmas características e só diferir no andar (Floor). Por isso
# o andar entra na comparação. Como um dos portais não publica o andar, uma
# linha sem andar num grupo que tem andares preenchidos é tratada como a
# cópia do outro portal e sai.
if REMOVER_REPETIDOS_ENTRE_PORTAIS:
    grupos = df.groupby(CHAVE_REPETIDOS, dropna=False)["Floor"]
    grupo_tem_andar = grupos.transform("count") > 0      # count ignora os nulos
    df = df[~(grupo_tem_andar & df["Floor"].isna())]
    df = df.drop_duplicates(subset=CHAVE_REPETIDOS + ["Floor"])
    registar(passos, "sem repetidos entre portais (D20)", df)


# =============================================================================
# 4. JUNÇÃO COM O PORDATA (D12)
# =============================================================================
# A chave é o concelho: City no portal, Município no PORDATA
df["chave_concelho"] = df["City"].map(normalizar_nome).replace(CORRESPONDENCIAS_CONCELHOS)

for coluna, (parte_nome, subcategoria, ano) in INDICADORES_PORDATA.items():
    municipio, nuts3 = ler_indicador_pordata(parte_nome, subcategoria, ano)
    # Valor do município; se não existir, o da NUTS III a que pertence
    df[coluna] = df["chave_concelho"].map(municipio).fillna(df["chave_concelho"].map(nuts3))
    # Para a avaliação dos apartamentos guardamos também de onde veio o
    # valor, para se poder ver quantos anúncios dependem de um substituto
    if coluna == "aval_m2_apartamento":
        tem_valor_concelho = df["chave_concelho"].map(municipio).notna()

# D13: a referência é a avaliação dos apartamentos do concelho; se faltar,
# a dos apartamentos da NUTS III (mesmo tipo de imóvel); só depois o total
# (ex.: Vila Nova de Cerveira não tem valor de apartamentos e fica com o do
# Alto Minho, 1 614 €/m², em vez do total do concelho, 1 285 €/m², que
# mistura moradias)
df["aval_m2"] = df["aval_m2_apartamento"].fillna(df["aval_m2_total"])
df["aval_origem"] = np.select(
    [tem_valor_concelho, df["aval_m2_apartamento"].notna(), df["aval_m2_total"].notna()],
    ["concelho", "nuts3", "total"],
    default="sem valor",
)
df = df.drop(columns=["aval_m2_apartamento", "aval_m2_total"])

# D20 (4): anúncios sem avaliação são os de fora de Portugal (Brasil, Dubai)
df = df.dropna(subset=["aval_m2"])
registar(passos, "com avaliação bancária do concelho (D12, D20)", df)


# =============================================================================
# 5. ALVO (D13, D15, D16)
# =============================================================================
# Rácio = preço por m² pedido no anúncio / valor mediano de avaliação
# bancária por m² no concelho. Um rácio de 1,5 quer dizer que o anúncio
# pede 50% acima do que os bancos avaliam naquele concelho.
df["racio"] = (df["Price"] / df["LivingArea"]) / df["aval_m2"]

# Os limiares são os percentis do rácio, calculados depois da limpeza
limiares = df["racio"].quantile(PERCENTIS_CLASSES).values
# np.digitize devolve 0 abaixo do 1.º limiar, 1 entre o 1.º e o 2.º, etc.
# right=True: um valor igual ao limiar fica na classe de baixo
df["classe_id"] = np.digitize(df["racio"], limiares, right=True)
df["classe"] = df["classe_id"].map(dict(enumerate(NOMES_CLASSES)))

# D16: o alarme forte é a classe «muito caro» (acima do P90). O alarme
# fraco depende da previsão do ID3 e é calculado no NB1.
df["alarme_forte"] = df["classe"] == "muito caro"


# =============================================================================
# 6. COLUNAS FINAIS E GRAVAÇÃO (D19)
# =============================================================================
colunas_finais = [
    # auxiliares (identificação e chave do cluster da D17; não são features)
    "District", "City",
    # features do anúncio
    "Tipologia", "LivingArea", "NumberOfBathrooms", "Parking",
    "ConstructionYear", "EnergyCertificate", "Elevator",
    # features do concelho (PORDATA)
    "poder_compra", "alojamentos_km2", "individuos_alojamento",
    # definem o alvo: nunca usar como features (falsos preditores, FAI33 p.26)
    "Price", "aval_m2", "aval_origem", "racio",
    # alvo
    "classe_id", "classe", "alarme_forte",
]
final = df[colunas_finais].reset_index(drop=True)

# Tipos coerentes: contagens como inteiros; ConstructionYear fica decimal
# porque tem nulos (D08: o nulo é a categoria «Desconhecido» no NB1)
for coluna in ["Tipologia", "NumberOfBathrooms", "Parking"]:
    final[coluna] = final[coluna].astype(int)
final["Elevator"] = final["Elevator"].astype(bool)

FICHEIRO_SAIDA.parent.mkdir(parents=True, exist_ok=True)
final.to_csv(FICHEIRO_SAIDA, index=False, encoding="utf-8")


# =============================================================================
# 7. RESUMO
# =============================================================================
print(f"\nGravado: {FICHEIRO_SAIDA.relative_to(RAIZ)}  ({final.shape[0]} linhas x {final.shape[1]} colunas)")

print("\nLimiares do rácio (D15):")
for p, v in zip(PERCENTIS_CLASSES, limiares):
    print(f"  P{int(p * 100):<3} {v:.3f}")

print("\nDistribuição do alvo:")
print((final["classe"].value_counts(normalize=True).reindex(NOMES_CLASSES) * 100).round(1).to_string())

print("\nOrigem da avaliação bancária (n.º de anúncios):")
print(final["aval_origem"].value_counts().to_string())

print("\nNulos por coluna (%):")
nulos = (final.isna().mean() * 100).round(2)
print(nulos[nulos > 0].to_string())
