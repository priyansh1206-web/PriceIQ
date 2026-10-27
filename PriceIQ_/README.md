
This repository contains only the project stages requested for submission:
1. Exploratory Data Analysis (EDA)
2. Data preprocessing: missing values, encoding, standardization/scaling, and outlier detection/removal.

The raw dataset is the same dataset supplied in the original project ZIP. No model training, model evaluation, price optimization, or dashboard files are included.

## Folder structure

```text
PriceIQ_EDA_Preprocessing/
├── data/
│   ├── raw/
│   │   └── ecommerce_pricing_data.csv
│   └── processed/
├── reports/
│   ├── figures/
│   ├── eda_summary.txt
│   └── preprocessing_report.txt
├── src/
│   ├── preprocessing.py
│   └── eda_visualization.py
├── requirements.txt
└── README.md
```

## Run in VS Code

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run preprocessing first:

```bash
python src/preprocessing.py
```

This creates:
- `data/processed/cleaned_pricing_data.csv`
- `data/processed/encoded_scaled_data.csv`
- `reports/preprocessing_report.txt`

Then run EDA:

```bash
python src/eda_visualization.py
```

This creates graphs in `reports/figures/` and the summary in `reports/eda_summary.txt`.

## Included EDA graphs

- Historical price vs sales quantity
- Total demand trend over time
- Total revenue trend over time
- Current price vs competitor price by category
- Price elasticity curve by category
- Category-wise pricing performance charts
- Correlation heatmap

## Preprocessing methods

- Duplicate row removal
- Missing-value imputation
- Negative price correction
- IQR-based outlier detection and row removal
- One-hot encoding of categorical columns
- StandardScaler standardization of numeric columns

`cleaned_pricing_data.csv` is kept readable for EDA. `encoded_scaled_data.csv` is the encoded and standardized version created for the preprocessing requirement.
