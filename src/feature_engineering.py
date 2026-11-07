# feature_engineering.py
# adds a few simple columns that make the comparisons easier

import pandas as pd


def weave_group(structure):
    """turn the messy 'structure' text into a few groups"""
    s = str(structure).lower()
    if "plain" in s and "flat knit" not in s:
        return "plain weave"
    if "twill" in s:
        return "twill"
    if "satin" in s:
        return "satin"
    if "knit" in s:
        return "knit"
    if "handloom" in s:
        return "handloom"
    return "other"


def add_features(df):
    df = df.copy()

    # wool bands, because wool % comes in only a few levels in each paper
    df["wool_band"] = pd.cut(
        df["wool_pct"],
        bins=[-1, 30, 50, 100],
        labels=["0-30 %", "31-50 %", ">50 %"],
    )

    df["weave_group"] = df["structure"].apply(weave_group)

    # is the other fibre synthetic or not?
    # (all the papers we have use a synthetic as the other fibre)
    df["other_is_synthetic"] = df["other_fiber"].notna()

    # for the pilling count (pills per sq inch) lower is better, so make a
    # simple flag for the "good" fabrics (1 pill or less on average)
    df["pilling_count_low"] = df["pilling_count"] <= 2

    return df


if __name__ == "__main__":
    from data_loader import load_data
    d = add_features(load_data())
    print(d[["wool_pct", "wool_band", "structure", "weave_group"]].drop_duplicates().head(15))
