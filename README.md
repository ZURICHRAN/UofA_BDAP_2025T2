# Adelaide Housing & Crime Data Analysis

This repository analyzes **housing affordability** and **crime trends** in South Australia (Adelaide focus) using public datasets (ABS, SAPOL, etc.). It contains two standalone analysis scripts plus an optional modeling notebook.

## Repository Structure

```
.
├─ Census Community Profiles/        # ABS Census profile tables (not used yet)
├─ Crime Statistics/                 # SAPOL crime CSVs (used by crime_analysis.py)
├─ Outputs/                          # Optional: exported tables from scripts/notebooks
├─ Private Rental Report/            # Rental market data (not used yet)
├─ Total Value of Dwellings/         # ABS 643201.xlsx (used by dwellings_analysis.py)
├─ Visualizations/                   # Figures written by scripts
├─ crime_analysis.py                 # Crime ETL + EDA + visualizations
├─ dwellings_analysis.py             # Dwelling value/count ETL + metrics + visualizations
├─ crime_model_data.csv              # (Optional) aggregated crime dataset for modeling
├─ Modeling.ipynb                    # (Optional) experiments/models
└─ README.md
```

---

## Datasets

### Used

* **Total Value of Dwellings/**

  * `643201.xlsx` (ABS, sheet `Data1`): dwelling stock **value**, **count**, and **ownership** for South Australia.
* **Crime Statistics/**

  * `2022-23_data_sa_crime.csv`, `2023-24_data_sa_crime.csv`, `2024-25_data_sa_crime.csv` (SAPOL):
    columns include `Reported Date`, `Suburb`, `Offence count`, `Offence Level 1/2/3 Description`.

### Present but not used (kept for future work)

* **Census Community Profiles/** – demographics, income, employment, household structure.
* **Private Rental Report/** – rental levels, vacancy, rental stress indicators.

---

## How to Run

### 1) Housing / Dwellings Analysis

Processes ABS dwelling stock value/counts and computes derived metrics.

```bash
# from repo root
python dwellings_analysis.py
```

**Inputs**

* `Total Value of Dwellings/643201.xlsx` (expects sheet `Data1`).

**What it does**

* Cleans/renames columns (first column → `Date`) and parses monthly dates.
* Computes `Average Price (SA)` = total value / dwelling count (units handled in script).
* Produces figures:

  * Total dwelling stock value (SA)
  * Average dwelling price (SA)
  * YoY growth of average price
  * Dwelling count vs average price (scatter)
  * Value by ownership type (Households / Non-Households / All sectors)

**Outputs**

* `Total Value of Dwellings/643201_cleaned_data.csv`
* Figures in `Visualizations/`

---

### 2) Crime Analysis

Merges multiple SAPOL yearly CSVs and produces trend/distribution charts.

```bash
# from repo root
python crime_analysis.py
```

**Inputs**

* `Crime Statistics/2022-23_data_sa_crime.csv`
* `Crime Statistics/2023-24_data_sa_crime.csv`
* `Crime Statistics/2024-25_data_sa_crime.csv`

**What it does**

* Concatenates annual files; standardizes column names:

  * `Offence Level 1/2/3`, `Offence Count`, `Suburb`
* Parses `Reported Date` (day-first) and creates `Month`.
* Produces figures:

  * Monthly total crime trend (2022–2025)
  * Top-10 offence types (Level 1)
  * Top-10 suburbs by total offences
  * Heatmap: suburb × Level 1 (log-scaled values)
  * Offence Level 1 distribution (pie)
  * Top-10 offence types (Level 2)

**Outputs**

* Figures in `Visualizations/`
* (Optional) aggregated tables to `Outputs/` or `crime_model_data.csv` if enabled in code/notebook.

---

## Modeling Notebook (`Modeling.ipynb`)

Notebook for **experiments and modeling** (e.g., forecasting/diagnosing crime and linking to housing indicators).

**Inputs**

* **Primary**: `crime_model_data.csv` (aggregated modeling dataset).
  If missing, generate your own aggregation from `crime_analysis.py` or your pipeline.
* **Optional**: outputs from `dwellings_analysis.py` (e.g., average dwelling price) if you plan to merge housing features.

**How to open**

```bash
# in repo root (with your preferred Jupyter setup)
jupyter lab    # or: jupyter notebook
# then open Modeling.ipynb
```

**Suggested workflow**

1. Data preparation: select scope, time-based split (hold out recent months), create lag/rolling/calendar features.
2. Baselines: naive seasonal/mean; simple GLM/linear models.
3. Optional ML: tree/boosting models if needed.
4. Evaluation: MAE/RMSE (and MAPE if appropriate) on the hold-out period.
5. Diagnostics: residual plots; careful interpretation of feature importances.
6. Export: predictions/metrics to `Outputs/` for the report.

**Starter cell (optional)**

```python
import os, pandas as pd

# Load modeling data
if os.path.exists("crime_model_data.csv"):
    df = pd.read_csv("crime_model_data.csv")
else:
    raise FileNotFoundError("Place or generate crime_model_data.csv in the repo root.")

# Parse common time columns
for c in ("Month","Date"):
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors="coerce")

print(df.shape)
df.head()
```

---

## Reproducibility Checklist

1. Place raw data in the folders shown above with the expected filenames.
2. Run `python dwellings_analysis.py` and `python crime_analysis.py`.
3. Inspect generated figures in `Visualizations/` and any CSVs written alongside inputs or in `Outputs/`.
4. Open `Modeling.ipynb` to reproduce/extend modeling steps.

---

## Assumptions & Notes

* **Date parsing**: crime data uses day-first date strings; any unparseable rows become `NaT` and are skipped by plots.
* **Unit handling**: ABS dwelling value/count columns are in millions/thousands; scripts scale them so average price is in AUD.
* **Folder case**: ensure consistency between script paths and the on-disk folder (`Visualizations/` recommended).

---

## Future Work

* Integrate **Census Community Profiles** (income, employment, household structure).
* Integrate **Private Rental Report** (rent levels, vacancies, rental stress).
* Build a composite **Housing Affordability Index** and add forecasting/causal analyses.

---

## Quick Commands

```bash
# Regenerate all figures
python dwellings_analysis.py && python crime_analysis.py

# Open the notebook
jupyter lab
```
