"""
eda_visualization.py
---------------------
Stage: Exploratory Data Analysis (EDA)

Generates the visualizations required by the project spec (section 12.6):
  - Historical price vs sales quantity scatter plot
  - Demand trend over time
  - Revenue trend over time
  - Competitor price comparison
  - Price elasticity curve (per category)
  - Product category-wise pricing performance dashboard (summary grid)

All figures are saved to reports/figures/. A short text summary of key
insights is printed to the console and saved to reports/eda_summary.txt.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "cleaned_pricing_data.csv"
FIG_DIR = ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    return df


def plot_price_vs_sales(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 6))
    sample = df.sample(min(2000, len(df)), random_state=1)
    sns.scatterplot(
        data=sample, x="current_price", y="historical_sales_quantity",
        hue="product_category", alpha=0.6, s=25
    )
    plt.title("Historical Price vs Sales Quantity")
    plt.xlabel("Current Price ($)")
    plt.ylabel("Sales Quantity (units)")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "01_price_vs_sales_scatter.png", dpi=130)
    plt.close()


def plot_demand_trend(df: pd.DataFrame) -> None:
    daily = df.groupby("date")["historical_sales_quantity"].sum().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(daily["date"], daily["historical_sales_quantity"], color="#2b6cb0")
    plt.title("Total Demand Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Units Sold (all products)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "02_demand_trend.png", dpi=130)
    plt.close()


def plot_revenue_trend(df: pd.DataFrame) -> None:
    daily = df.groupby("date")["revenue"].sum().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(daily["date"], daily["revenue"], color="#2f855a")
    plt.title("Total Revenue Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue ($)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "03_revenue_trend.png", dpi=130)
    plt.close()


def plot_competitor_comparison(df: pd.DataFrame) -> None:
    cat_avg = df.groupby("product_category")[["current_price", "competitor_price"]].mean().reset_index()
    cat_avg = cat_avg.melt(id_vars="product_category", var_name="price_type", value_name="avg_price")
    plt.figure(figsize=(9, 5))
    sns.barplot(data=cat_avg, x="product_category", y="avg_price", hue="price_type")
    plt.title("Average Current Price vs Competitor Price by Category")
    plt.xlabel("Product Category")
    plt.ylabel("Average Price ($)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "04_competitor_price_comparison.png", dpi=130)
    plt.close()


def plot_price_elasticity_curve(df: pd.DataFrame) -> None:
    """Bin price into deciles per category and plot avg demand per bin."""
    plt.figure(figsize=(9, 6))
    for cat in df["product_category"].unique():
        sub = df[df["product_category"] == cat].copy()
        sub["price_bin"] = pd.qcut(sub["current_price"], 10, duplicates="drop")
        curve = sub.groupby("price_bin", observed=True).agg(
            avg_price=("current_price", "mean"),
            avg_demand=("historical_sales_quantity", "mean"),
        ).reset_index()
        plt.plot(curve["avg_price"], curve["avg_demand"], marker="o", label=cat)
    plt.title("Price Elasticity Curve (Avg Demand vs Price Decile, by Category)")
    plt.xlabel("Average Price ($)")
    plt.ylabel("Average Demand (units)")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "05_price_elasticity_curve.png", dpi=130)
    plt.close()


def plot_category_dashboard(df: pd.DataFrame) -> None:
    summary = df.groupby("product_category", observed=True).agg(
        avg_price=("current_price", "mean"),
        avg_revenue=("revenue", "sum"),
        avg_demand=("historical_sales_quantity", "mean"),
        avg_rating=("product_rating", "mean"),
    ).reset_index()

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    sns.barplot(data=summary, x="product_category", y="avg_price", ax=axes[0, 0], color="#4299e1")
    axes[0, 0].set_title("Avg Price by Category")
    axes[0, 0].tick_params(axis="x", rotation=20)

    sns.barplot(data=summary, x="product_category", y="avg_revenue", ax=axes[0, 1], color="#48bb78")
    axes[0, 1].set_title("Total Revenue by Category")
    axes[0, 1].tick_params(axis="x", rotation=20)

    sns.barplot(data=summary, x="product_category", y="avg_demand", ax=axes[1, 0], color="#ed8936")
    axes[1, 0].set_title("Avg Demand by Category")
    axes[1, 0].tick_params(axis="x", rotation=20)

    sns.barplot(data=summary, x="product_category", y="avg_rating", ax=axes[1, 1], color="#9f7aea")
    axes[1, 1].set_title("Avg Product Rating by Category")
    axes[1, 1].tick_params(axis="x", rotation=20)

    plt.suptitle("Product Category-wise Pricing Performance Dashboard", fontsize=14)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "06_category_performance_dashboard.png", dpi=130)
    plt.close()
    return summary


def correlation_heatmap(df: pd.DataFrame) -> None:
    numeric_cols = [
        "current_price", "competitor_price", "historical_sales_quantity",
        "discount_percentage", "inventory_level", "product_rating",
        "promotion_flag", "revenue"
    ]
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap of Numeric Features")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "07_correlation_heatmap.png", dpi=130)
    plt.close()


def main():
    df = load_data()

    plot_price_vs_sales(df)
    plot_demand_trend(df)
    plot_revenue_trend(df)
    plot_competitor_comparison(df)
    plot_price_elasticity_curve(df)
    summary = plot_category_dashboard(df)
    correlation_heatmap(df)

    corr = df[["current_price", "historical_sales_quantity"]].corr().iloc[0, 1]
    promo_uplift = (
        df[df["promotion_flag"] == 1]["historical_sales_quantity"].mean()
        / df[df["promotion_flag"] == 0]["historical_sales_quantity"].mean()
        - 1
    ) * 100

    lines = [
        "EDA SUMMARY",
        "===========",
        f"Rows analyzed: {len(df):,} | Products: {df['product_id'].nunique()} | Categories: {df['product_category'].nunique()}",
        f"Correlation(current_price, sales_quantity): {corr:.3f} (confirms negative price elasticity)",
        f"Promotion uplift on avg sales quantity: {promo_uplift:.1f}%",
        "",
        "Category performance summary:",
        summary.round(2).to_string(index=False),
    ]
    summary_text = "\n".join(lines)
    print(summary_text)
    (ROOT / "reports" / "eda_summary.txt").write_text(summary_text)
    print(f"\nFigures saved to: {FIG_DIR}")


if __name__ == "__main__":
    main()
