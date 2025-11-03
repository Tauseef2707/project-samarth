# ==========================================================
# 🌾 PROJECT SAMARTH — Intelligent Q&A System (No spaCy)
# ==========================================================
# Author: Tauseef Hussain
# Description:
# This program creates an intelligent Q&A system that combines
# agricultural and rainfall data from data.gov.in-like datasets
# using keyword-based analysis and visualization.
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ----------------------------------------------------------
# SECTION 1: Data Loading
# ----------------------------------------------------------
st.title("🌾 Project Samarth — Agricultural and Climate Q&A System")
st.markdown("### Designed by **Tauseef Hussain**")
st.write(
    "This system analyzes agriculture and rainfall data to answer natural language questions and visualize trends.")

# Load data
st.subheader("📂 Data Loading Section")

rainfall_path = st.text_input("Enter Rainfall CSV File Path:", "RS_Session_258_AU_210_1.csv")
agriculture_path = st.text_input("Enter Agriculture CSV File Path:", "Total_agriculture_land_holders_Total.csv")

import os
st.write("Current working directory:", os.getcwd())
try:
    rainfall_df = pd.read_csv(rainfall_path)
    st.success("✅ Rainfall Data Loaded Successfully!")
    st.dataframe(rainfall_df.head())
except Exception as e:
    st.error(f"⚠️ Error loading rainfall data: {e}")
    rainfall_df = None

try:
    agriculture_df = pd.read_csv(agriculture_path)
    st.success("✅ Agriculture Data Loaded Successfully!")
    st.dataframe(agriculture_df.head())
except Exception as e:
    st.error(f"⚠️ Error loading agriculture data: {e}")
    agriculture_df = None

# If agriculture data loaded, normalize column names to avoid case/whitespace/BOM issues
def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # strip whitespace and BOM, keep original case except trimmed
    new_cols = []
    for c in df.columns:
        if isinstance(c, str):
            nc = c.strip().replace('\ufeff', '')
        else:
            nc = c
        new_cols.append(nc)
    df.columns = new_cols
    return df

def find_column(cols, keywords):
    """Return the first column name that contains all keywords (case-insensitive)."""
    kws = [k.lower() for k in keywords]
    for col in cols:
        if not isinstance(col, str):
            continue
        low = col.lower()
        if all(k in low for k in kws):
            return col
    return None


TALUK_COL = None
AREA_COL = None

if agriculture_df is not None:
    agriculture_df = _normalize_columns(agriculture_df)
    # detect key columns for later use
    TALUK_COL = find_column(agriculture_df.columns.tolist(), ["taluk"]) or find_column(agriculture_df.columns.tolist(), ["name"]) or agriculture_df.columns[0]
    AREA_COL = find_column(agriculture_df.columns.tolist(), ["area"]) or find_column(agriculture_df.columns.tolist(), ["total"]) or agriculture_df.columns[-1]
    # show detected columns
    st.write(f"Detected taluk column: '{TALUK_COL}', area column: '{AREA_COL}'")

# ----------------------------------------------------------
# SECTION 2: Data Summary
# ----------------------------------------------------------
if rainfall_df is not None:
    st.subheader("📊 Rainfall Data Summary")
    st.write(rainfall_df.describe())

if agriculture_df is not None:
    st.subheader("🌱 Agriculture Data Summary")
    st.write(agriculture_df.describe())

# ----------------------------------------------------------
# SECTION 3: Visualization
# ----------------------------------------------------------
st.subheader("📈 Visualization")

if rainfall_df is not None:
    st.write("### Annual Rainfall Trend")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=rainfall_df, x="Year", y="Annual", marker='o', ax=ax)
    ax.set_title("Annual Rainfall Over Years", fontsize=14)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual Rainfall (mm)")
    st.pyplot(fig)
    if agriculture_df is not None:
        st.write("📋 Columns in agriculture_df:", agriculture_df.columns.tolist())
        st.write("Columns in agriculture_df:", agriculture_df.columns.tolist())
        # Take top 10 taluks by detected area column (convert to numeric safely)
        st.write("### 🌾 Top Agricultural Land Holders")

        # Let user choose columns with sensible defaults (detected names)
        cols = agriculture_df.columns.tolist()
        default_x_idx = cols.index(TALUK_COL) if TALUK_COL in cols else 0
        default_y_idx = cols.index(AREA_COL) if AREA_COL in cols else max(0, len(cols) - 1)
        x_col = st.selectbox("Select category column (x):", options=cols, index=default_x_idx)
        y_col = st.selectbox("Select numeric column (y):", options=cols, index=default_y_idx)

        if x_col not in agriculture_df.columns or y_col not in agriculture_df.columns:
            st.error("Could not find required columns for plotting. See detected columns above.")
        else:
            # Convert y column to numeric (coerce errors to NaN) and sort
            agriculture_df['_y_numeric'] = pd.to_numeric(agriculture_df[y_col], errors='coerce').fillna(0)
            top_taluks = agriculture_df.sort_values('_y_numeric', ascending=False).head(10)

            # Show available columns for debugging
            st.write("📋 Columns available in top_taluks DataFrame:")
            st.write(top_taluks.columns.tolist())

            st.write(f"Using x column: '{x_col}' and y column: '{y_col}'")

            # Create bar chart safely
            fig, ax = plt.subplots(figsize=(10, 6))
            try:
                sns.barplot(x=x_col, y='_y_numeric', data=top_taluks, ax=ax)
            except Exception as e:
                st.error(f"Could not create barplot: {e}")
                st.write("Available columns:", top_taluks.columns.tolist())
                raise
            ax.set_xlabel(x_col)
            ax.set_ylabel(f"{y_col} (numeric)")
            ax.set_title("Top Agricultural Land Holders by Taluk")
            # Rotate long x labels for readability
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            fig.tight_layout()

            st.pyplot(fig)


    # Use correct column names (will fix after we see them)
    # sns.barplot(data=top_taluks, x="Taluk name", y=agriculture_df.columns[-1], palette="viridis", ax=ax)

# ----------------------------------------------------------
# SECTION 4: Keyword-based Q&A
# ----------------------------------------------------------
st.subheader("💬 Ask a Question")

user_query = st.text_input("Enter your question about agriculture or rainfall:")


def answer_query(query):
    query = query.lower()
    response = ""
    source = ""

    # Rainfall comparison
    if "rainfall" in query and "compare" in query:
        if rainfall_df is not None:
            avg_rain = rainfall_df["Annual"].mean()
            response = f"🌧️ The average annual rainfall across available years is **{avg_rain:.2f} mm**."
            source = "Source: Rainfall dataset"
        else:
            response = "⚠️ Rainfall data not available."

    # Top crop or area-related question
    elif "agriculture" in query or "land" in query or "top" in query:
        if agriculture_df is not None:
            # Use detected columns for answer
            x_col = TALUK_COL
            y_col = AREA_COL
            try:
                y_numeric = pd.to_numeric(agriculture_df[y_col], errors='coerce').fillna(0)
                idx = y_numeric.idxmax()
                top_taluk = agriculture_df.loc[idx]
                taluk_name = top_taluk.get(x_col, "(unknown)")
                taluk_area = float(y_numeric.loc[idx])
                response = (f"🌾 The taluk with the highest total agricultural area is "
                            f"**{taluk_name}**, "
                            f"covering **{taluk_area:.2f} hectares.**")
                source = "Source: Agricultural dataset"
            except Exception:
                response = "⚠️ Could not determine top taluk from the agricultural dataset."
                source = "Source: Agricultural dataset"
        else:
            response = "⚠️ Agricultural data not available."

    # Trend analysis
    elif "trend" in query or "over years" in query:
        if rainfall_df is not None:
            trend = rainfall_df.groupby("Year")["Annual"].mean()
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.lineplot(x=trend.index, y=trend.values, marker="o", ax=ax)
            ax.set_title("Rainfall Trend Over Years")
            st.pyplot(fig)
            response = "📈 Displaying rainfall trend over years."
            source = "Source: Rainfall dataset"
        else:
            response = "⚠️ No data available for trend analysis."

    # Default fallback
    else:
        response = "🤖 Sorry, I couldn’t understand your question. Try keywords like 'compare rainfall', 'top taluk', or 'trend over years'."

    return response, source


if user_query:
    answer, citation = answer_query(user_query)
    st.success(answer)
    if citation:
        st.caption(f"📘 {citation}")

# ----------------------------------------------------------
# SECTION 5: Closing Summary
# ----------------------------------------------------------
st.markdown("---")
st.markdown("✅ **Analysis Completed Successfully — Project Samarth Prototype**")
st.markdown("© 2025 | Designed & Developed by **Tauseef Hussain**")

