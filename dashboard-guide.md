# Steam Games Power BI Dashboard — Build Guide

Follow these steps in **Power BI Desktop** (free download from Microsoft) to
assemble the dashboard from this repo. Estimated time: 30–45 minutes.

> **Note:** there is no `.pbix` file in this repo — a `.pbix` can only be
> produced inside Power BI Desktop. Everything the build needs (clean data,
> DAX measures, page specs) is here; the mockups in `mockups/` show the
> intended layout and the real numbers each visual should display.

---

## Step 1 — Prepare the data

```bash
pip install -r requirements.txt
python data-prep.py
```

This reads the raw Steam dataset and writes `data/steam_clean.csv`
(27,075 rows × 20 columns) with dashboard-ready derived columns:
`year`, `primary_genre` (first listed genre), `total_reviews`,
`pos_ratio`, `is_free`, `price_band`.

## Step 2 — Import into Power BI

1. Power BI Desktop → **Home → Get data → Text/CSV** → select
   `data/steam_clean.csv` → **Load**.
2. In **Model view**, rename the table to **`SteamGames`**.
3. Check data types (Power Query usually gets these right; fix if needed):
   - `release_date` → Date
   - `year`, `appid`, `positive_ratings`, `negative_ratings`,
     `total_reviews`, `achievements` → Whole Number
   - `price`, `pos_ratio`, `average_playtime`, `median_playtime` → Decimal Number
   - `is_free` → True/False

## Step 3 — Data model

The model is **intentionally a flat star**: one fact table
(`SteamGames`), no dimension tables. The dataset is a single snapshot
with no snowflake-worthy hierarchies, and every analysis question can be
answered by slicing this one table — which is exactly how a real analyst
would model it rather than over-engineering dimensions nobody needs.

## Step 4 — Create the DAX measures

**Modeling → New measure**, one at a time, pasting from
[`dax/measures.dax`](dax/measures.dax):

| Measure | Purpose |
|---|---|
| `Total Games` | KPI: games in current filter context |
| `Total Reviews` | KPI: review volume |
| `Avg Positive Ratio` | KPI: mean per-game positive ratio |
| `Median Price` | KPI: median price |
| `Free Share %` | KPI: free-to-play share of catalog |
| `Free Games` | helper for the free share |
| `Positive Review Ratio` | review-weighted sentiment (DIVIDE-safe) |
| `Games with 50+ Reviews` | filtered count for sentiment pages |
| `Avg Playtime (hrs)` | engagement KPI |
| `Games in Selection` | context-aware count for titles |

> Tip: format `Free Share %`, `Avg Positive Ratio` and
> `Positive Review Ratio` as **Percentage** (Modeling → Format).

---

## Page 1 — "Overview"

**Page-level filters:** none.

| # | Visual | Fields / Measures | Expected result |
|---|---|---|---|
| 1 | Card | `Total Games` | **27,075** |
| 2 | Card | `Avg Positive Ratio` + visual filter `total_reviews ≥ 50` | **0.745** |
| 3 | Card | `Median Price` + visual filter `price > 0` | **$4.79** |
| 4 | Card | `Free Share %` | **9.5%** |
| 5 | Clustered bar chart | Axis: `year` · Values: `Total Games` · filter `year ≥ 2005` | Peak **8,160 games in 2018** |
| 6 | Clustered bar chart | Axis: `primary_genre` (Top N = 10) · Values: `Total Games` | **Action** leads with **11,212** |
| 7 | Slicer | `year` (range slider) | drives visuals 1–6 |
| 8 | Slicer | `primary_genre` (dropdown) | drives visuals 1–6 |

Layout: 4 KPI cards across the top, bar charts side-by-side below,
slicers in a left rail. See `mockups/01_overview.svg`.

## Page 2 — "Pricing & Sentiment"

**Page-level filter:** `total_reviews ≥ 50` (keeps sentiment stats honest —
near-zero-review games would otherwise skew the averages).

| # | Visual | Fields / Measures | Expected result |
|---|---|---|---|
| 1 | Clustered bar chart | Axis: `price_band` (sort: Free, Under $5, $5-10, $10-20, $20-30, $30+) · Values: `Avg Positive Ratio` | **$10–20 band highest at 0.785**; Under $5 lowest at 0.713 |
| 2 | Card | `Positive Review Ratio` | review-weighted overall sentiment |
| 3 | Histogram of `price` | Use **Transform → New column** `price_bin = ROUND(SteamGames[price],0)` or the built-in binning on `price` (bin size 5, cap at 60) | right-skewed: most games under $10 |
| 4 | Scatter chart | X: `price` · Y: `total_reviews` · Size: `pos_ratio` · Details: `name` · filter `total_reviews ≥ 50` | blockbusters cluster high-sentiment |
| 5 | Slicer | `price_band` (chiclet/horizontal) | drives visuals 1–4 |

See `mockups/02_pricing_sentiment.svg`.

## Page 3 — "Genre Deep-Dive"

**Page-level filters:** none (the genre slicer does the work).

| # | Visual | Fields / Measures | Expected result |
|---|---|---|---|
| 1 | Slicer | `primary_genre` (vertical list, multi-select) | **drives every visual on the page** |
| 2 | Clustered bar chart | Axis: `primary_genre` (Top N = 8 by `Games with 50+ Reviews`) · Values: `Avg Positive Ratio` + visual filter `total_reviews ≥ 50` | **Adventure 0.776** on top |
| 3 | Cards | `Games in Selection`, `Avg Playtime (hrs)` | respond to the slicer |
| 4 | Table | `name`, `developer`, `total_reviews`, `pos_ratio` (%), `price` · sorted by `total_reviews` desc, Top N = 10 | CS:GO row: **3.05M reviews, 86.8% positive** |
| 5 | Donut chart | Legend: `is_free` · Values: `Total Games` | ~90/10 paid-vs-free split |

See `mockups/03_genre_deepdive.svg`.

---

## Sanity checklist (compare against these real numbers)

Computed from the data by `data-prep.py` — if your cards disagree,
check filters and formats first:

- Total games: **27,075**
- Avg positive ratio (50+ reviews): **0.745**
- Median paid price: **$4.79**
- Free-to-play share: **9.5%**
- Peak release year: **2018 (8,160 games)**
- Top genre: **Action (11,212 games)**
- Best-reviewed major genre: **Adventure (0.776)**
- Best price band: **$10–20 (0.785 positive ratio)**
