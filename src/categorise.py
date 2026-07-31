import pandas as pd

# --- Editable lookup dictionaries ---
FOOD_SHOPS = {
    "MCDONALD'S", "KOI", "STARBUCKS", "FAIRPRICE", "COLD STORAGE", "ELIJAH", "GUZMAN Y GOMEZ",
      "TIAN WANG DESSERTS", "MUNCHI", "JOLLIBEE", "WINGSTOP", "4FINGERS", "LUCKIN COFFEE", "WOK HEY",
      "SUBWAY", "POPEYES", "GOKOKU", "MCDONALDS", "YAYOI", "BURGER KING", "MARCHE", "NIKUIKU",
      "MOS BURGER", "TORI-Q", "CHAGEE", "SUSHIRO", "MAMMA MIA", "KOPITIAM", "KOUFU", "YOCHI",
      "CAI-CA", "MISTER DONUT", "I LOVE TAIMEI", "POTATO CORNER", "CHIMICHANGA", "IM ACAI", "YOSHINOYA",
      "MR COCONUT", "FOUR LEAVES", "BREADTALK", "PEPPER LUNCH", "MESSINA", "FLOCKCAFE", "SAIZERIYA"
      
}

SUBSCRIPTIONS = {
    "NETFLIX", "SPOTIFY", "YOUTUBE", "OPENAI",
}

CONVENIENCE = {
    "CHEERS", "7-ELEVEN", "SEVEN ELEVEN", "WATSONS", "GUARDIAN"
}

GROCERIES = {
    "NTUC", "SHENG SIONG", "GIANT", "COLD STORAGE"
}

COMMERCE = {
    "TAOBAO", "SHOPEE", "SCARLETT"
}

ACTIVITIES = {
    "GV", "SHAW THEATRES"
}

IGNORE_LIST = {

}

def matches_any(remainder: str, keywords: set) -> bool:
    return any(keyword in remainder for keyword in keywords)

def categorize_transaction_type(row: pd.Series) -> str:
    if pd.notna(row["Debit Amount"]):
        return "Debit"
    elif pd.notna(row["Credit Amount"]):
        return "Credit"
    else:
        return "Unknown"


def categorize_expense(supp_code: str) -> str:
    if pd.isna(supp_code):
        return "Miscellaneous"

    supp_code = supp_code.strip().upper()
    first_three = supp_code[:3]
    remainder = supp_code[3:].strip()
    first_word = remainder.split()[0] if remainder else ""

    if first_three == "IBG":
        return "IBG"
    elif first_word in {"BUS/MRT", "WWW.ANYWHEEL.SG"}:
        return "Transport"
    elif matches_any(remainder, FOOD_SHOPS):
        return "Food"
    elif "TOP-UP" in remainder:
        return "PayLah Top-up"
    elif "INCOMING PAYNOW" in remainder:
        return "Incoming PayNow"
    elif "PAYNOW TRANSFER" in remainder:
        return "PayNow Transfer"
    elif matches_any(remainder, SUBSCRIPTIONS):
        return "Subscriptions"
    elif matches_any(remainder, CONVENIENCE):
        return "Convenience"
    elif matches_any(remainder, GROCERIES):
        return "Groceries"
    elif matches_any(remainder, COMMERCE):
        return "Shopping"
    elif matches_any(remainder, ACTIVITIES):
        return "Activities"
    else:
        return "Miscellaneous"


def add_categories(df: pd.DataFrame) -> pd.DataFrame:
    df["transaction_type"] = df.apply(categorize_transaction_type, axis=1)
    df["category"] = df["Supplementary Code"].apply(categorize_expense)
    return df

def get_uncategorized(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["category"] == "Miscellaneous"]

def summarize_uncategorized(df: pd.DataFrame) -> pd.DataFrame:
    misc = get_uncategorized(df)
    misc = misc[~misc["Supplementary Code"].isin(IGNORE_LIST)]
    summary = misc["Supplementary Code"].value_counts().reset_index()
    summary.columns = ["Supplementary Code", "count"]
    return summary