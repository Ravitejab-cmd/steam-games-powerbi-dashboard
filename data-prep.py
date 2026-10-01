"""
Steam Games Power BI Dashboard — data preparation
=================================================
Cleans the raw "Steam Store Games" CSV and produces a dashboard-ready
flat table (data/steam_clean.csv) for import into Power BI Desktop.

Dataset: "Steam Store Games" by Nik Davis (Kaggle), CC-BY 4.0
          https://www.kaggle.com/datasets/nikdavis/steam-store-games

Run:
    pip install -r requirements.txt
    python data-prep.py

Input : ../steam-games-analysis/data/steam.csv   (raw, 27,075 rows x 18 cols)
Output: data/steam_clean.csv                     (cleaned, dashboard-ready)
"""

import numpy as np
import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
RAW_PATH = HERE.parent / "steam-games-analysis" / "data" / "steam.csv"
OUT_PATH = HERE / "data" / "steam_clean.csv"

MIN_REVIEWS = 50  # review-count floor used for sentiment stats


def main() -> None:
    df = pd.read_csv(RAW_PATH)
    print(f"Raw rows: {len(df):,} | columns: {list(df.columns)}")

    # --- dates -----------------------------------------------------------------
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year

    # --- reviews / sentiment ----------------------------------------------------
    df["total_reviews"] = df["positive_ratings"] + df["negative_ratings"]
    df["pos_ratio"] = np.where(
        df["total_reviews"] > 0,
        df["positive_ratings"] / df["total_reviews"],
        np.nan,
    )

    # --- genre ------------------------------------------------------------------
    # Primary genre = first genre listed by Steam
    df["primary_genre"] = df["genres"].fillna("Unknown").str.split(";").str[0]

    # --- price ------------------------------------------------------------------
    df["is_free"] = df["price"] == 0

    def price_band(p: float) -> str:
        if p == 0:
            return "Free"
        if p < 5:
            return "Under $5"
        if p < 10:
            return "$5-10"
        if p < 20:
            return "$10-20"
        if p < 30:
            return "$20-30"
        return "$30+"

    df["price_band"] = df["price"].apply(price_band)

    # --- keep the columns the dashboard needs ------------------------------------
    keep = [
        "appid", "name", "release_date", "year", "developer", "publisher",
        "platforms", "genres", "primary_genre", "steamspy_tags",
        "positive_ratings", "negative_ratings", "total_reviews", "pos_ratio",
        "average_playtime", "median_playtime", "owners", "price",
        "is_free", "price_band",
    ]
    df = df[keep]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {OUT_PATH} — {len(df):,} rows x {len(df.columns)} columns")

    # --- sanity summary (mirrors the DAX KPI cards) ----------------------------
    sub = df[df["total_reviews"] >= MIN_REVIEWS]
    print("\n--- KPI sanity check (from the cleaned table) ---")
    print(f"Total games               : {len(df):,}")
    print(f"Avg positive ratio        : {sub['pos_ratio'].mean():.3f} (50+ reviews)")
    print(f"Median price (paid games) : ${df.loc[~df['is_free'], 'price'].median():.2f}")
    print(f"Free-to-play share        : {df['is_free'].mean() * 100:.1f}%")
    print(f"Total reviews             : {df['total_reviews'].sum():,}")
    peak = df["year"].value_counts()
    print(f"Peak release year         : {int(peak.idxmax())} ({int(peak.max()):,} games)")
    print(f"Top genre                 : {df['primary_genre'].value_counts().idxmax()} "
          f"({df['primary_genre'].value_counts().iloc[0]:,} games)")
    order = ["Free", "Under $5", "$5-10", "$10-20", "$20-30", "$30+"]
    bands = sub.groupby("price_band")["pos_ratio"].mean().reindex(order)
    print("\nPositive ratio by price band (50+ reviews):")
    print(bands.round(3).to_string())
    g = sub.groupby("primary_genre")["pos_ratio"].agg(["mean", "count"])
    print("\nTop genres by avg positive ratio (8 most-reviewed):")
    print(g.nlargest(8, "count").sort_values("mean").round(3).to_string())


if __name__ == "__main__":
    main()
