"""
Comprehensive Test Suite for Climate-Smart Agricultural Loan & Insurance Decision System
Verifies Database CRUD, AI Model Classification, Financial Calculations, and End-to-End Workflow.
"""

import os
import unittest
import tempfile
from db_manager import DatabaseManager
from risk_engine import AgriRiskEngine


class TestAgriFinanceSystem(unittest.TestCase):

    def setUp(self):
        """Create a temporary database for isolated testing."""
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        self.db = DatabaseManager(db_path=self.temp_db_path)
        self.engine = AgriRiskEngine(random_state=42)

    def tearDown(self):
        """Close and remove temporary test database."""
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    # -------------------------------------------------------------------------
    # 1. Database Architecture Tests
    # -------------------------------------------------------------------------
    def test_database_initialization_and_seeding(self):
        """Verify automatic table creation and initial dummy farmer seeding."""
        farmers = self.db.get_all_farmers()
        self.assertGreaterEqual(len(farmers), 8, "Expected at least 8 seeded farmers on first launch.")
        first = farmers[0]
        self.assertIn("name", first)
        self.assertIn("crop_type", first)
        self.assertIn("loan_amount", first)
        self.assertIn("interest_rate", first)
        self.assertIn("credit_score", first)

    def test_farmer_crud_operations(self):
        """Verify adding, retrieving, updating, and deleting farmer records."""
        new_id = self.db.add_farmer(
            name="Kavita Rao",
            region="Warangal, Telangana",
            crop_type="Chilli",
            farm_size_acres=8.0,
            loan_amount=10000.0,
            interest_rate=8.0,
            credit_score=750
        )
        self.assertIsInstance(new_id, int)

        farmer = self.db.get_farmer(new_id)
        self.assertIsNotNone(farmer)
        self.assertEqual(farmer["name"], "Kavita Rao")
        self.assertEqual(farmer["crop_type"], "Chilli")

        # Update
        updated = self.db.update_farmer(
            farmer_id=new_id,
            name="Kavita Rao",
            region="Warangal, Telangana",
            crop_type="Organic Chilli",
            farm_size_acres=9.5,
            loan_amount=12000.0,
            interest_rate=7.8,
            credit_score=760
        )
        self.assertTrue(updated)
        farmer_updated = self.db.get_farmer(new_id)
        self.assertEqual(farmer_updated["crop_type"], "Organic Chilli")
        self.assertEqual(farmer_updated["loan_amount"], 12000.0)

        # Delete
        deleted = self.db.delete_farmer(new_id)
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_farmer(new_id))

    def test_assessment_and_claim_logging(self):
        """Verify logging of risk assessments and payout claims."""
        farmers = self.db.get_all_farmers()
        fid = farmers[0]["farmer_id"]

        asst_id = self.db.add_risk_assessment(
            farmer_id=fid,
            obs_temp=42.0,
            predicted_temp=44.0,
            season="Summer",
            risk_score="High Risk",
            calculated_payout=7500.0,
            adjusted_interest_rate=11.5
        )
        self.assertGreater(asst_id, 0)

        claim_id = self.db.add_payout_claim(
            farmer_id=fid,
            claim_amount=7500.0,
            status="Pending",
            assessment_id=asst_id
        )
        self.assertGreater(claim_id, 0)

        # Transition claim status
        self.db.update_claim_status(claim_id, "Approved")
        self.db.update_claim_status(claim_id, "Disbursed")

        kpis = self.db.get_financial_kpis()
        self.assertGreaterEqual(kpis["total_disbursed"], 7500.0)

    # -------------------------------------------------------------------------
    # 2. AI Logic & Scikit-Learn Model Tests
    # -------------------------------------------------------------------------
    def test_model_training_and_accuracy(self):
        """Verify RandomForest model achieves high accuracy on validation data."""
        acc = self.engine.model_metrics["test_accuracy"]
        self.assertGreater(acc, 85.0, f"Model accuracy {acc}% is below acceptable threshold 85%.")
        self.assertIn("classification_report", self.engine.model_metrics)
        self.assertIn("feature_importances", self.engine.model_metrics)

    def test_ml_prediction_bounds(self):
        """Verify model returns expected risk labels, probabilities, and confidences."""
        result = self.engine.predict_risk(obs_temp=43.0, forecast_temp=45.0, humidity=25.0, season="Summer")
        self.assertIn(result["risk_category"], ["Low Risk", "Medium Risk", "High Risk"])
        self.assertEqual(result["risk_category"], "High Risk")
        self.assertGreater(result["confidence_percent"], 50.0)

        # Low risk test in cool conditions
        cool_result = self.engine.predict_risk(obs_temp=24.0, forecast_temp=25.5, humidity=65.0, season="Rabi")
        self.assertEqual(cool_result["risk_category"], "Low Risk")

    # -------------------------------------------------------------------------
    # 3. Financial Calculation Rules Tests
    # -------------------------------------------------------------------------
    def test_financial_payout_rules(self):
        """
        Verify parametric insurance payout rules:
        - Low Risk -> 0%
        - Medium Risk -> 35%
        - High Risk -> 75%
        """
        loan = 10000.0
        p_low, pct_low = self.engine.calculate_insurance_payout(loan, "Low Risk")
        self.assertEqual(p_low, 0.0)
        self.assertEqual(pct_low, 0.0)

        p_med, pct_med = self.engine.calculate_insurance_payout(loan, "Medium Risk")
        self.assertEqual(p_med, 3500.0)
        self.assertEqual(pct_med, 35.0)

        p_high, pct_high = self.engine.calculate_insurance_payout(loan, "High Risk")
        self.assertEqual(p_high, 7500.0)
        self.assertEqual(pct_high, 75.0)

    def test_dynamic_interest_adjustment_rules(self):
        """
        Verify interest adjustments:
        - Low Risk -> base - 1.0%
        - Medium Risk -> base + 1.5%
        - High Risk -> base + 3.5%
        """
        base = 8.0
        r_low, d_low, _ = self.engine.calculate_adjusted_interest_rate(base, "Low Risk")
        self.assertEqual(r_low, 7.0)
        self.assertEqual(d_low, -1.0)

        r_med, d_med, _ = self.engine.calculate_adjusted_interest_rate(base, "Medium Risk")
        self.assertEqual(r_med, 9.5)
        self.assertEqual(d_med, 1.5)

        r_high, d_high, _ = self.engine.calculate_adjusted_interest_rate(base, "High Risk")
        self.assertEqual(r_high, 11.5)
        self.assertEqual(d_high, 3.5)

    # -------------------------------------------------------------------------
    # 4. End-to-End Evaluation Workflow
    # -------------------------------------------------------------------------
    def test_evaluate_full_case_workflow(self):
        """Verify orchestration of full case combining ML, finance, and farmer context."""
        farmer = {
            "farmer_id": 99,
            "name": "Test Farmer",
            "region": "Punjab",
            "crop_type": "Wheat",
            "loan_amount": 20000.0,
            "interest_rate": 8.0
        }
        res = self.engine.evaluate_full_case(farmer, 44.0, 46.0, 20.0, "Summer")
        self.assertEqual(res["farmer_id"], 99)
        self.assertEqual(res["risk_category"], "High Risk")
        self.assertEqual(res["calculated_payout"], 15000.0)
        self.assertEqual(res["adjusted_interest_rate"], 11.5)


if __name__ == "__main__":
    unittest.main()
