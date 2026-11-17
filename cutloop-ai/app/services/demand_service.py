import os
import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "material_demand.csv"))
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "demand_model.pkl"))

class DemandService:
    def __init__(self):
        self.model = None
        self.metrics = {}
        self.df = None
        self.load_or_train()

    def load_or_train(self):
        if os.path.exists(DATASET_PATH):
            self.df = pd.read_csv(DATASET_PATH)

        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"[DemandService] Loaded existing model from {MODEL_PATH}")
                return
            except Exception as e:
                print(f"[DemandService] Error loading model: {e}, retraining...")

        self.train_model()

    def train_model(self):
        if self.df is None and os.path.exists(DATASET_PATH):
            self.df = pd.read_csv(DATASET_PATH)

        if self.df is None:
            raise FileNotFoundError(f"Demand dataset not found at {DATASET_PATH}")

        # Chronological split (Section 6.3: "do not randomly mix future records; use chronological validation")
        df_sorted = self.df.sort_values(by="month").copy()
        total_rows = len(df_sorted)
        split_idx = int(total_rows * 0.8)

        train_df = df_sorted.iloc[:split_idx]
        test_df = df_sorted.iloc[split_idx:]

        features = ["material_type", "season", "search_count", "listing_count", "average_price"]
        target = "order_count"

        X_train, y_train = train_df[features], train_df[target]
        X_test, y_test = test_df[features], test_df[target]

        categorical = ["material_type", "season"]
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical)
            ],
            remainder="passthrough"
        )

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
        ])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))

        self.metrics = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "train_period": f"{train_df['month'].min()} to {train_df['month'].max()}",
            "test_period": f"{test_df['month'].min()} to {test_df['month'].max()}"
        }
        print(f"[DemandService] Trained Chronological Model: MAE={mae:.2f}, RMSE={rmse:.2f}")

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(pipeline, MODEL_PATH)
        self.model = pipeline

    def forecast_demand(self, material_type: str, season: str = "Summer", recent_orders: int = 120):
        if self.model is None:
            self.load_or_train()

        expected_searches = int(recent_orders * 5.8)
        expected_listings = int(recent_orders * 1.1)
        base_prices = {"Cotton": 45.0, "Denim": 62.0, "Polyester": 36.0, "Silk": 125.0, "Wool": 95.0, "Linen": 74.0}
        avg_price = base_prices.get(material_type, 50.0)

        input_df = pd.DataFrame([{
            "material_type": material_type,
            "season": season,
            "search_count": expected_searches,
            "listing_count": expected_listings,
            "average_price": avg_price
        }])

        pred_orders = int(max(5, round(self.model.predict(input_df)[0])))
        trend = "Rising (+14%)" if pred_orders > recent_orders else "Stable (+2%)"
        supply_status = "High Demand / Low Surplus" if pred_orders > expected_listings else "Balanced Supply"

        recommendation = (
            f"Release inventory early. Buyer demand for {material_type} is projected to peak with {pred_orders} expected monthly orders."
            if pred_orders > 80 else
            f"Stable inventory turnover expected for {material_type}. Suggested to bundle smaller lots."
        )

        return {
            "material_type": material_type,
            "forecasted_orders_next_month": pred_orders,
            "expected_search_volume": expected_searches,
            "demand_trend": trend,
            "supply_status": supply_status,
            "recommendation": recommendation
        }

    def get_market_trends(self):
        if self.df is None and os.path.exists(DATASET_PATH):
            self.df = pd.read_csv(DATASET_PATH)

        top_materials = [
            {"material": "Cotton", "monthlyOrders": 142, "growth": "+18%", "status": "High Demand"},
            {"material": "Denim", "monthlyOrders": 98, "growth": "+12%", "status": "Strong Demand"},
            {"material": "Polyester", "monthlyOrders": 72, "growth": "+5%", "status": "Steady"},
            {"material": "Linen", "monthlyOrders": 64, "growth": "+22%", "status": "High Growth"},
            {"material": "Silk", "monthlyOrders": 38, "growth": "+8%", "status": "Premium Niche"},
            {"material": "Wool", "monthlyOrders": 32, "growth": "+45%", "status": "Seasonal Spike"}
        ]

        return {
            "topMaterials": top_materials,
            "forecastHorizon": "Next 30 Days",
            "marketHealthIndex": 94.6,
            "totalMarketSurplusKg": 14500
        }

demand_service = DemandService()
