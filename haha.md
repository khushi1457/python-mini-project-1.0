# AGRO-SHIELD AI: Climate-Smart Agricultural Loan & Insurance Decision System

A complete, production-grade Python desktop application integrating **Climate Intelligence** (heatwave and thermal stress analytics) with **Agricultural Microfinance** and **Parametric Insurance Risk Management**.

Built with **Python 3**, **Tkinter (`ttk`)**, **SQLite**, and **Scikit-Learn (`RandomForestClassifier`)**.

---

## 🏛️ Architecture Overview

The system is engineered using a clean **3-Tier Modular Architecture**:

```
┌──────────────────────────────────────────────────────────────┐
│                    PRESENTATION TIER                         │
│   gui.py  •  Modern Tkinter (ttk) Desktop Application       │
│   - Tab 1: Farmer Profile Manager (CRUD, Treeview, Search)   │
│   - Tab 2: AI Risk Assessment & Dynamic Underwriting         │
│   - Tab 3: Financial Ledger, Claims & Portfolio Exposure     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                   BUSINESS & AI LOGIC TIER                   │
│   risk_engine.py  •  AgriRiskEngine                          │
│   - Scikit-Learn RandomForestClassifier (>94% Accuracy)      │
│   - Agro-thermal physics simulation (Heatwave & Humidity)    │
│   - Parametric Insurance Payout Calculator                   │
│   - Dynamic Climate Interest Rate Adjustment Engine          │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     DATA ACCESS TIER                         │
│   db_manager.py  •  DatabaseManager (SQLite)                 │
│   - SQLite: agri_finance.db                                  │
│   - Relational Tables: Farmers, RiskAssessments, PayoutClaims│
│   - Auto-seeding of 8 realistic agricultural profiles        │
│   - Portfolio KPI Aggregations and Financial Ledger Queries  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | Desktop application launcher and entry point (supports standard GUI and `--headless-check` mode). |
| `gui.py` | Modern desktop UI implementation using `tkinter.ttk` (custom theme, cards, badges, treeviews, and dialogs). |
| `risk_engine.py` | Machine Learning and financial logic layer (`RandomForestClassifier`, thermal physics, dynamic interest, insurance payouts). |
| `db_manager.py` | SQLite database access layer (`agri_finance.db`, table creation, CRUD, cascading foreign keys, KPI aggregations). |
| `tests.py` | Comprehensive test suite covering database operations, ML classification accuracy, financial formulas, and workflow. |
| `agri_finance.db` | Auto-created SQLite database file. |

---

## ⚙️ Financial & Machine Learning Rules

### 1. Machine Learning Model (`RandomForestClassifier`)
- **Features**:
  - `observed_temp` (°C) — Ambient observed maximum temperature.
  - `forecast_max_temp` (°C) — Predicted heatwave peak temperature.
  - `humidity` (%) — Relative atmospheric humidity.
  - `season_encoded` — Crop season (`0 = Kharif/Monsoon`, `1 = Rabi/Winter`, `2 = Summer/Zaid`).
- **Target**:
  - `Low Risk` (Optimal crop vegetative conditions).
  - `Medium Risk` (Elevated thermal stress / evaporative demand).
  - `High Risk` (Critical heatwave / terminal heat / severe yield failure).

### 2. Parametric Insurance Payout Rule
Payout is calculated automatically based on the classified climate risk level:
- **Low Risk**: **0%** of principal loan ($0.00).
- **Medium Risk**: **35%** of principal loan.
- **High Risk**: **75%** of principal loan (automatic claim generation).

### 3. Dynamic Loan Interest Adjustment Rule
Adjusts the farmer's base loan interest rate based on real-time climate vulnerability:
- **Low Risk**: Base Rate **- 1.0%** (Resilience incentive discount).
- **Medium Risk**: Base Rate **+ 1.5%** (Climate stress reserve premium).
- **High Risk**: Base Rate **+ 3.5%** (Hazard risk rate & loan restructuring flag).

---

## 🚀 How to Run the Application

### 1. Launch the Desktop GUI
Run the main launcher:
```bash
python3 main.py
```

### 2. Run Automated Verification / Test Suite
Run the unit and integration tests:
```bash
python3 tests.py
```

Run headless startup verification:
```bash
python3 main.py --headless-check
```

---

## 🖥️ User Interface Guide

### Tab 1: Farmer Profile Manager
- Register new farmers or update existing profiles with fields: Name, Region, Crop Type, Farm Size (Acres), Loan Amount ($), Base Interest Rate (%), and Credit Score (300-900).
- Filter and search the database by Name, Crop, or Region.
- Click any table row to load the farmer's details into the editing form.

### Tab 2: Climate Risk & Insurance Engine
- Select any registered farmer from the dropdown to preview their financial profile.
- Enter meteorological metrics (Observed Temp, Forecast Temp, Humidity, and Season) or click a **Simulation Preset** (e.g., *Severe Heatwave 43°C*, *Moderate Stress 35°C*, *Optimal Conditions 26°C*).
- Click **Run AI Risk Assessment & Compute Payout**:
  - Predicts risk category and confidence breakdown.
  - Calculates insurance payout and dynamic adjusted interest rate.
  - Automatically writes results to SQLite (`RiskAssessments` and `PayoutClaims`).
  - Displays color-coded risk badge (Green = Low, Yellow = Medium, Red = High).

### Tab 3: Financial Ledger & Claims Center
- Monitor high-level KPI cards:
  - **Total Active Loans Portfolio ($)**
  - **Total Estimated Payout Exposure ($)**
  - **High Risk Farmers Count**
  - **Total Claims Disbursed ($)**
- Filter historical risk ledger entries by Region, Risk Level, Claim Status, or Farmer Name.
- Select a claim row and click **Approve Claim** or **Disburse Payout**.
- Export the current ledger view to a timestamped CSV report (**Export CSV**).
