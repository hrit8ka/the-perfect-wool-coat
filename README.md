# The Perfect Wool Coat

A small data project about one question:

> **Does a higher wool % really mean a warmer, longer lasting coat fabric?**

I look at pilling, abrasion, warmth (thermal resistance) and tear strength as **separate** outcomes, because a high
wool % doesn't automatically mean better results in all of them.

## The data (and its big limitation)

There is no ready made dataset that has fabric composition **and** real performance tests, so I collected the numbers
by hand from 4 papers. Every row has a source id, and all sources are listed in `data/raw/sources.md`.

| Paper | Fabric | What it measures | Rows |
|---|---|---|---|
| Elshakankery 2008 | woven polyester/wool | pilling (pills per sq inch) | 108 |
| Bhatia & Sinha 2021 | handloom wool/polyester | warmth (Clo) | 36 |
| Colak 2020 (MSc thesis) | knitted acrylic/wool | pilling, abrasion, warmth | 24 |
| Manich et al. | woven PES or PLA / 45 % wool | abrasion, tear strength | 4 |

Important:
- **Papers use different tests and units, so I never mix them.** Wool % is only compared inside one paper.
- No paper measures everything on the same fabrics, so I can't train one model. It is an exploratory analysis only.
- The project uses published literature data only. I left out other datasets on purpose (the T2P simulated fabric data and a pilling image dataset).
- Every value was typed in from the papers, so please double check before using them in anything important.

## What I found (short version)

- **Pilling:** in the woven polyester/wool fabrics, more wool went with fewer pills, but the **weave mattered more**
  (satin pilled a lot more than plain at every wool %).
- **Warmth:** in the handloom fabrics, more wool went with slightly higher thermal resistance (small differences).
- **Knits:** in the acrylic/wool knits, pilling got worse with wool, abrasion and warmth showed no clear trend, and how
  bulky the yarn was seemed to matter more than the wool %.
- **Other fibre:** at the same 45 % wool, polyester blends were much more abrasion and tear resistant than polylactide blends.
- So: wool % alone doesn't decide quality. Weave, yarn and the other fibre matter as much or more.

The full write up with tables and figures is in `notebooks/01_exploratory_analysis.ipynb`.

## Project structure

```
perfect-wool-coat/
├── data/
│   ├── raw/sources.md                      where every number came from
│   └── processed/wool_literature_data.csv  the collected data (172 rows)
├── notebooks/
│   └── 01_exploratory_analysis.ipynb       analysis, figures, conclusions
├── src/
│   ├── data_loader.py                      loads the csv, fixes number columns
│   ├── data_quality.py                     checks for typos and shows coverage
│   └── feature_engineering.py              wool bands, weave groups
├── outputs/
│   ├── figures/                            fig1 to fig4
│   └── summary_table.csv                   one line per paper
├── requirements.txt
└── README.md
```

## How to run

```
pip install -r requirements.txt
cd src
python data_quality.py          # quick check of the data
cd ../notebooks
jupyter notebook                # open 01_exploratory_analysis.ipynb and run all cells
```

## Data dictionary (columns of the csv)

| column | meaning |
|---|---|
| source_doi | id of the paper (most have no DOI, see sources.md) |
| wool_pct | wool % (for the Bhatia paper this is the weft yarn only) |
| other_fiber | the other fibre in the blend |
| gsm | fabric weight, g/m2 (only if the paper gave it) |
| structure | weave or knit type |
| pilling_grade | grade 1-5, 5 = best |
| pilling_count | pills per sq inch, lower = better |
| abrasion_result | Martindale mass loss (% in Colak, mg in Manich), lower = better |
| thermal_resistance | Clo (Bhatia) or 1e-3 K m2/W (Colak), higher = warmer |
| tear_strength | tear force in N (Elmendorf) |
| condition | heat set or treatment stage, so treatments are not mixed |
| units_notes | everything else the paper reported, plus caveats |

## Ideas for next steps
- Find more papers that vary the wool % in woven fabrics with abrasion and tear data
  (two Textile Research Journal papers are listed as paywalled in `sources.md`).
- Use the pilling image dataset in a separate small computer vision project.
