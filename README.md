# Steam Games Power BI Dashboard

A 3-page Power BI dashboard project analyzing **27,075 Steam store games** —
release trends, pricing vs. player sentiment, and a genre deep-dive — built on
a cleaned flat-table data model with hand-written DAX measures.

## What's in this repo

| File | Purpose |
|---|---|
| `data-prep.py` | Cleans the raw CSV → `data/steam_clean.csv` (run it yourself) |
| `dax/measures.dax` | 10 real DAX measures to paste into Power BI Desktop |
| `dashboard-guide.md` | Click-by-click build guide: import, model, measures, 3 page specs |
| `mockups/` | 3 layout mockups showing each page's design and real target numbers |
| `requirements.txt` | Python deps for the prep script |

## The three dashboard pages

1. **Overview** — KPI cards (27,075 games · 0.745 avg positive ratio · $4.79 median paid price · 9.5% free-to-play), releases-per-year bar (peak: 8,160 in 2018), top-10 genres bar (Action: 11,212), year + genre slicers.
2. **Pricing & Sentiment** — price-band vs. positive-ratio bar ($10–20 band highest at 0.785), price distribution histogram, price-vs-review-volume scatter, price-band slicer. Page filter: games with 50+ reviews.
3. **Genre Deep-Dive** — genre sentiment ranking (Adventure 0.776 on top), genre slicer driving all visuals, top-10 games by review volume table (CS:GO: 3.05M reviews, 86.8% positive), paid-vs-free donut.

## The honest fine print

- **There is no `.pbix` file here, and that's deliberate.** A `.pbix` can
  only be produced inside Power BI Desktop, which doesn't run in this
  environment — faking one would be dishonest. Follow
  [`dashboard-guide.md`](dashboard-guide.md) to assemble it yourself in
  30–45 minutes; the mockups show exactly what each page should look like.
- **The mockups are design mockups**, not screenshots. Every number on them
  was computed from the real dataset (see the sanity checklist in the guide).
- **The dataset CSV is not bundled** (too large for the repo). Download it
  free from Kaggle and point `data-prep.py` at it:

  **Source:** "Steam Store Games" by Nik Davis — https://www.kaggle.com/datasets/nikdavis/steam-store-games (CC-BY 4.0)

## How to run

```bash
pip install -r requirements.txt
# place the Kaggle CSV at ../steam-games-analysis/data/steam.csv (or edit RAW_PATH)
python data-prep.py        # → data/steam_clean.csv
python make_mockups.py      # regenerate the mockups (optional)
```

Then open Power BI Desktop and follow `dashboard-guide.md`.

## Tech

Python (pandas) · Power BI Desktop · DAX · matplotlib (mockups only)

## Key findings the dashboard surfaces

- Steam's catalog exploded after 2013: 418 releases → peak **8,160 in 2018**.
- It's a budget storefront: median paid price **$4.79**, only **9.5%** free-to-play.
- Cheapest isn't best-received: sub-$5 games score lowest (0.713); the **$10–20 band scores highest (0.785)**.
- **Action** dominates by count (11,212 games) but **Adventure** is best-reviewed (0.776).
- Popularity and sentiment move together: 5M+ owner blockbusters average 0.84+ positive vs. 0.76 for the long tail.
