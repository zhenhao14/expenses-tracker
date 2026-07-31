# activate venv before running the script to access the python kernel
# source .venv/bin/activate
# run the script with python src/etl.py


import pandas as pd
from pathlib import Path
from datetime import datetime
from categorise import add_categories

RAW_DIR = Path(__file__).resolve().parent.parent/"data"/"raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent/"data"/"processed"

# create function to read_csv each raw file
def extract(filepath: Path) -> pd.DataFrame:
    # read csv file starting from row 8 onwards
    return pd.read_csv(filepath, header = 8)

# create function to parse the raw file names
def transform(df: pd.DataFrame, filepath: Path) -> pd.DataFrame:
    # Parase month/year from filename
    stem = filepath.stem
    month_str, year_str = stem.split("_")

    df["source_month"] = month_str.title()
    df["source_year"] = int(year_str)

    # drop columns
    df = df.drop(['Statement Code', 'Description', 'Additional Reference', 'Status'], axis = 'columns')
    return df

# create function that loops and transforms all the raw data
# and then concatenate and save to PROCESSED_DIR

# sort by month first
def sort_key(filepath: Path):
    stem = filepath.stem
    month_str, year_str = stem.split("_")
    month_num = datetime.strptime(month_str, "%b").month
    year_num = int(year_str)
    return (year_num, month_num)

def run_etl() -> pd.DataFrame:
    all_dfs = []
    for filepath in sorted(RAW_DIR.glob("*.csv"), key = sort_key):
        df = extract(filepath)
        df = transform(df, filepath)
        all_dfs.append(df)
    combined = pd.concat(all_dfs, ignore_index = True)
    combined = add_categories(combined)
    return combined

def load (df: pd.DataFrame, filename = "all_expenses.csv"):
    PROCESSED_DIR.mkdir(parents = True, exist_ok = True)
    df.to_csv(PROCESSED_DIR / filename, index = False)

if __name__ == "__main__":
    combined = run_etl()
    load(combined)
    print(f"Processed {len(combined)} rows across all files.")