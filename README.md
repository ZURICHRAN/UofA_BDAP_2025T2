# Adelaide Housing & Crime Data Analysis

This repository analyzes **housing affordability** and **crime trends** in South Australia (Adelaide focus) using public datasets (ABS, SAPOL, etc.). It contains two standalone analysis scripts plus optional notebooks and outputs.

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
├─ dwellings_analysis.py             # Housing/dwellings ETL + metrics + visualizations
├─ crime_model_data.csv              # (Optional) aggregated crime dataset for modeling
├─ Modeling.ipynb                    # (Optional) experiments/models
└─ README.md
```

## Datasets

* **Used**

  * `Total Value of Dwellings/643201.xlsx` (ABS, sheet `Data1`)
    – Dwelling stock value, dwelling counts, and ownership splits for South Australia.
  * `Crime Statistics/2022-23_data_sa_crime.csv`, `2023-24_data_sa_crime.csv`, `2024-25_data_sa_crime.csv` (SAPOL)
    – Contains `Reported Date`, `Suburb`, `Offence count`, and offence level descriptors.

* **Present but not used (kept for future work)**

  * `Census Community Profiles/` – Demographics, income, employment, etc.
  * `Private Rental Report/` – Rental market levels/pressure indicators.


## How to Run

### 1) Housing / Dwellings Analysis

Processes ABS dwelling stock value/counts and computes derived metrics.

```bash
python dwellings_analysis.py
```

**Inputs**

* `Total Value of Dwellings/643201.xlsx` (expects sheet `Data1`).

**What it does**

* Cleans and renames columns (first column → `Date`).
* Converts monthly dates, handles unit scales.
* Computes `Average Price (SA)` = total value / dwelling count.
* Plots:

  * Total dwelling stock value (SA)
  * Average dwelling price (SA)
  * YoY growth of average price
  * Dwelling count vs average price (scatter)
  * Value by ownership type (Households / Non-Households / All sectors)

**Outputs**

* Clean CSV: `Total Value of Dwellings/643201_cleaned_data.csv`
* Figures in `Visualizations/`

### 2) Crime Analysis

Merges multiple SAPOL yearly CSVs and produces trend/distribution charts.

```bash
python crime_analysis.py
```

**Inputs**

* `Crime Statistics/2022-23_data_sa_crime.csv`
* `Crime Statistics/2023-24_data_sa_crime.csv`
* `Crime Statistics/2024-25_data_sa_crime.csv`

**What it does**

* Concatenates annual files, standardizes column names:

  * `Offence Level 1/2/3`, `Offence Count`, `Suburb`, parses `Reported Date` (`dayfirst=True`) and creates `Month`.
* Visualizations:

  * Monthly total crime trend (2022–2025)
  * Top-10 offence types (Level 1)
  * Top-10 suburbs by total offences
  * Heatmap: suburb × Level 1 (log-scaled)
  * Offence Level 1 distribution (pie)
  * Top-10 offence types (Level 2)

**Outputs**

* Figures in `Visualizations/`
* (Optional) aggregated tables to `Outputs/` or `crime_model_data.csv` if enabled in code/notebook.

## Reproducibility Checklist

1. Place raw data in the folders shown above (keep file names as referenced by the scripts).
2. Create a virtual environment and install dependencies.
3. Run `python dwellings_analysis.py` and `python crime_analysis.py`.
4. Inspect generated figures in `Visualizations/` and any CSVs in their respective folders.

## Assumptions & Notes

* **Date parsing**: crime data uses `dayfirst=True`. If your source switches to ISO format, adjust parsing accordingly.
* **Unit handling**: dwelling value/count columns in ABS 643201 use “millions”/“thousands” scales; the script converts them so average price is in AUD.
* **Missing/irregular rows**: the scripts coerce unparseable dates to `NaT` and skip them in plots.

## Future Work

* Integrate **Census Community Profiles** (income, employment, household structure).
* Integrate **Private Rental Report** (rent levels, vacancy, rental stress).
* Build a composite **Housing Affordability Index** and add forecasting/causal analysis.

## Quick Commands

```bash
# Regenerate all figures
python dwellings_analysis.py && python crime_analysis.py

# Open the notebook
jupyter lab
```
