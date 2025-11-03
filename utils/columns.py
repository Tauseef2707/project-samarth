import pandas as pd
from typing import List, Optional, Tuple


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and BOM from column names in-place and return df."""
    new_cols = []
    for c in df.columns:
        if isinstance(c, str):
            nc = c.strip().replace('\ufeff', '')
        else:
            nc = c
        new_cols.append(nc)
    df.columns = new_cols
    return df


def find_column(cols: List[str], keywords: List[str]) -> Optional[str]:
    """Return the first column name that contains all keywords (case-insensitive)."""
    kws = [k.lower() for k in keywords]
    for col in cols:
        if not isinstance(col, str):
            continue
        low = col.lower()
        if all(k in low for k in kws):
            return col
    return None


def detect_columns(df: pd.DataFrame) -> Tuple[str, str]:
    """Detect a taluk/category column and an area/numeric column from the DataFrame.

    Returns (taluk_col, area_col). Uses simple keyword matching with sensible fallbacks.
    """
    cols = df.columns.tolist()
    taluk = find_column(cols, ["taluk"]) or find_column(cols, ["name"]) or cols[0]
    area = find_column(cols, ["area"]) or find_column(cols, ["total"]) or cols[-1]
    return taluk, area
