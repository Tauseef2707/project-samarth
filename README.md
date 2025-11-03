# Project Samarth - Intelligent Q&A System

This project demonstrates an AI-powered Question and Answer System built using Python and Machine Learning.

🎥 **Watch the Demo Video:**  
[Loom Video Link](https://www.loom.com/share/4fb8e871e8c94ffab6b0555f15c56c17)

## Quick run & expected columns

Install dependencies (recommended in a virtualenv):

```bash
pip install -r requirements.txt
```

Run locally with Streamlit:

```bash
streamlit run /workspaces/project-samarth/app.py
```

Expected column names in the agriculture CSV:
- A column containing the taluk or category name (examples: `Taluk name`, `Taluk`, `Name`).
- A numeric area/total column (examples: `Total_Area_Total`, `Total Agricultural Land Holders _Total_Area_Total`, `Total`).

The app normalizes column names (trims whitespace and removes BOM) and attempts to auto-detect these columns by keywords. If detection fails, use the dropdowns in the UI to select the correct x/y columns.
