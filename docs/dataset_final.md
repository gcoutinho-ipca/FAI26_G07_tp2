# Dataset final: `data/processed/dataset_final.csv`

Gerado por `src/preparar_dataset.py` a partir de duas fontes:

| Fonte | Ficheiro | Origem |
|---|---|---|
| Anúncios de imóveis | `data/archive/portugal_listinigs.csv` (190 867 linhas, 23 colunas) | Kaggle; nome e URL do dataset `[VERIFICAR]` (necessário para o R10) |
| Indicadores por concelho | `data/pordata/*.xlsx` | PORDATA, extraído a 04-11-2026; entidades indicadas por indicador |

O ficheiro não está no git (`data/processed/` está excluído). Reproduz-se correndo o script na raiz do projeto:

```
.venv/Scripts/python.exe src/preparar_dataset.py
```

## Passos e linhas

| Passo | Linhas | Decisão |
|---|---|---|
| Dataset original | 190 867 | n.a. |
| Só `Type` = Apartment ou House, com `Price` | 122 271 | D21 |
| Sem duplicados exatos | 115 391 | D20 |
| Regras: preço, área útil, casas de banho de 1 a 10, certificado com classe, moradias T0 (ruínas), anos 1937 e 1951 | 80 581 | D20, D22, D23 |
| Sem nulos em `Elevator` e `Tipologia` | 80 581 | D09, D20 |
| Sem repetidos entre portais (fica uma linha por andar quando os andares diferem) | 72 272 | D20 |
| Com avaliação bancária do concelho | **72 270** | D12, D20 |

Resultado: **45 498 apartamentos e 26 772 moradias**.

## Metadados (FAI33 p.12)

Papéis:
- **input:** feature;
- **target:** alvo;
- **id:** identificação ou chave, não entra no modelo;
- **ignore:** fica no ficheiro só para conferir o alvo e **nunca** pode ser feature (falso preditor, FAI33 p.26).

| Coluna | Tipo | Papel | Descrição | Origem |
|---|---|---|---|---|
| `District` | nominal | id | Distrito do anúncio | Anúncios |
| `City` | nominal | id | Concelho do anúncio; chave da junção com o PORDATA e do cluster do NB2 (D17) | Anúncios |
| `Type` | binário | input | Apartment ou House | Anúncios |
| `Tipologia` | ordinal (inteiro) | input | Número de quartos: `NumberOfBedrooms`, ou `TotalRooms` quando aquele falta (D19). Mínimo 0 nos apartamentos (estúdio) e 1 nas moradias (D22) | Anúncios, derivada |
| `LivingArea` | numérico (m²) | input | Área útil, entre 20 e 1 000 m² | Anúncios |
| `NumberOfBathrooms` | numérico (inteiro) | input | Casas de banho, entre 1 e 10 | Anúncios |
| `Parking` | numérico (inteiro) | input | Lugares de estacionamento (0 a 3) | Anúncios |
| `ConstructionYear` | numérico (ano) | input | Ano de construção; **vazio em 10,1%** (13,5% nos apartamentos, 4,4% nas moradias), tratado como categoria «Desconhecido» no NB1 (D08); sem os anos por omissão 1937 e 1951 (D23) | Anúncios |
| `EnergyCertificate` | ordinal | input | Certificado energético, de A+ a G | Anúncios |
| `Elevator` | binário | input | Tem elevador (63% dos apartamentos; 1,4% das moradias) | Anúncios |
| `poder_compra` | numérico (índice, PT = 100) | input | Poder de compra per capita do concelho, 2023 | PORDATA / INE, Estudo sobre o Poder de Compra Concelhio |
| `alojamentos_km2` | numérico | input | Alojamentos familiares clássicos por km² no concelho, 2022 | PORDATA / INE e DGT |
| `individuos_alojamento` | numérico (rácio) | input | Pessoas por alojamento familiar clássico no concelho, 2022 (valores baixos indicam segunda habitação ou casas vazias) | PORDATA / INE |
| `Price` | numérico (€) | ignore | Preço pedido no anúncio | Anúncios |
| `aval_m2` | numérico (€/m²) | ignore | Valor mediano de avaliação bancária do **mesmo tipo** no concelho, 2025; substituto: o mesmo tipo na NUTS III, depois o total (D13, D21) | PORDATA / INE, Inquérito à Avaliação Bancária na Habitação |
| `aval_origem` | nominal | ignore | De onde veio o `aval_m2`: concelho (apartamentos 45 020, moradias 25 964), nuts3 (476 e 808), total (2 e 0) | Derivada |
| `racio` | numérico | ignore | (`Price` / `LivingArea`) / `aval_m2` | Derivada (D13) |
| `classe_id` | ordinal (0 a 4) | target | Código da classe | Derivada (D15) |
| `classe` | ordinal | target | barato, medio, medio-alto, caro, muito caro | Derivada (D15) |
| `alarme_forte` | binário | target auxiliar | `classe` = muito caro (D16) | Derivada |

## Alvo (D15, por tipo)

| Classe | Apartment | House | % em cada tipo |
|---|---|---|---|
| barato | até 1,111 | até 1,008 | 25 |
| medio | 1,111 a 1,418 | 1,008 a 1,402 | 25 |
| medio-alto | 1,418 a 1,820 | 1,402 a 1,917 | 25 |
| caro | 1,820 a 2,299 | 1,917 a 2,566 | 15 |
| muito caro | acima de 2,299 | acima de 2,566 | 10 |

Os limiares são os percentis 25, 50, 75 e 90 do rácio de cada tipo e são recalculados sempre que o script corre. Por construção, o `Type` sozinho não prevê o alvo (ganho de informação 0).

## Coerência das features entre os dois tipos

| Mediana | Apartment | House |
|---|---|---|
| Tipologia | T2 | T3 |
| Área útil | 93 m² | 174 m² |
| Casas de banho | 2 | 3 |
| Estacionamento | 0 | 1 |
| Ano de construção | 1998 | 1999 |
| Preço | 298 000 € | 377 000 € |
| Rácio | 1,42 | 1,40 |

Os efeitos têm o mesmo sentido nos dois tipos. A % de «muito caro» sobe com a construção recente (depois de 2018: 26% nos apartamentos, 16% nas moradias) e com os certificados A+ a B. Nas moradias o sinal é mais fraco porque falta o terreno (D22).

## Ganho de informação de cada feature face ao alvo

A entropia do alvo é 2,243 bits. Só para esta medida, os contínuos foram discretizados em 10 intervalos de frequência igual.

| Feature | Total | Apartment | House |
|---|---|---|---|
| `ConstructionYear` (nulo como categoria) | 0,138 | 0,209 | 0,059 |
| `EnergyCertificate` | 0,132 | 0,186 | 0,079 |
| `LivingArea` | 0,036 | 0,052 | 0,048 |
| `Tipologia` | 0,028 | 0,047 | 0,009 |
| `Parking` | 0,021 | 0,035 | 0,007 |
| `NumberOfBathrooms` | 0,020 | 0,024 | 0,038 |
| `Elevator` | 0,018 | 0,044 | 0,003 |
| `poder_compra` | 0,018 | 0,023 | 0,021 |
| `individuos_alojamento` | 0,014 | 0,018 | 0,019 |
| `alojamentos_km2` | 0,012 | 0,018 | 0,019 |
| `Type` | 0,000 | n.a. | n.a. |

## Limitações conhecidas

- **Avaliação bancária:** só cobre imóveis comprados com crédito. O rácio mede o **sobrepreço face à avaliação** e não prova especulação (D16).
- **Universo:** são «imóveis habitáveis com certificado energético». Saíram as ruínas e o NC, que nos apartamentos era sobretudo construção recente (D20, D22).
- **Moradias:** sem informação de terreno, o que explica parte do sinal mais fraco (D22).
- **Metainformação do PORDATA:** não explica o significado do `0` nem a área de referência do €/m² bancário `[VERIFICAR]`.
- **Linhas iguais nas colunas finais:** 221, de andares diferentes de um mesmo empreendimento. O andar não fica no ficheiro final.
- **Ano 1950:** com 897 moradias, também fica acima dos anos vizinhos, mas não foi removido (D23).
