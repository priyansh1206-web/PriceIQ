<p align="center">
  <img src="https://img.shields.io/badge/ML-Regression%20%7C%20Demand%20Modeling-6C63FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/status-active-00C2A8?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge" />
</p>

# 💰 PriceIQ — Dynamic Pricing Optimization for E-commerce Products

> Predict the demand. Optimize the price. Maximize the revenue.

**PriceIQ** is a Machine Learning-based system that analyzes historical sales, pricing, competitor, and demand data to recommend the **optimal price point** for e-commerce products — maximizing revenue while respecting inventory constraints.

---

## 🚀 Features

- 📈 **Demand Prediction** — forecasts expected unit sales at any given price using lag features, rolling trends, and price-elasticity signals
- 💸 **Price Simulation Engine** — tests multiple price scenarios (±30%) per product and calculates expected revenue for each
- 🎯 **Optimal Price Recommendation** — picks the revenue-maximizing price per product, constrained by current inventory
- 📊 **Interactive Dashboard** — visualizes price-demand curves, revenue optimization curves, competitor comparisons, and category-wise performance
- 🧠 **Model Benchmarking** — compares Linear Regression, Random Forest, XGBoost, and LightGBM on MAE, RMSE, MAPE, and R²
- 🏷️ **Revenue Uplift Estimation** — quantifies expected % revenue gain vs current pricing strategy

---

## 🧩 Problem Statement

E-commerce platforms constantly face the question:

> *"Product ka price kitna rakhein jisse sales aur revenue maximum ho?"*

PriceIQ answers this by learning how demand responds to price changes (price elasticity), competitor pricing, seasonality, and promotions — then simulating pricing scenarios to recommend the price that maximizes revenue without overselling stock.

**Example:**

| Product | Current Price | Predicted Demand | Optimal Price | Expected Revenue |
|---|---|---|---|---|
| Running Shoes | ₹4,999 | 120 units | ₹4,699 | ₹5.63L |

---

## 🏗️ Machine Learning Workflow

1. Clean historical sales and pricing data
2. Engineer lag features (`sales_lag_1`, `sales_lag_7`, 7-day rolling mean)
3. Compute price elasticity of demand per product/category
4. Train regression models: **Linear Regression, Random Forest, XGBoost, LightGBM**
5. Simulate multiple price scenarios per product
6. Calculate `Expected Revenue = Predicted Demand × Proposed Price`
7. Select the revenue-maximizing price subject to inventory constraints

---

## 📊 Data Features

`Product ID` · `Category` · `Current Price` · `Competitor Price` · `Historical Sales Quantity` · `Discount %` · `Inventory Level` · `Product Rating` · `Demand Level` · `Seasonality Indicator` · `Promotion Flag` · `Revenue`

---

## 📐 Evaluation Metrics

- MAE · RMSE · MAPE · R² Score
- Revenue uplift compared to current pricing

---

## 🖥️ Tech Stack

`Python` · `Pandas` · `NumPy` · `Scikit-learn` · `XGBoost` · `LightGBM` · `Matplotlib / Seaborn` · `Streamlit`

---

## 📦 Final Deliverable

A dynamic pricing dashboard that recommends optimal prices, expected demand, expected revenue, competitor comparison, and inventory-aware pricing suggestions for every product.

---

## 🔮 Advanced Extension (Roadmap)

- [ ] Reinforcement Learning-based pricing policy that continuously learns from customer response
- [ ] Real-time competitor price scraping integration
- [ ] Multi-product bundle pricing optimization

---

## ⚙️ Getting Started

```bash
git clone https://github.com/<your-username>/PriceIQ.git
cd PriceIQ
pip install -r requirements.txt

# Generate dataset
python data/generate_data.py

# Train & compare models
python src/train_models.py

# Run price optimization
python src/price_optimizer.py

# Launch dashboard
streamlit run dashboard/app.py
```

---

## 📁 Project Structure

```
PriceIQ/
├── data/                # Dataset & data generation script
├── src/                 # Feature engineering, training, optimization
├── dashboard/            # Streamlit dashboard app
├── models/               # Trained models & recommendation outputs
├── visuals/               # Generated charts
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<p align="center">Made with ❤️ and a lot of price simulations</p>
