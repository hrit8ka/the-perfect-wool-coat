# data_loader.py
# loads the literature csv and makes the number columns actually numbers

import pandas as pd
from pathlib import Path

# project root = the folder above src/
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "wool_literature_data.csv"

NUMBER_COLS = [
    "wool_pct", "gsm", "pilling_grade", "pilling_count",
    "abrasion_result", "thermal_resistance", "tear_strength",
]

# short names for the papers so the plots are readable
# (the long version of each source is in data/raw/sources.md)
PAPER_NAMES = {
    "no-doi:fibre2fashion-3259": "Elshakankery 2008 (woven PES/wool)",
    "no-doi:ijftr-2021-bhatia-sinha": "Bhatia & Sinha 2021 (handloom wool/PES)",
    "no-doi:colak-2020-uludag": "Colak 2020 (acrylic/wool knit)",
    "no-doi:manich-ifatcc-pla-wool": "Manich (PLA or PET / wool woven)",
}


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)

    # blanks and text become NaN, which is what we want for missing values
    for col in NUMBER_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["paper"] = df["source_doi"].map(PAPER_NAMES)
    # if a paper is not in the dict yet, just use its id
    df["paper"] = df["paper"].fillna(df["source_doi"])

    return df


if __name__ == "__main__":
    d = load_data()
    print(d.shape)
    print(d["paper"].value_counts())
