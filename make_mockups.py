"""
Generate 3 dashboard layout mockups (design mockups, NOT Power BI screenshots).
Every number is computed live from data/steam_clean.csv — no hardcoded stats.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data" / "steam_clean.csv"
OUT = HERE / "mockups"
OUT.mkdir(exist_ok=True)

ACCENT = "#2563eb"
DARK = "#1e293b"
LIGHT_BG = "#f1f5f9"

df = pd.read_csv(DATA)
sub = df[df["total_reviews"] >= 50]  # sentiment base

# ---- shared aggregates (all real) -------------------------------------------
yearly = df[df["year"] >= 2005]["year"].value_counts().sort_index()
top_genres = df["primary_genre"].value_counts().head(10)
band_order = ["Free", "Under $5", "$5-10", "$10-20", "$20-30", "$30+"]
band_sent = sub.groupby("price_band")["pos_ratio"].mean().reindex(band_order)
g = sub.groupby("primary_genre")["pos_ratio"].agg(["mean", "count"])
genre_sent = g.nlargest(8, "count").sort_values("mean")
top_games = df.nlargest(10, "total_reviews")[["name", "total_reviews", "pos_ratio", "price"]]
free_share = df["is_free"].mean()


def header(ax, title):
    ax.text(0.01, 0.96, title, fontsize=20, fontweight="bold", color=DARK,
            transform=ax.transAxes, va="top", ha="left")
    ax.text(0.99, 0.96, "DESIGN MOCKUP — not a Power BI screenshot",
            fontsize=10, style="italic", color="#64748b",
            transform=ax.transAxes, va="top", ha="right")


def kpi_card(fig, x, y, w, h, label, value):
    ax = fig.add_axes([x, y, w, h])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    rect = mpatches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                   boxstyle="round,pad=0.02", fc="white",
                                   ec=ACCENT, lw=2)
    ax.add_patch(rect)
    ax.text(0.5, 0.62, value, fontsize=26, fontweight="bold", color=ACCENT,
            ha="center", va="center")
    ax.text(0.5, 0.28, label, fontsize=11, color=DARK, ha="center", va="center")


def panel(fig, x, y, w, h, title):
    ax = fig.add_axes([x, y, w, h])
    ax.set_title(title, fontsize=13, fontweight="bold", color=DARK,
                 loc="left", pad=8)
    return ax


def slicer_box(fig, x, y, w, h, label):
    ax = fig.add_axes([x, y, w, h])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(mpatches.FancyBboxPatch((0.02, 0.05), 0.96, 0.9,
                                         boxstyle="round,pad=0.02",
                                         fc=LIGHT_BG, ec="#94a3b8",
                                         lw=1.5, linestyle="--"))
    ax.text(0.5, 0.5, "" + label, fontsize=11, color="#475569",
            ha="center", va="center")


# ============ Page 1 — Overview ==============================================
fig = plt.figure(figsize=(16, 9), facecolor="#e2e8f0")
fig.text(0.5, 0.004, "Mockup 1 of 3 — layout concept only", ha="center",
         fontsize=9, color="#64748b", style="italic")
ax0 = fig.add_axes([0, 0, 1, 1]); ax0.axis("off")
header(ax0, "Page 1 — Overview")

kpi_card(fig, 0.02, 0.78, 0.225, 0.14, "Total Games", f"{len(df):,}")
kpi_card(fig, 0.265, 0.78, 0.225, 0.14, "Avg Positive Ratio (50+ reviews)",
         f"{sub['pos_ratio'].mean():.3f}")
kpi_card(fig, 0.51, 0.78, 0.225, 0.14, "Median Price (paid)",
         f"${df.loc[~df['is_free'], 'price'].median():.2f}")
kpi_card(fig, 0.755, 0.78, 0.225, 0.14, "Free-to-Play Share",
         f"{free_share * 100:.1f}%")

ax1 = panel(fig, 0.25, 0.08, 0.35, 0.62, "Games released per year")
ax1.bar(yearly.index, yearly.values, color=ACCENT, alpha=0.85)
peak_y, peak_v = int(yearly.idxmax()), int(yearly.max())
ax1.annotate(f"{peak_v:,}", (peak_y, peak_v), textcoords="offset points",
             xytext=(0, 6), ha="center", fontweight="bold", fontsize=11,
             color=DARK)
ax1.set_xlabel("Release year"); ax1.set_ylabel("Games released")
ax1.tick_params(axis="x", rotation=45, labelsize=8)

ax2 = panel(fig, 0.63, 0.08, 0.35, 0.62, "Top 10 genres by game count")
ax2.barh(top_genres.index, top_genres.values, color=ACCENT, alpha=0.85)
ax2.invert_yaxis()
ax2.text(top_genres.values[0] + 80, 0, f"{top_genres.values[0]:,}",
         va="center", fontweight="bold", color=DARK)
ax2.set_xlabel("Games")

slicer_box(fig, 0.02, 0.55, 0.19, 0.12, "Slicer: Year")
slicer_box(fig, 0.02, 0.40, 0.19, 0.12, "Slicer: Genre")
axn = fig.add_axes([0.02, 0.08, 0.19, 0.28]); axn.axis("off")
axn.text(0.5, 0.9, "Interactions", fontsize=12, fontweight="bold",
         color=DARK, ha="center", va="top")
axn.text(0.5, 0.6, "Both slicers drive\nall visuals on\nthis page.",
         fontsize=10, color="#475569", ha="center", va="top")
fig.savefig(OUT / "01_overview.svg", dpi=110, bbox_inches="tight")
plt.close(fig)

# ============ Page 2 — Pricing & Sentiment ====================================
fig = plt.figure(figsize=(16, 9), facecolor="#e2e8f0")
fig.text(0.5, 0.004, "Mockup 2 of 3 — layout concept only", ha="center",
         fontsize=9, color="#64748b", style="italic")
ax0 = fig.add_axes([0, 0, 1, 1]); ax0.axis("off")
header(ax0, "Page 2 — Pricing & Sentiment  (page filter: total_reviews ≥ 50)")

ax1 = panel(fig, 0.03, 0.45, 0.45, 0.42, "Avg positive ratio by price band")
colors = [ACCENT if b == "$10-20" else "#93c5fd" for b in band_order]
bars = ax1.bar(band_order, band_sent.values, color=colors)
ax1.set_ylim(0.65, 0.82)
best = band_sent.idxmax()
ax1.annotate(f"{band_sent.max():.3f} ← highest", (best, band_sent.max()),
             textcoords="offset points", xytext=(0, 8), ha="center",
             fontweight="bold", fontsize=11, color=DARK)
ax1.set_ylabel("Avg positive ratio")
ax1.tick_params(axis="x", rotation=20, labelsize=9)

ax2 = panel(fig, 0.52, 0.45, 0.45, 0.42, "Price distribution")
prices = df.loc[df["price"] <= 60, "price"]
ax2.hist(prices, bins=30, color=ACCENT, alpha=0.8)
ax2.axvline(df.loc[~df["is_free"], "price"].median(), color="#dc2626",
            linestyle="--", label=f"Median paid: ${df.loc[~df['is_free'], 'price'].median():.2f}")
ax2.legend(fontsize=9)
ax2.set_xlabel("Price (USD, capped at $60)"); ax2.set_ylabel("Games")

ax3 = panel(fig, 0.03, 0.06, 0.62, 0.32, "Price vs review volume (sample)")
s = sub.sample(min(1500, len(sub)), random_state=42)
sc = ax3.scatter(s["price"].clip(upper=60), s["total_reviews"],
                 c=s["pos_ratio"], cmap="RdYlGn", alpha=0.5, s=12,
                 vmin=0.5, vmax=1.0)
ax3.set_yscale("log")
ax3.set_xlabel("Price (USD, capped at $60)")
ax3.set_ylabel("Total reviews (log)")
plt.colorbar(sc, ax=ax3, label="Positive ratio", shrink=0.9)

slicer_box(fig, 0.70, 0.06, 0.27, 0.12, "Slicer: Price band")
axn = fig.add_axes([0.70, 0.20, 0.27, 0.12]); axn.axis("off")
axn.text(0.5, 0.5, "Card: Positive Review Ratio\n(review-weighted)",
         ha="center", va="center", fontsize=11, color=DARK,
         bbox=dict(boxstyle="round", fc="white", ec=ACCENT, lw=2))
fig.savefig(OUT / "02_pricing_sentiment.svg", dpi=110, bbox_inches="tight")
plt.close(fig)

# ============ Page 3 — Genre Deep-Dive =======================================
fig = plt.figure(figsize=(16, 9), facecolor="#e2e8f0")
fig.text(0.5, 0.004, "Mockup 3 of 3 — layout concept only", ha="center",
         fontsize=9, color="#64748b", style="italic")
ax0 = fig.add_axes([0, 0, 1, 1]); ax0.axis("off")
header(ax0, "Page 3 — Genre Deep-Dive")

slicer_box(fig, 0.02, 0.62, 0.20, 0.16, "Slicer: Genre\n(drives all visuals)")

ax1 = panel(fig, 0.25, 0.45, 0.42, 0.42, "Avg positive ratio by genre")
ax1.barh(genre_sent.index, genre_sent["mean"], color=ACCENT, alpha=0.85)
ax1.invert_yaxis()
ax1.text(genre_sent["mean"].iloc[-1] + 0.002, len(genre_sent) - 1,
         f"{genre_sent['mean'].iloc[-1]:.3f} ← top",
         va="center", fontweight="bold", color=DARK, fontsize=11)
ax1.set_xlim(0.6, 0.82)
ax1.set_xlabel("Avg positive ratio (8 most-reviewed genres, 50+ reviews)")

ax2 = fig.add_axes([0.70, 0.45, 0.27, 0.42]); ax2.axis("off")
ax2.set_title("Paid vs Free split", fontsize=13, fontweight="bold",
              color=DARK, loc="left", pad=8)
ax2.pie([1 - free_share, free_share], labels=["Paid", "Free"],
        autopct="%.1f%%", colors=[ACCENT, "#93c5fd"],
        startangle=90, textprops={"fontsize": 12})

ax3 = panel(fig, 0.02, 0.03, 0.95, 0.32, "Top 10 games by review volume")
ax3.axis("off")
rows = [["#", "Game", "Reviews", "Positive", "Price"]]
for i, r in enumerate(top_games.itertuples(), 1):
    rows.append([str(i), r.name[:38],
                 f"{int(r.total_reviews):,}",
                 f"{r.pos_ratio:.1%}", f"${r.price:.2f}"])
table = ax3.table(cellText=rows, loc="center", colWidths=[0.05, 0.45, 0.18, 0.16, 0.16])
table.auto_set_font_size(False)
table.set_fontsize(9)
for (ri, _), cell in table.get_celld().items():
    if ri == 0:
        cell.set_facecolor(ACCENT); cell.set_text_props(color="white",
                                                       fontweight="bold")
    elif ri % 2 == 0:
        cell.set_facecolor("#f8fafc")
fig.savefig(OUT / "03_genre_deepdive.svg", dpi=110, bbox_inches="tight")
plt.close(fig)

print("mockups written:", sorted(p.name for p in OUT.glob("*.svg")))
print(f"verified KPIs — games={len(df):,} peak={int(yearly.idxmax())}({int(yearly.max()):,}) "
      f"top_genre={top_genres.index[0]}({top_genres.iloc[0]:,}) "
      f"best_band={band_sent.idxmax()}({band_sent.max():.3f}) "
      f"top_sent_genre={genre_sent.index[-1]}({genre_sent['mean'].iloc[-1]:.3f}) "
      f"top_game={top_games.iloc[0]['name']}({int(top_games.iloc[0]['total_reviews']):,} reviews, "
      f"{top_games.iloc[0]['pos_ratio']:.1%})")
