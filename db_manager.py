"""
Database Architecture for Climate-Smart Agricultural Loan & Insurance Decision System
SQLite Database Handler (agri_finance.db)
"""

import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """
    Manages SQLite database operations for the Agricultural Finance & Insurance System.
    Handles table schema creation, data seeding, and full CRUD operations.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database manager with the given database path.
        If db_path is not specified, defaults to 'agri_finance.db' in the current working directory.
        """
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, "agri_finance.db")
        else:
            self.db_path = db_path

        self.create_tables()
        self.seed_initial_data()

    @contextmanager
    def get_connection(self):
        """
        Yields a SQLite connection configured with foreign keys enabled and row factory,
        ensuring the connection is closed after usage.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    def create_tables(self) -> None:
        """
        Creates the required database tables if they do not already exist:
        - Farmers
        - RiskAssessments
        - PayoutClaims
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Farmers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Farmers (
                    farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    region TEXT NOT NULL,
                    crop_type TEXT NOT NULL,
                    farm_size_acres REAL NOT NULL CHECK(farm_size_acres > 0),
                    loan_amount REAL NOT NULL CHECK(loan_amount >= 0),
                    interest_rate REAL NOT NULL CHECK(interest_rate >= 0),
                    credit_score INTEGER NOT NULL CHECK(credit_score BETWEEN 300 AND 900)
                );
            """)

            # 2. RiskAssessments Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RiskAssessments (
                    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    farmer_id INTEGER NOT NULL,
                    obs_temp REAL NOT NULL,
                    predicted_temp REAL NOT NULL,
                    season TEXT NOT NULL,
                    risk_score TEXT NOT NULL CHECK(risk_score IN ('Low', 'Medium', 'High', 'Low Risk', 'Medium Risk', 'High Risk')),
                    calculated_payout REAL NOT NULL CHECK(calculated_payout >= 0),
                    adjusted_interest_rate REAL NOT NULL CHECK(adjusted_interest_rate >= 0),
                    assessment_date TEXT NOT NULL,
                    FOREIGN KEY (farmer_id) REFERENCES Farmers(farmer_id) ON DELETE CASCADE
                );
            """)

            # 3. PayoutClaims Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PayoutClaims (
                    claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    farmer_id INTEGER NOT NULL,
                    claim_amount REAL NOT NULL CHECK(claim_amount >= 0),
                    status TEXT NOT NULL CHECK(status IN ('Pending', 'Approved', 'Disbursed')),
                    created_at TEXT NOT NULL,
                    assessment_id INTEGER,
                    FOREIGN KEY (farmer_id) REFERENCES Farmers(farmer_id) ON DELETE CASCADE,
                    FOREIGN KEY (assessment_id) REFERENCES RiskAssessments(assessment_id) ON DELETE SET NULL
                );
            """)

            # Indices for frequent queries
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_farmers_region ON Farmers(region);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessments_farmer ON RiskAssessments(farmer_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_farmer ON PayoutClaims(farmer_id);")

            conn.commit()

    def seed_initial_data(self) -> None:
        """
        Populate the database with realistic agricultural profiles on first launch
        if the Farmers table is currently empty.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Farmers;")
            count = cursor.fetchone()[0]

            if count == 0:
                initial_farmers = [
                    ("Rajesh Patil", "Vidarbha, Maharashtra", "Cotton", 12.5, 150000.0, 8.5, 720),
                    ("Sunita Devi", "Ludhiana, Punjab", "Wheat", 18.0, 220000.0, 7.8, 765),
                    ("Vikram Singh", "Bikaner, Rajasthan", "Bajra (Millet)", 25.0, 185000.0, 9.2, 680),
                    ("Anita Sharma", "Indore, Madhya Pradesh", "Soybean", 14.0, 140000.0, 8.0, 740),
                    ("Ramesh Kumar", "Varanasi, Uttar Pradesh", "Rice (Paddy)", 10.0, 120000.0, 8.5, 695),
                    ("Priya Nair", "Palakkad, Kerala", "Spices / Pepper", 6.5, 160000.0, 7.5, 785),
                    ("Amit Chakraborty", "Burdwan, West Bengal", "Rice (Paddy)", 11.0, 135000.0, 8.2, 710),
                    ("Dharmendra Patel", "Anand, Gujarat", "Groundnut", 15.0, 175000.0, 8.0, 730)
                ]

                cursor.executemany("""
                    INSERT INTO Farmers (name, region, crop_type, farm_size_acres, loan_amount, interest_rate, credit_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                """, initial_farmers)

                # Seed realistic historical assessments and claims in Rupees
                sample_records = [
                    (1, 41.5, 43.0, "Summer", "High Risk", 112500.0, 12.0, "2026-05-14 11:30:00", 112500.0, "Pending"),
                    (2, 28.2, 29.5, "Rabi", "Low Risk", 0.0, 6.8, "2026-02-10 09:15:00", 0.0, "Approved"),
                    (4, 35.8, 37.2, "Kharif", "Medium Risk", 49000.0, 9.5, "2026-08-22 14:00:00", 49000.0, "Approved"),
                    (5, 39.4, 40.8, "Summer", "High Risk", 90000.0, 12.0, "2026-06-05 16:45:00", 90000.0, "Disbursed"),
                ]

                for fid, ot, pt, season, risk, payout, adj_rate, dt, claim_amt, status in sample_records:
                    cursor.execute("""
                        INSERT INTO RiskAssessments (farmer_id, obs_temp, predicted_temp, season, risk_score, calculated_payout, adjusted_interest_rate, assessment_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """, (fid, ot, pt, season, risk, payout, adj_rate, dt))
                    asst_id = cursor.lastrowid

                    if claim_amt > 0:
                        cursor.execute("""
                            INSERT INTO PayoutClaims (farmer_id, claim_amount, status, created_at, assessment_id)
                            VALUES (?, ?, ?, ?, ?);
                        """, (fid, claim_amt, status, dt, asst_id))

                conn.commit()

    # -------------------------------------------------------------
    # Farmer CRUD Operations
    # -------------------------------------------------------------
    def add_farmer(
        self,
        name: str,
        region: str,
        crop_type: str,
        farm_size_acres: float,
        loan_amount: float,
        interest_rate: float,
        credit_score: int
    ) -> int:
        """Add a new farmer profile to the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Farmers (name, region, crop_type, farm_size_acres, loan_amount, interest_rate, credit_score)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (name.strip(), region.strip(), crop_type.strip(), farm_size_acres, loan_amount, interest_rate, credit_score))
            conn.commit()
            return cursor.lastrowid

    def update_farmer(
        self,
        farmer_id: int,
        name: str,
        region: str,
        crop_type: str,
        farm_size_acres: float,
        loan_amount: float,
        interest_rate: float,
        credit_score: int
    ) -> bool:
        """Update an existing farmer's profile."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Farmers
                SET name = ?, region = ?, crop_type = ?, farm_size_acres = ?, loan_amount = ?, interest_rate = ?, credit_score = ?
                WHERE farmer_id = ?;
            """, (name.strip(), region.strip(), crop_type.strip(), farm_size_acres, loan_amount, interest_rate, credit_score, farmer_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_farmer(self, farmer_id: int) -> bool:
        """Delete a farmer and cascades to related risk assessments and claims."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Farmers WHERE farmer_id = ?;", (farmer_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_farmer(self, farmer_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single farmer by their ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Farmers WHERE farmer_id = ?;", (farmer_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_farmers(self, search_query: Optional[str] = None, region_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all farmers with optional search and region filters."""
        query = "SELECT * FROM Farmers WHERE 1=1"
        params: List[Any] = []

        if search_query:
            query += " AND (name LIKE ? OR crop_type LIKE ?)"
            term = f"%{search_query.strip()}%"
            params.extend([term, term])

        if region_filter and region_filter != "All Regions":
            query += " AND region LIKE ?"
            params.append(f"%{region_filter.strip()}%")

        query += " ORDER BY farmer_id DESC;"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    # -------------------------------------------------------------
    # Risk Assessment Operations
    # -------------------------------------------------------------
    def add_risk_assessment(
        self,
        farmer_id: int,
        obs_temp: float,
        predicted_temp: float,
        season: str,
        risk_score: str,
        calculated_payout: float,
        adjusted_interest_rate: float,
        assessment_date: Optional[str] = None
    ) -> int:
        """Log a new climate risk assessment for a farmer."""
        if not assessment_date:
            assessment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO RiskAssessments (
                    farmer_id, obs_temp, predicted_temp, season, risk_score,
                    calculated_payout, adjusted_interest_rate, assessment_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                farmer_id, obs_temp, predicted_temp, season.strip(), risk_score.strip(),
                calculated_payout, adjusted_interest_rate, assessment_date
            ))
            conn.commit()
            return cursor.lastrowid

    def get_assessments(
        self,
        region_filter: Optional[str] = None,
        risk_filter: Optional[str] = None,
        name_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve assessments with joined farmer information."""
        query = """
            SELECT 
                r.assessment_id,
                r.farmer_id,
                f.name AS farmer_name,
                f.region,
                f.crop_type,
                f.loan_amount,
                f.interest_rate AS base_interest_rate,
                r.obs_temp,
                r.predicted_temp,
                r.season,
                r.risk_score,
                r.calculated_payout,
                r.adjusted_interest_rate,
                r.assessment_date
            FROM RiskAssessments r
            JOIN Farmers f ON r.farmer_id = f.farmer_id
            WHERE 1=1
        """
        params: List[Any] = []

        if region_filter and region_filter != "All Regions":
            query += " AND f.region LIKE ?"
            params.append(f"%{region_filter.strip()}%")

        if risk_filter and risk_filter != "All Risk Levels":
            query += " AND r.risk_score LIKE ?"
            params.append(f"%{risk_filter.strip()}%")

        if name_filter:
            query += " AND f.name LIKE ?"
            params.append(f"%{name_filter.strip()}%")

        query += " ORDER BY r.assessment_id DESC;"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    # -------------------------------------------------------------
    # Payout Claims Operations
    # -------------------------------------------------------------
    def add_payout_claim(
        self,
        farmer_id: int,
        claim_amount: float,
        status: str = "Pending",
        assessment_id: Optional[int] = None,
        created_at: Optional[str] = None
    ) -> int:
        """Create a new insurance payout claim."""
        if not created_at:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PayoutClaims (farmer_id, claim_amount, status, created_at, assessment_id)
                VALUES (?, ?, ?, ?, ?);
            """, (farmer_id, claim_amount, status, created_at, assessment_id))
            conn.commit()
            return cursor.lastrowid

    def update_claim_status(self, claim_id: int, new_status: str) -> bool:
        """Update status of a payout claim (Pending, Approved, Disbursed)."""
        valid_statuses = ("Pending", "Approved", "Disbursed")
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of {valid_statuses}")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE PayoutClaims
                SET status = ?
                WHERE claim_id = ?;
            """, (new_status, claim_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_claims_ledger(
        self,
        region_filter: Optional[str] = None,
        risk_filter: Optional[str] = None,
        name_filter: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Unified ledger query joining Assessments, Claims, and Farmers.
        """
        query = """
            SELECT 
                r.assessment_id,
                COALESCE(c.claim_id, 0) AS claim_id,
                r.assessment_date,
                f.farmer_id,
                f.name AS farmer_name,
                f.region,
                f.crop_type,
                f.loan_amount,
                f.interest_rate AS base_interest_rate,
                r.obs_temp,
                r.predicted_temp,
                r.season,
                r.risk_score,
                r.calculated_payout,
                r.adjusted_interest_rate,
                COALESCE(c.status, CASE WHEN r.calculated_payout > 0 THEN 'Pending' ELSE 'N/A' END) AS claim_status
            FROM RiskAssessments r
            JOIN Farmers f ON r.farmer_id = f.farmer_id
            LEFT JOIN PayoutClaims c ON r.assessment_id = c.assessment_id
            WHERE 1=1
        """
        params: List[Any] = []

        if region_filter and region_filter != "All Regions":
            query += " AND f.region LIKE ?"
            params.append(f"%{region_filter.strip()}%")

        if risk_filter and risk_filter != "All Risk Levels":
            query += " AND r.risk_score LIKE ?"
            params.append(f"%{risk_filter.strip()}%")

        if name_filter:
            query += " AND f.name LIKE ?"
            params.append(f"%{name_filter.strip()}%")

        if status_filter and status_filter != "All Statuses":
            query += " AND c.status = ?"
            params.append(status_filter.strip())

        query += " ORDER BY r.assessment_id DESC;"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    # -------------------------------------------------------------
    # Financial KPI Aggregation
    # -------------------------------------------------------------
    def get_financial_kpis(self) -> Dict[str, Any]:
        """
        Calculates aggregate key performance indicators:
        - Total Loans Active ($)
        - Total Estimated Payout Exposure ($)
        - High Risk Farmer Count
        - Total Disbursed Claims ($)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total Active Loans
            cursor.execute("SELECT COALESCE(SUM(loan_amount), 0.0) FROM Farmers;")
            total_loans = cursor.fetchone()[0]

            # Total Estimated Payout Exposure (sum of calculated payouts across assessments)
            cursor.execute("SELECT COALESCE(SUM(calculated_payout), 0.0) FROM RiskAssessments;")
            total_payout_exposure = cursor.fetchone()[0]

            # High Risk Farmer Count (distinct farmers with at least one High Risk assessment)
            cursor.execute("""
                SELECT COUNT(DISTINCT farmer_id) 
                FROM RiskAssessments 
                WHERE risk_score LIKE '%High%';
            """)
            high_risk_count = cursor.fetchone()[0]

            # Total Disbursed Claims
            cursor.execute("""
                SELECT COALESCE(SUM(claim_amount), 0.0) 
                FROM PayoutClaims 
                WHERE status = 'Disbursed';
            """)
            total_disbursed = cursor.fetchone()[0]

            # Total Farmers
            cursor.execute("SELECT COUNT(*) FROM Farmers;")
            farmer_count = cursor.fetchone()[0]

            return {
                "total_loans_active": round(total_loans, 2),
                "total_payout_exposure": round(total_payout_exposure, 2),
                "high_risk_farmer_count": high_risk_count,
                "total_disbursed": round(total_disbursed, 2),
                "total_farmers": farmer_count
            }
