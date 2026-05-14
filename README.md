# 📊 Kitchen Performance & Variance Dashboard

A comprehensive Streamlit dashboard developed for Rebel Foods to analyze and visualize kitchen performance metrics, profit and loss (P&L) data, and variance analysis.

## 🚀 Links
- **Deployed Application**: [https://streamrebel-jkafbkx55d2q9u3oamp4em.streamlit.app/](https://streamrebel-jkafbkx55d2q9u3oamp4em.streamlit.app/)
- **GitHub Repository**: [https://github.com/ridhesh/stream_rebel](https://github.com/ridhesh/stream_rebel)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Data Processing](#data-processing)
- [Project Structure](#project-structure)
- [Installation & Local Setup](#installation--local-setup)
- [Implementation Process](#implementation-process)

---

## 🔍 Overview
This project transforms raw Excel-based P&L data into an interactive, actionable dashboard. It enables kitchen managers and stakeholders to:
- Monitor **Net Revenue**, **Gross Margin**, and **EBITDA** trends.
- Analyze **Variance** between ideal and actual food costs.
- Compare performance across different **Cities**, **Zones**, and **Stores**.
- Identify outliers and distribution patterns in kitchen profitability.

## ✨ Features
### 1. Kitchen Performance Dashboard
- **Metric Cards**: Real-time display of Total Net Revenue, Gross Margin, Avg GM%, Total EBITDA, and Avg CM%.
- **Monthly Trend Analysis**: Visualizing revenue, margin, and EBITDA over time using multi-axis charts.
- **Store Comparison**: Top 20 stores ranking by revenue with EBITDA color-coding.
- **EBITDA Distribution**: Histogram showing the frequency of EBITDA performance across categories.
- **Raw Data Viewer**: Tabular view of filtered data with formatted currency and percentages.

### 2. Variance Analysis Dashboard
- **Variance % Analysis**: Bar charts showing average variance percentage by revenue cohort.
- **Store Count Heatmap**: A temporal heatmap visualizing store distribution across revenue ranges over months.
- **Bucket Filtering**: Specialized filters for variance ranges (e.g., < 15k, 15k-20k, etc.).

### 3. Advanced Filtering
- **Global Filters**: Sidebar filters for City, Zone, and Month.
- **Cohort Filters**: Select specific Revenue, CM, or EBITDA cohorts.
- **Range Sliders**: Dynamic sliders for Net Revenue, EBITDA, and Contribution Margin ranges.

## 🛠 Tech Stack
- **Framework**: [Streamlit](https://streamlit.io/) (Web UI)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
- **Visualizations**: [Plotly](https://plotly.com/python/) (Express & Graph Objects)
- **Data Source**: Excel (.xlsx) using `openpyxl`

## 📊 Data Processing
The application performs several automated transformations:
- **Metric Calculation**: Calculates GM%, CM, CM%, and EBITDA from raw P&L values.
- **Categorization**: Automatically assigns stores into Variance Buckets and Revenue Ranges based on performance.
- **Temporal Sorting**: Ensures months are ordered chronologically (Jan 2023 to Dec 2024).
- **Filtering Logic**: Implements a cascading filter system to drill down into specific data subsets.

## 📁 Project Structure
```text
.
├── kitchen_dashboard.py      # Main Streamlit application script
├── Kittchen PNL Data.xlsx    # Source Excel data
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## ⚙️ Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ridhesh/stream_rebel
   cd stream_rebel
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run kitchen_dashboard.py
   ```

---

## 🛠 Implementation Process
The development of this dashboard followed a structured approach:

1.  **Exploratory Data Analysis (EDA)**: Analyzed the `Kittchen PNL Data.xlsx` to understand the schema, handle missing values, and identify key performance indicators (KPIs).
2.  **Environment Setup**: Configured the Python environment with necessary libraries (`streamlit`, `pandas`, `plotly`, `openpyxl`).
3.  **Core Logic Development**:
    *   Implemented data loading and caching to optimize performance.
    *   Developed the sidebar and global filtering mechanism.
    *   Wrote the calculation logic for derived metrics (GM%, CM%, etc.).
4.  **UI/UX Design**: 
    *   Organized the layout using Streamlit Tabs and Columns for a clean interface.
    *   Utilized Plotly for high-quality, interactive visualizations.
5.  **Hardening & Testing**: Added error handling for missing files and empty data scenarios.
6.  **Deployment**: Successfully deployed the application to Streamlit Cloud for public access.

---
*Developed for Rebel Foods - Data Analysis Assignment*
