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

rainfall_path = st.text_input("Enter Rainfall CSV File Path:", r"C:\Users\Admin\Downloads\RS_Session_258_AU_210_1.csv")
agriculture_path = st.text_input("Enter Agriculture CSV File Path:",
                                 r"C:\Users\Admin\Downloads\Total_agriculture_land_holders_Total.csv")

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
    st.write("### Top Agricultural Land Holders")
    top_taluks = agriculture_df.nlargest(10, agriculture_df.columns[-1])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_taluks, x="Taluk name", y=agriculture_df.columns[-1], palette="viridis", ax=ax)
    plt.xticks(rotation=45)
    ax.set_title("Top 10 Taluks by Total Agricultural Land Holders")
    st.pyplot(fig)

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
            top_taluk = agriculture_df.loc[agriculture_df[agriculture_df.columns[-1]].idxmax()]
            response = (f"🌾 The taluk with the highest total agricultural area is "
                        f"**{top_taluk['Taluk name']}**, "
                        f"covering **{top_taluk[agriculture_df.columns[-1]]:.2f} hectares.**")
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

