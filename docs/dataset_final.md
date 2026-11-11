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
| Só `Type = Apartment` com `Price` | 70 423 | D18 |
| Sem duplicados exatos | 66 298 | D20 |
| Regras de plausibilidade: preço, área útil, casas de banho de 1 a 10, certificado energético com classe | 52 666 | D20 |
| Sem nulos em `Elevator` e `Tipologia` | 52 666 | D09, D20 |
| Sem repetidos entre portais (fica uma linha por andar quando os andares diferem) | 46 450 | D20 |
| Com avaliação bancária do concelho | **46 450** | D12, D20 |

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
| `Tipologia` | ordinal (inteiro) | input | Número de quartos (T0, T1, ...): `NumberOfBedrooms`, ou `TotalRooms` quando aquele falta (D19) | Anúncios, derivada |
| `LivingArea` | numérico (m²) | input | Área útil, entre 20 e 1 000 m² | Anúncios |
| `NumberOfBathrooms` | numérico (inteiro) | input | Casas de banho, entre 1 e 10 | Anúncios |
| `Parking` | numérico (inteiro) | input | Lugares de estacionamento (0 a 3) | Anúncios |
| `ConstructionYear` | numérico (ano) | input | Ano de construção; **vazio em 13,3%**, tratado como categoria «Desconhecido» na discretização do NB1 (D08) | Anúncios |
| `EnergyCertificate` | ordinal | input | Certificado energético, de A+ a G | Anúncios |
| `Elevator` | binário | input | Tem elevador | Anúncios |
| `poder_compra` | numérico (índice, PT = 100) | input | Poder de compra per capita do concelho, 2023 | PORDATA / INE, Estudo sobre o Poder de Compra Concelhio |
| `alojamentos_km2` | numérico | input | Alojamentos familiares clássicos por km² no concelho, 2022 | PORDATA / INE e DGT |
| `individuos_alojamento` | numérico (rácio) | input | Pessoas por alojamento familiar clássico no concelho, 2022 (valores baixos indicam segunda habitação ou casas vazias) | PORDATA / INE |
| `Price` | numérico (€) | ignore | Preço pedido no anúncio | Anúncios |
| `aval_m2` | numérico (€/m²) | ignore | Valor mediano de avaliação bancária dos apartamentos no concelho, 2025; substituto: NUTS III, depois o total (D13) | PORDATA / INE, Inquérito à Avaliação Bancária na Habitação |
| `aval_origem` | nominal | ignore | De onde veio o `aval_m2`: concelho (45 967), nuts3 (481), total (2) | Derivada |
| `racio` | numérico | ignore | (`Price` / `LivingArea`) / `aval_m2` | Derivada (D13) |
| `classe_id` | ordinal (0 a 4) | target | Código da classe | Derivada (D15) |
| `classe` | ordinal | target | barato, medio, medio-alto, caro, muito caro | Derivada (D15) |
| `alarme_forte` | binário | target auxiliar | `classe` = muito caro (D16) | Derivada |

## Alvo (D15)

| Classe | Rácio | % |
|---|---|---|
| barato | até 1,111 | 25 |
| medio | 1,111 a 1,417 | 25 |
| medio-alto | 1,417 a 1,818 | 25 |
| caro | 1,818 a 2,294 | 15 |
| muito caro | acima de 2,294 | 10 |

Os limiares são os percentis 25, 50, 75 e 90 do rácio e são recalculados sempre que o script corre.

## Ganho de informação de cada feature face ao alvo

A entropia do alvo é 2,243 bits. Só para esta medida, os contínuos foram discretizados em 10 intervalos de frequência igual.

| Feature | IG |
|---|---|
| `ConstructionYear` (com o nulo como categoria) | 0,206 |
| `EnergyCertificate` | 0,182 |
| `LivingArea` | 0,051 |
| `Tipologia` | 0,046 |
| `Elevator` | 0,043 |
| `Parking` | 0,035 |
| `NumberOfBathrooms` | 0,023 |
| `poder_compra` | 0,022 |
| `individuos_alojamento` | 0,018 |
| `alojamentos_km2` | 0,013 |

O nulo do `ConstructionYear` informa: tem 4% de baratos e 21% de muito caros.

## Limitações conhecidas

- **Avaliação bancária:** só cobre imóveis comprados com crédito. O rácio mede o **sobrepreço face à avaliação** e não prova especulação (D16).
- **Corte dos «NC»:** ao tirar os apartamentos sem certificado energético saiu sobretudo construção recente. O universo é «apartamentos com certificado» (D20).
- **Metainformação do PORDATA:** não explica o significado do `0` nem a área de referência do €/m² bancário `[VERIFICAR]`.
- **Linhas iguais nas colunas finais:** 214. São frações de andares diferentes de um mesmo empreendimento, porque o andar não fica no ficheiro final.
- **Picos no `ConstructionYear`:** 1951 e 1937 podem ser um valor por omissão do portal (Q17, em aberto).
