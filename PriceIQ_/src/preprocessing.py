from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "ecommerce_pricing_data.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
CLEAN_PATH = PROCESSED_DIR / "cleaned_pricing_data.csv"
ENCODED_PATH = PROCESSED_DIR / "encoded_scaled_data.csv"
REPORT_PATH = ROOT / "reports" / "preprocessing_report.txt"

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW_PATH, parse_dates=["date"])
    original_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    for col in ["current_price", "competitor_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = df.loc[df[col] < 0, col].abs()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    missing_before = int(df.isna().sum().sum())
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    for col in categorical_cols:
        mode = df[col].mode(dropna=True)
        if not mode.empty:
            df[col] = df[col].fillna(mode.iloc[0])

    # Outlier detection and removal using the IQR rule on numeric columns.
    outlier_mask = pd.Series(False, index=df.index)
    outlier_counts = {}
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        if pd.isna(iqr) or iqr == 0:
            outlier_counts[col] = 0
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        col_mask = (df[col] < lower) | (df[col] > upper)
        outlier_counts[col] = int(col_mask.sum())
        outlier_mask |= col_mask

    removed_outlier_rows = int(outlier_mask.sum())
    df = df.loc[~outlier_mask].copy()

    if "revenue" in df.columns and {"current_price", "historical_sales_quantity"}.issubset(df.columns):
        df["revenue"] = df["current_price"] * df["historical_sales_quantity"]

    df.to_csv(CLEAN_PATH, index=False)

    # One-hot encode nominal categories and standardize numeric columns.
    encoded = df.drop(columns=["date"], errors="ignore").copy()
    categorical_cols = encoded.select_dtypes(include=["object", "category"]).columns.tolist()
    encoded = pd.get_dummies(encoded, columns=categorical_cols, drop_first=False, dtype=int)
    numeric_cols = encoded.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        scaler = StandardScaler()
        encoded[numeric_cols] = scaler.fit_transform(encoded[numeric_cols])
    encoded.to_csv(ENCODED_PATH, index=False)

    report = [
        "PREPROCESSING REPORT",
        "====================",
        f"Input rows: {original_rows}",
        f"Duplicate rows removed: {duplicate_rows}",
        f"Missing values before imputation: {missing_before}",
        f"Rows removed by IQR outlier detection: {removed_outlier_rows}",
        "",
        "Outlier counts detected per numeric column:",
    ]
    report += [f"{col}: {count}" for col, count in outlier_counts.items()]
    report += [
        "",
        f"Cleaned dataset rows: {len(df)}",
        f"Cleaned dataset columns: {len(df.columns)}",
        f"Encoded/scaled dataset rows: {len(encoded)}",
        f"Encoded/scaled dataset columns: {len(encoded.columns)}",
        "",
        "Methods: duplicate removal, missing-value imputation, negative-price correction,",
        "IQR outlier detection/removal, one-hot encoding, and StandardScaler standardization.",
    ]
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"\nSaved: {CLEAN_PATH}")
    print(f"Saved: {ENCODED_PATH}")

if __name__ == "__main__":
    main()
