import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "material_prices.csv"))
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "price_model.pkl"))

class PricingService:
    def __init__(self):
        self.model = None
        self.metrics = {}
        self.load_or_train()

    def load_or_train(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"[PricingService] Loaded existing model from {MODEL_PATH}")
                return
            except Exception as e:
                print(f"[PricingService] Error loading model: {e}, retraining...")

        self.train_model()

    def train_model(self):
        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError(f"Prices dataset not found at {DATASET_PATH}")

        df = pd.read_csv(DATASET_PATH)
        X = df.drop(columns=["selling_price"])
        y = df["selling_price"]

        categorical = ["material_type", "condition", "colour", "location"]
        numerical = ["quantity_kg", "width_inches", "reference_price"]

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical)
            ],
            remainder="passthrough"
        )

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))
        ])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
        r2 = r2_score(y_test, predictions)

        self.metrics = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 4),
            "samples_trained": len(X_train),
            "samples_tested": len(X_test)
        }
        print(f"[PricingService] Trained Model: MAE=INR {mae:.2f}, RMSE=INR {rmse:.2f}, R2={r2:.4f}")

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(pipeline, MODEL_PATH)
        self.model = pipeline

    def predict_price(self, material_type: str, condition: str, quantity_kg: float,
                      width_inches: float, colour: str, location: str, reference_price: float):
        if self.model is None:
            self.load_or_train()

        input_df = pd.DataFrame([{
            "material_type": material_type,
            "condition": condition,
            "quantity_kg": quantity_kg,
            "width_inches": width_inches,
            "colour": colour,
            "location": location,
            "reference_price": reference_price
        }])

        pred_price = float(self.model.predict(input_df)[0])
        # Reasonable market range calculation: approx +/- 7%
        price_min = round(pred_price * 0.93, 2)
        price_max = round(pred_price * 1.07, 2)
        suggested = round(pred_price, 2)

        return {
            "suggested_price": suggested,
            "suggested_price_min": price_min,
            "suggested_price_max": price_max,
            "unit": "INR/kg",
            "model_name": "Random Forest Regressor (200 trees)",
            "input_summary": {
                "Material": material_type,
                "Quantity": f"{quantity_kg} kg",
                "Condition": condition,
                "Location": location
            }
        }

pricing_service = PricingService()
