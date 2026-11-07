# data_quality.py
# simple checks so we notice if a typo sneaks into the csv

import pandas as pd

OUTCOMES = ["pilling_grade", "pilling_count", "abrasion_result",
            "thermal_resistance", "tear_strength"]


def check_data(df):
    """returns a list of problems found (empty list = all good)"""
    problems = []

    # every row needs a source (project rule)
    if df["source_doi"].isna().any() or (df["source_doi"] == "").any():
        problems.append("some rows have no source_doi")

    # wool % has to be between 0 and 100
    bad = df[(df["wool_pct"] < 0) | (df["wool_pct"] > 100)]
    if len(bad) > 0:
        problems.append(f"{len(bad)} rows with wool_pct outside 0-100")

    # rows with no wool % can't be used for our main question
    if df["wool_pct"].isna().any():
        problems.append(f"{df['wool_pct'].isna().sum()} rows have no wool_pct")

    # pilling grade is on a 1-5 scale
    bad = df[(df["pilling_grade"] < 1) | (df["pilling_grade"] > 5)]
    if len(bad) > 0:
        problems.append(f"{len(bad)} rows with pilling_grade outside 1-5")

    # nothing measured can be negative
    for col in ["pilling_count", "abrasion_result", "thermal_resistance",
                "tear_strength", "gsm"]:
        if (df[col] < 0).any():
            problems.append(f"negative values in {col}")

    # a row with no outcome at all is useless
    no_outcome = df[OUTCOMES].isna().all(axis=1)
    if no_outcome.any():
        problems.append(f"{no_outcome.sum()} rows have no outcome measurement")

    # exact duplicate rows
    # (condition has to be in here, the 3 treatment stages of one fabric share the same notes)
    dups = df.duplicated(subset=["source_doi", "units_notes", "condition"]).sum()
    if dups > 0:
        problems.append(f"{dups} duplicate rows")

    return problems


def coverage_table(df):
    """how many measurements do we have for each paper and outcome?"""
    counts = df.groupby("paper")[OUTCOMES].count()
    counts["rows"] = df.groupby("paper").size()
    return counts


if __name__ == "__main__":
    from data_loader import load_data
    d = load_data()
    p = check_data(d)
    print("problems:", p if p else "none")
    print(coverage_table(d))
