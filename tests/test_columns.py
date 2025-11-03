import os
import sys
import pandas as pd

# Ensure project root is on sys.path for importing utils package during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.columns import normalize_columns, find_column, detect_columns


def test_normalize_and_find_detect():
    # Simulate messy headers with BOM and spaces
    raw_cols = ["\ufeffTaluk name ", " Total Agricultural Land Holders _Total_Area_Total "]
    df = pd.DataFrame(columns=raw_cols)

    df = normalize_columns(df)
    # After normalization, whitespace and BOM should be removed
    assert "Taluk name" in df.columns
    assert "Total Agricultural Land Holders _Total_Area_Total" in df.columns

    taluk, area = detect_columns(df)
    # taluk should contain 'taluk' keyword and area should contain either 'area' or 'total'
    assert "taluk" in taluk.lower()
    assert ("area" in area.lower()) or ("total" in area.lower())
