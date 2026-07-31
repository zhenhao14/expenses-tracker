# Expenses Tracker

A pipeline that extracts, cleans, categorizes, and visualizes monthly bank statement data.

## Initial Setup

Before running anything for the first time, set up the project structure and environment.

### 1. Create the data folders

This project expects the following folder structure. If they don't already exist, create them:

```bash
mkdir -p data/raw data/processed
```

- **`data/raw/`** — place your raw, unedited monthly bank statement CSVs here.
- **`data/processed/`** — the ETL script will automatically generate `all_expenses.csv` here. You don't need to create this file manually; running the ETL script for the first time will create it.

> **Note:** These folders are excluded from git via `.gitignore` since they contain personal financial data. If you're cloning this repo fresh, these folders will be empty (or missing) — you'll need to add your own raw CSVs before running the pipeline.

### 2. Set up the virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

---

## Monthly Workflow

Follow these steps each time you want to add a new month of data and refresh the dashboard.

### 1. Activate the venv

`cd` into your project folder, then run:

```bash
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

Your terminal prompt should show `(.venv)` at the start once it's active. Everything below assumes this is done first.

If this is the first time running the project, install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Add the new month's raw CSV

Save the new bank statement CSV into `data/raw/`, using the same naming convention as your existing files (e.g. `aug_2026.csv`) so the filename parsing and sorting logic in `etl.py` still works correctly.

### 3. Run the ETL script

```bash
python src/etl.py
```

(or `python -m src.etl`, depending on how your imports are set up)

Since categorization is baked into `run_etl()`, this single command extracts, cleans, categorizes, and saves the fully processed file to `data/processed/all_expenses.csv` — dashboard-ready with no extra steps.

### 4. Check for uncategorized transactions

Open `notebooks/EDA.ipynb`, then load `data/processed/all_expenses.csv` and call `summarize_uncategorized()` to check for any new merchant codes that fell into `'Miscellaneous'`.

### 5. Fix any gaps, then rerun the ETL

If any new codes show up with a meaningful count, open `src/categorize.py` and add the keyword to the right dictionary (`FOOD_SHOPS`, `SUBSCRIPTIONS`, `CONVENIENCE`, etc.), or to `IGNORE_LIST` if it's a genuine one-off.

Then rerun the ETL script from the terminal again, since it needs to regenerate the processed file with the fix applied:

```bash
python src/etl.py
```

### 6. Recheck until clean

Reload the CSV in the notebook and call `summarize_uncategorized()` again to confirm the fix worked. Repeat the fix → rerun → recheck loop until the list only shows genuine one-offs or is empty.

### 7. Launch the dashboard

Once you're happy with the categorization, run:

```bash
streamlit run dashboard.py
```

It reads directly from the now up-to-date `data/processed/all_expenses.csv`, so you'll immediately see the new month available in the dropdown with correctly categorized bars.