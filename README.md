# 📊 CX Data Quality Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI-Powered Data Quality Analysis & Insights** - A modular, enterprise-grade Streamlit application that combines traditional statistical quality checks with cutting-edge AI analysis to provide comprehensive data quality assessment.

## 🎯 Overview

CX Data Quality Agent revolutionizes data quality analysis by integrating:
- **Statistical Quality Checks**: Traditional data profiling and validation
- **AI-Powered Insights**: Google Gemini-based intelligent recommendations
- **Batch Processing**: Analyze multiple datasets simultaneously
- **Interactive Visualizations**: Rich, publication-ready charts
- **Modular Architecture**: Clean, maintainable, and extensible codebase

Perfect for **data analysts**, **data engineers**, **ML practitioners**, and **quality assurance teams** who need fast, reliable data quality assessment.

---

## 🏗️ Architecture & Project Structure

### High-Level Architecture


### Project File Structure

data-quality-agent/ │ ├── 📄 app.py # Main Streamlit application entry point │ ├── 📁 modules/ # Core business logic modules │ ├── init.py # Package initializer │ ├── file_handler.py # File loading & format handling │ ├── analysis_engine.py # Quality checks orchestration │ ├── session_manager.py # Streamlit session state management │ └── ui_components.py # Reusable UI widgets & components │ ├── 📁 views/ # UI rendering & display logic │ ├── init.py # Package initializer │ ├── single_file_view.py # Single file results rendering │ └── batch_results_view.py # Batch analysis results rendering │ ├── 📁 utils/ # Utility functions & helpers │ ├── data_loader.py # Data loading utilities │ ├── quality_checks.py # Quality check implementations │ └── visualizations.py # Chart generation functions │ ├── 📁 agents/ # AI/ML agents │ └── data_quality_agent.py # Google Gemini integration │ ├── 📁 .streamlit/ # Streamlit configuration │ └── config.toml # App configuration settings │ ├── 📄 requirements.txt # Python dependencies ├── 📄 README.md # This file └── 📄 LICENSE # MIT License


### Module Responsibilities

| Module | Responsibility | Key Functions |
|--------|---------------|---------------|
| `app.py` | Application orchestration | UI layout, workflow coordination |
| `file_handler.py` | I/O operations | Load CSV, JSON, Parquet files |
| `analysis_engine.py` | Quality check execution | Run checks, generate metrics |
| `session_manager.py` | State persistence | Manage analysis results across sessions |
| `ui_components.py` | UI primitives | Buttons, metrics, configuration panels |
| `single_file_view.py` | Single file display | Render detailed analysis tabs |
| `batch_results_view.py` | Batch display | Summary tables, file selection |
| `quality_checks.py` | Validation logic | Missing values, duplicates, outliers |
| `visualizations.py` | Chart generation | Heatmaps, distributions, correlations |
| `data_quality_agent.py` | AI analysis | Gemini-based insights generation |

---

## 🔬 Technologies & Stack

### Core Technologies

```python
Framework:    Streamlit 1.28+          # Interactive web app framework
Language:     Python 3.8+              # Core programming language
Data:         Pandas 2.0+              # Data manipulation & analysis
Visualization: Matplotlib 3.7+         # Plotting & charting
              Seaborn 0.12+           # Statistical visualizations
AI/ML:        Google Gemini API        # Generative AI for insights
              google-generativeai     # Official Gemini Python SDK
File Formats: PyArrow 12.0+           # Parquet file support
Statistics:   NumPy 1.24+             # Numerical computations
              SciPy 1.10+             # Statistical functions


┌──────────────┐
│ File Upload  │
│ (CSV/JSON/   │
│  Parquet)    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│ 1. FILE VALIDATION & LOADING         │
│    ├─ Detect file format             │
│    ├─ Validate file integrity        │
│    ├─ Apply row sampling (if needed) │
│    └─ Load into Pandas DataFrame     │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ 2. QUALITY CHECKS EXECUTION           │
│    ├─ Missing Values Analysis        │
│    ├─ Duplicate Detection            │
│    ├─ Data Type Validation           │
│    ├─ Outlier Detection (IQR)        │
│    ├─ Schema Validation              │
│    └─ Statistical Summary            │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ 3. METRICS CALCULATION                │
│    ├─ Completeness Score             │
│    ├─ Uniqueness Score               │
│    ├─ Validity Score                 │
│    └─ Overall Quality Score          │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ 4. VISUALIZATION GENERATION           │
│    ├─ Missing values heatmap         │
│    ├─ Distribution plots             │
│    ├─ Correlation matrices           │
│    └─ Outlier box plots              │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ 5. AI INSIGHTS (Optional)             │
│    ├─ Send results to Gemini API    │
│    ├─ Generate executive summary     │
│    ├─ Create recommendations         │
│    └─ Identify priority issues       │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ 6. RESULTS PRESENTATION               │
│    ├─ Interactive dashboards         │
│    ├─ Tabbed views (4 tabs)         │
│    └─ Downloadable reports (future)  │
└──────────────────────────────────────┘

Step 2: Quality Checks Execution


Quality Checks:
  1. Missing Values:
     - Count nulls per column
     - Calculate percentage
     - Identify patterns
  
  2. Duplicates:
     - Detect exact row matches
     - Show sample duplicates
     - Calculate impact
  
  3. Data Types:
     - Infer expected types
     - Detect type mismatches
     - Validate consistency
  
  4. Outliers:
     - IQR method (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
     - Z-score detection (optional)
     - Flag extreme values
  
  5. Schema:
     - Column name validation
     - Type constraints
     - Nullable checks
  
  6. Statistics:
     - Descriptive stats (mean, median, std)
     - Quartiles, min, max
     - Unique value counts

Step 3: Metrics Calculation

Scoring Algorithm:
  
  Completeness = (Total Cells - Missing Cells) / Total Cells × 100
  
  Uniqueness = (Total Rows - Duplicate Rows) / Total Rows × 100
  
  Validity = (Columns with Valid Types) / Total Columns × 100
  
  Overall Score = (Completeness × 0.4) + 
                  (Uniqueness × 0.3) + 
                  (Validity × 0.3)

Step 4: Visualization Generation
Visualizations:
  - Missing Values Heatmap: Seaborn heatmap showing null patterns
  - Distribution Plots: Histogram + KDE for numeric columns
  - Correlation Matrix: Pearson correlation with color gradient
  - Outlier Box Plots: Identify extreme values visually

🤖 AI-Powered Analysis
How AI is Integrated

┌─────────────────────────────────────────────────────────┐
│                   AI ANALYSIS PIPELINE                   │
└─────────────────────────────────────────────────────────┘

1. Data Collection
   ├─ Quality check results (missing, duplicates, outliers)
   ├─ Statistical summaries (mean, std, quartiles)
   ├─ Schema information (types, columns)
   └─ Sample data records (first 10 rows)

2. Prompt Engineering
   ├─ Structured context formatting
   ├─ Domain-specific instructions
   ├─ Output format specification (JSON)
   └─ Example-based learning

3. Gemini API Request
   ├─ Model: gemini-pro
   ├─ Temperature: 0.7 (balanced creativity)
   ├─ Max tokens: 2048
   └─ Safety settings: Medium

4. Response Processing
   ├─ Parse JSON response
   ├─ Extract insights components
   ├─ Validate output structure
   └─ Handle errors gracefully

5. Results Integration
   ├─ Executive summary
   ├─ Actionable recommendations
   ├─ Priority issue ranking
   └─ Next steps guidance

AI Analysis Components
1. Executive Summary
Code
Generates a 2-3 sentence overview of data quality:
- Overall health assessment
- Key strengths
- Major concerns
Example Output:

"This dataset contains 125,450 records across 18 columns with an overall quality score of 76%. The primary concern is 23% missing values in the 'email' column, which could impact customer outreach. Data types are well-defined, and outlier detection shows only 2.3% of records need review."

2. Recommendations
Code
Provides specific, actionable suggestions:
- Prioritized by impact
- Includes implementation hints
- References specific columns/issues
Example Output:

Code
1. Address missing emails: Implement a data collection form validation or backfill from secondary sources
2. Remove 1,247 duplicate records: Use customer_id as unique key for deduplication
3. Investigate outliers in 'purchase_amount': 89 records exceed $10,000 - validate or cap values
3. Priority Issues
Code
Ranks problems by urgency:
- Critical (blocks usage)
- High (significant impact)
- Medium (gradual degradation)
- Low (minor concerns)
Example Output:

Code
🔴 CRITICAL: 'user_id' column has 45% nulls - impacts all join operations
🟠 HIGH: 15,000 duplicate records (12% of dataset) - inflates metrics
🟡 MEDIUM: 'signup_date' has inconsistent formats - needs standardization


AI Prompt Structure

# Simplified prompt template
prompt = f"""
You are a data quality expert. Analyze this dataset:

DATASET OVERVIEW:
- Shape: {rows} rows × {columns} columns
- Memory: {memory_mb} MB
- File: {filename}

QUALITY METRICS:
- Overall Score: {quality_score}%
- Completeness: {completeness}%
- Uniqueness: {uniqueness}%

ISSUES DETECTED:
1. Missing Values:
{missing_values_summary}

2. Duplicates:
{duplicates_summary}

3. Outliers:
{outliers_summary}

SAMPLE DATA:
{data_sample}

Provide:
1. Executive Summary (2-3 sentences)
2. Top 5 Recommendations (prioritized)
3. Priority Issues (ranked by severity)

Format as JSON with keys: summary, recommendations, priority_issues
"""

When AI is Used
AI Analysis Triggers:
  ✓ User enables "AI Recommendations" checkbox
  ✓ After quality checks complete successfully
  ✓ DataFrame has at least 10 rows
  ✓ Valid Gemini API key is configured

AI Analysis Skipped:
  ✗ User disables AI recommendations
  ✗ API key missing or invalid
  ✗ API rate limit exceeded
  ✗ Network connectivity issues

Benchmarks (on MacBook Pro M1, 16GB RAM):

File Size     Rows      Processing Time    Memory Usage
─────────────────────────────────────────────────────────
10 MB         100K      3-5 seconds        ~150 MB
50 MB         500K      8-12 seconds       ~600 MB
100 MB        1M        15-20 seconds      ~1.2 GB
500 MB        5M        45-60 seconds      ~4 GB (with sampling)

Optimization Features:
- Chunked file reading
- Configurable row sampling
- Lazy evaluation for visualizations
- Memory-efficient data types

Built with ❤️ using:

Streamlit - App framework
Pandas - Data manipulation
Google Gemini - AI insights
Matplotlib & Seaborn - Visualizations
