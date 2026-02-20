"""Reusable UI components"""

import streamlit as st
import pandas as pd
from typing import Dict, Any


class UIComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def render_header():
        """Render main application header"""
        st.markdown('<h1 class="main-header">📊 CX Data Quality Agent</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subheader">AI-Powered Data Quality Analysis & Insights</p>', unsafe_allow_html=True)
    
    @staticmethod
    def render_file_uploader():
        """Render file upload widget"""
        st.markdown("### 📂 Browse Files")
        st.caption("Upload one or multiple data files")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['csv', 'json', 'jsonl', 'parquet'],
            accept_multiple_files=True,
            help="Select one or more CSV, JSON, or Parquet files",
            label_visibility="collapsed"
        )
        
        return uploaded_files
    
    @staticmethod
    def render_file_list(uploaded_files: list, processed_files: set):
        """Render list of uploaded files with status"""
        if not uploaded_files:
            return
        
        num_files = len(uploaded_files)
        total_size = sum(f.size for f in uploaded_files) / (1024 * 1024)
        
        if num_files == 1:
            st.success(f"✅ {uploaded_files[0].name} ({uploaded_files[0].size / (1024 * 1024):.1f}MB)")
        else:
            st.success(f"✅ {num_files} files selected ({total_size:.1f}MB total)")
            
            with st.expander("📋 File List", expanded=True):
                for f in uploaded_files:
                    file_size = f.size / (1024 * 1024)
                    status = "✓ Processed" if f.name in processed_files else "⏳ Pending"
                    st.write(f"📄 {f.name} ({file_size:.1f}MB) - {status}")
    
    @staticmethod
    def render_configuration() -> Dict[str, Any]:
        """Render configuration panel and return settings"""
        st.markdown("### ⚙️ Configuration")
        
        # Row limit slider
        st.markdown("**🎲 Row Limit**")
        st.caption("Sample data for faster analysis")
        
        max_rows = st.select_slider(
            "Maximum rows to analyze",
            options=[50000, 100000, 500000, 1000000],
            value=50000,
            format_func=lambda x: {
                50000: "50K rows (Fast)",
                100000: "100K rows (Balanced)", 
                500000: "500K rows (Comprehensive)",
                1000000: "1M rows (Full analysis)"
            }[x]
        )
        
        st.divider()
        
        # Quality checks
        st.markdown("**Quality Checks**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            run_missing = st.checkbox("Missing Values", value=True)
        with col2:
            run_duplicates = st.checkbox("Duplicates", value=True)
        with col3:
            run_types = st.checkbox("Data Types", value=True)
        
        col4, col5, col6 = st.columns(3)
        with col4:
            run_outliers = st.checkbox("Outliers", value=True)
        with col5:
            run_schema = st.checkbox("Schema", value=True)
        with col6:
            run_stats = st.checkbox("Statistics", value=True)
        
        st.divider()
        
        # AI insights
        st.markdown("**AI Insights**")
        use_ai = st.checkbox("Enable AI Recommendations", value=True)
        
        return {
            'max_rows': max_rows,
            'checks': {
                'missing': run_missing,
                'duplicates': run_duplicates,
                'types': run_types,
                'outliers': run_outliers,
                'schema': run_schema,
                'stats': run_stats
            },
            'use_ai': use_ai
        }
    
    @staticmethod
    def render_analysis_button(num_files: int, num_new: int) -> bool:
        """Render analysis button and return if clicked"""
        st.divider()
        
        if num_files == 1:
            return st.button("🔍 Run Analysis", type="primary", use_container_width=True)
        elif num_new == 0:
            st.info("✓ All files already analyzed")
            return False
        else:
            return st.button(f"🔍 Analyze {num_new} New File(s)", type="primary", use_container_width=True)
    
    @staticmethod
    def render_quality_metrics(metrics: Dict[str, float]):
        """Render quality metrics dashboard"""
        if not metrics:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            score = metrics.get('overall_score', 0)
            st.metric("Quality Score", f"{score:.1f}%")
        
        with col2:
            completeness = metrics.get('completeness', 0)
            st.metric("Completeness", f"{completeness:.1f}%")
        
        with col3:
            uniqueness = metrics.get('uniqueness', 0)
            st.metric("Uniqueness", f"{uniqueness:.1f}%")
        
        with col4:
            validity = metrics.get('validity', 0)
            st.metric("Validity", f"{validity:.1f}%")
    
    @staticmethod
    def render_data_preview(df: pd.DataFrame):
        """Render data preview section"""
        st.dataframe(df.head(100), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", f"{len(df):,}")
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Memory", f"{df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
    
    @staticmethod
    def render_welcome_screen():
        """Render welcome/info screen"""
        st.markdown("### 👈 Get Started")
        st.info("Click the **Browse files** button to select one or more data files to analyze.")
        
        with st.expander("ℹ️ Features & Capabilities"):
            st.markdown("""
            **📂 File Upload**
            - **Single File**: Upload one file for detailed analysis
            - **Multiple Files**: Upload multiple files for batch processing
            - **Drag & Drop**: Drag files directly into the upload area
            - **Incremental Analysis**: Add new files without re-processing existing ones
            
            **📊 Comprehensive Quality Checks**
            - Missing Values, Duplicates, Data Types
            - Outliers, Schema Validation, Statistics
            
            **📈 Rich Visualizations**
            - Heatmaps, Distributions, Correlations
            - Outlier Detection Charts
            
            **🤖 AI-Powered Insights**
            - Intelligent recommendations
            - Priority issue identification
            - Separate AI Summary tab
            
            **📂 Supported File Formats**
            - **CSV**: Efficient chunked reading
            - **JSON**: Array or JSONL (line-delimited) 
            - **Parquet**: Best for large files (compressed)
            
            **⚡ Performance**
            - Handles 1M+ rows with sampling
            - Smart batch processing (skip already-analyzed files)
            - Increase nginx: `client_max_body_size 500M;`
            """)
