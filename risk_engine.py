"""
AI & Financial Logic Engine Layer for Climate-Smart Agricultural Loan & Insurance Decision System
Implements RandomForestClassifier ML modeling and dynamic microfinance calculations.
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


class AgriRiskEngine:
    """
    AI & Financial Logic Engine.
    Combines meteorological machine learning risk predictions with
    parametric microfinance rules to determine dynamic loan interest rates
    and crop insurance payouts.
    """

    SEASON_MAP = {
        "Kharif": 0,
        "Rabi": 1,
        "Summer": 2
    }

    SEASON_REVERSE_MAP = {
        0: "Kharif",
        1: "Rabi",
        2: "Summer"
    }

    RISK_CLASSES = ["Low Risk", "Medium Risk", "High Risk"]

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model: Optional[RandomForestClassifier] = None
        self.model_metrics: Dict[str, Any] = {}
        self._train_initial_model()

    def _generate_synthetic_meteorological_data(self, n_samples: int = 1500) -> Tuple[np.ndarray, np.ndarray]:
        """
        Synthesize realistic agro-meteorological data incorporating crop thermal physics.
        Features: [obs_temp, forecast_max_temp, humidity, season_encoded]
        Target: 0 = Low Risk, 1 = Medium Risk, 2 = High Risk
        """
        np.random.seed(self.random_state)

        # Generate seasons uniformly: 0 (Kharif/Monsoon), 1 (Rabi/Winter), 2 (Summer/Zaid)
        seasons = np.random.choice([0, 1, 2], size=n_samples, p=[0.40, 0.35, 0.25])

        obs_temps = np.zeros(n_samples)
        forecast_temps = np.zeros(n_samples)
        humidities = np.zeros(n_samples)
        targets = np.zeros(n_samples, dtype=int)

        for i in range(n_samples):
            season = seasons[i]

            if season == 0:  # Kharif (Monsoon: humid, moderate to warm)
                obs_t = np.random.normal(30.0, 4.0)
                forecast_t = obs_t + np.random.normal(1.5, 1.2)
                hum = np.clip(np.random.normal(72.0, 12.0), 20.0, 98.0)
            elif season == 1:  # Rabi (Winter: cooler, critical wheat grain filling)
                obs_t = np.random.normal(24.0, 4.5)
                forecast_t = obs_t + np.random.normal(1.8, 1.5)
                hum = np.clip(np.random.normal(55.0, 14.0), 20.0, 95.0)
            else:  # Summer (Zaid: hot, dry/heatwaves)
                obs_t = np.random.normal(38.0, 4.5)
                forecast_t = obs_t + np.random.normal(2.5, 1.5)
                hum = np.clip(np.random.normal(38.0, 15.0), 10.0, 85.0)

            obs_temps[i] = np.clip(obs_t, 12.0, 49.0)
            forecast_temps[i] = np.clip(forecast_t, obs_temps[i] - 2.0, 52.0)
            humidities[i] = hum

            # Calculate Agronomic Thermal Stress Index
            t_max = max(obs_temps[i], forecast_temps[i])

            if season == 2:  # Summer heatwave vulnerability
                if t_max >= 42.0 or (t_max >= 39.5 and hum < 30.0):
                    stress_score = 2  # High Risk
                elif t_max >= 36.0 or (t_max >= 34.0 and hum > 65.0):
                    stress_score = 1  # Medium Risk
                else:
                    stress_score = 0  # Low Risk

            elif season == 1:  # Rabi terminal heat vulnerability (wheat shrivels above 32°C)
                if t_max >= 34.5:
                    stress_score = 2  # High Risk
                elif t_max >= 29.5 or hum < 30.0:
                    stress_score = 1  # Medium Risk
                else:
                    stress_score = 0  # Low Risk

            else:  # Kharif flood/drought/pest heat vulnerability
                if t_max >= 38.5 or (t_max >= 35.0 and hum > 85.0) or hum < 30.0:
                    stress_score = 2  # High Risk
                elif t_max >= 33.0 or hum > 80.0 or hum < 45.0:
                    stress_score = 1  # Medium Risk
                else:
                    stress_score = 0  # Low Risk

            # Add subtle stochastic environmental variability (5% realistic noise)
            if np.random.rand() < 0.04:
                stress_score = np.random.choice([0, 1, 2])

            targets[i] = stress_score

        X = np.column_stack([obs_temps, forecast_temps, humidities, seasons])
        y = targets
        return X, y

    def _train_initial_model(self) -> None:
        """
        Train the RandomForestClassifier model and compute verification accuracy metrics.
        """
        X, y = self._generate_synthetic_meteorological_data()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=self.random_state, stratify=y
        )

        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=4,
            random_state=self.random_state
        )
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=self.RISK_CLASSES, output_dict=True)

        feature_names = ["Observed Temp", "Forecast Max Temp", "Relative Humidity", "Season"]
        importances = dict(zip(feature_names, self.model.feature_importances_))

        self.model_metrics = {
            "test_accuracy": round(accuracy * 100, 2),
            "sample_count": len(X),
            "feature_importances": {k: round(v * 100, 2) for k, v in importances.items()},
            "classification_report": report
        }

    def predict_risk(
        self,
        obs_temp: float,
        forecast_temp: float,
        humidity: float,
        season: str
    ) -> Dict[str, Any]:
        """
        Predict crop yield failure risk classification and class probabilities.
        """
        if season not in self.SEASON_MAP:
            raise ValueError(f"Invalid season '{season}'. Expected one of {list(self.SEASON_MAP.keys())}")

        season_encoded = self.SEASON_MAP[season]
        input_vector = np.array([[obs_temp, forecast_temp, humidity, season_encoded]])

        pred_idx = int(self.model.predict(input_vector)[0])
        probabilities = self.model.predict_proba(input_vector)[0]

        risk_label = self.RISK_CLASSES[pred_idx]
        confidence = float(probabilities[pred_idx])

        prob_dict = {
            self.RISK_CLASSES[i]: round(float(probabilities[i]) * 100, 1)
            for i in range(len(self.RISK_CLASSES))
        }

        return {
            "risk_category": risk_label,
            "risk_index": pred_idx,
            "confidence_percent": round(confidence * 100, 1),
            "probabilities": prob_dict,
            "inputs": {
                "obs_temp": obs_temp,
                "forecast_temp": forecast_temp,
                "humidity": humidity,
                "season": season
            }
        }

    # -------------------------------------------------------------
    # Financial Calculation Rules
    # -------------------------------------------------------------
    @staticmethod
    def calculate_insurance_payout(loan_amount: float, risk_category: str) -> Tuple[float, float]:
        """
        Parametric insurance payout rule:
        - Low Risk    -> 0% of loan amount
        - Medium Risk -> 35% of loan amount
        - High Risk   -> 75% of loan amount

        Returns: (payout_amount, payout_percentage)
        """
        clean_risk = risk_category.strip().title()

        if "High" in clean_risk:
            percentage = 0.75
        elif "Medium" in clean_risk:
            percentage = 0.35
        elif "Low" in clean_risk:
            percentage = 0.0
        else:
            percentage = 0.0

        payout = round(loan_amount * percentage, 2)
        return payout, round(percentage * 100, 1)

    @staticmethod
    def calculate_adjusted_interest_rate(base_rate: float, risk_category: str) -> Tuple[float, float, str]:
        """
        Dynamic loan interest rate adjustment rule:
        - Low Risk    -> Standard interest rate - 1.0% (Incentive discount for climate resilience)
        - Medium Risk -> Standard interest rate + 1.5% (Thermal risk premium)
        - High Risk   -> Standard interest rate + 3.5% (High hazard restructuring tier)

        Returns: (adjusted_rate, rate_delta, rationale_text)
        """
        clean_risk = risk_category.strip().title()

        if "High" in clean_risk:
            delta = 3.5
            rationale = "Severe heatwave hazard (+3.5%). High default risk triggered; loan restructuring flagged."
        elif "Medium" in clean_risk:
            delta = 1.5
            rationale = "Moderate climate stress premium (+1.5%). Buffer required for potential yield drop."
        elif "Low" in clean_risk:
            delta = -1.0
            rationale = "Optimal agro-climatic conditions (-1.0%). Climate resilience incentive rate applied."
        else:
            delta = 0.0
            rationale = "Standard rate maintained."

        adjusted_rate = max(0.5, round(base_rate + delta, 2))
        return adjusted_rate, delta, rationale

    def evaluate_full_case(
        self,
        farmer_data: Dict[str, Any],
        obs_temp: float,
        forecast_temp: float,
        humidity: float,
        season: str
    ) -> Dict[str, Any]:
        """
        Orchestrates full assessment: ML classification + Financial insurance & interest computations.
        """
        risk_result = self.predict_risk(obs_temp, forecast_temp, humidity, season)
        risk_category = risk_result["risk_category"]

        loan_amount = float(farmer_data.get("loan_amount", 0.0))
        base_rate = float(farmer_data.get("interest_rate", 7.0))

        payout_amt, payout_pct = self.calculate_insurance_payout(loan_amount, risk_category)
        adj_rate, rate_delta, rate_rationale = self.calculate_adjusted_interest_rate(base_rate, risk_category)

        return {
            "farmer_id": farmer_data.get("farmer_id"),
            "farmer_name": farmer_data.get("name"),
            "crop_type": farmer_data.get("crop_type"),
            "region": farmer_data.get("region"),
            "loan_amount": loan_amount,
            "base_interest_rate": base_rate,
            "risk_category": risk_category,
            "confidence_percent": risk_result["confidence_percent"],
            "probabilities": risk_result["probabilities"],
            "calculated_payout": payout_amt,
            "payout_percentage": payout_pct,
            "adjusted_interest_rate": adj_rate,
            "rate_delta": rate_delta,
            "rate_rationale": rate_rationale,
            "meteorological_data": risk_result["inputs"]
        }
