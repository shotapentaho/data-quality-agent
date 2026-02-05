"""Single file analysis results view"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from modules.ui_components import UIComponents
from utils.visualizations import (
    plot_missing_values_heatmap,
    plot_distributions,
    plot_correlation_matrix,
    plot_outliers
)


def render_single_file_results(df: pd.DataFrame, analysis_result: Dict[str, Any]):
    """
    Render complete single file analysis results
    
    Args:
        df: Analyzed DataFrame
        analysis_result: Dictionary containing results, metrics, row_count, column_count
    """
    results = analysis_result['results']
    metrics = analysis_result['metrics']
    
    # Display data preview summary
    with st.expander("📋 Data Preview", expanded=False):
        st.dataframe(df.head(50), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows Analyzed", f"{df.shape[0]:,}")
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Memory", f"{df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
    
    # Quality Dashboard
    st.markdown("### 📊 Quality Dashboard")
    UIComponents.render_quality_metrics(metrics)
    
    st.divider()
    
    # Create tabs for detailed sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Data Preview",
        "🔍 Detailed Checks",
        "📈 Visualizations",
        "🤖 AI Summary"
    ])
    
    with tab1:
        render_data_preview_tab(df)
    
    with tab2:
        render_detailed_checks_tab(results)
    
    with tab3:
        render_visualizations_tab(df, results)
    
    with tab4:
        render_ai_summary_tab(df, results)


def render_data_preview_tab(df: pd.DataFrame):
    """Render data preview tab content"""
    UIComponents.render_data_preview(df)


def render_detailed_checks_tab(results: Dict[str, Any]):
    """Render detailed quality checks tab"""
    
    # Missing Values
    if 'missing_values' in results:
        st.subheader("🔴 Missing Values")
        missing_data = results['missing_values']
        
        if missing_data['total_missing'] > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Missing", f"{missing_data['total_missing']:,}")
            with col2:
                st.metric("Missing %", f"{missing_data['missing_percentage']:.2f}%")
            
            st.dataframe(
                missing_data['by_column'].style.background_gradient(cmap='Reds'),
                use_container_width=True
            )
        else:
            st.success("✅ No missing values found!")
    
    st.divider()
    
    # Duplicates
    if 'duplicates' in results:
        st.subheader("🔄 Duplicate Records")
        dup_data = results['duplicates']
        
        if dup_data['duplicate_count'] > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Duplicate Rows", f"{dup_data['duplicate_count']:,}")
            with col2:
                st.metric("Duplicate %", f"{dup_data['duplicate_percentage']:.2f}%")
            
            with st.expander("View Duplicate Records"):
                st.dataframe(dup_data['duplicate_rows'], use_container_width=True)
        else:
            st.success("✅ No duplicate records found!")
    
    st.divider()
    
    # Data Types
    if 'data_types' in results:
        st.subheader("🔤 Data Types")
        type_data = results['data_types']
        
        st.dataframe(type_data['column_types'], use_container_width=True)
        
        if type_data['type_mismatches']:
            st.warning("⚠️ Potential type issues detected:")
            for issue in type_data['type_mismatches']:
                st.write(f"- {issue}")
    
    st.divider()
    
    # Outliers
    if 'outliers' in results:
        st.subheader("📉 Outliers")
        outlier_data = results['outliers']
        
        if outlier_data['total_outliers'] > 0:
            st.metric("Total Outliers", f"{outlier_data['total_outliers']:,}")
            st.dataframe(outlier_data['by_column'], use_container_width=True)
        else:
            st.success("✅ No significant outliers detected!")
    
    st.divider()
    
    # Schema
    if 'schema' in results:
        st.subheader("📋 Schema Validation")
        schema_data = results['schema']
        
        st.dataframe(schema_data['schema_info'], use_container_width=True)
    
    st.divider()
    
    # Statistics
    if 'statistics' in results:
        st.subheader("📊 Statistical Summary")
        stats_data = results['statistics']
        
        st.dataframe(stats_data['numeric_stats'], use_container_width=True)
        
        if not stats_data['categorical_stats'].empty:
            st.subheader("Categorical Columns")
            st.dataframe(stats_data['categorical_stats'], use_container_width=True)


def render_visualizations_tab(df: pd.DataFrame, results: Dict[str, Any]):
    """Render visualizations tab"""
    
    # Missing values heatmap
    if 'missing_values' in results and results['missing_values']['total_missing'] > 0:
        st.subheader("Missing Values Heatmap")
        fig = plot_missing_values_heatmap(df)
        if fig:
            st.pyplot(fig)
    
    st.divider()
    
    # Distributions
    st.subheader("Data Distributions")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        selected_col = st.selectbox("Select column for distribution", numeric_cols)
        fig = plot_distributions(df, selected_col)
        if fig:
            st.pyplot(fig)
    else:
        st.info("No numeric columns available for distribution plots")
    
    st.divider()
    
    # Correlation matrix
    if len(numeric_cols) > 1:
        st.subheader("Correlation Matrix")
        fig = plot_correlation_matrix(df)
        if fig:
            st.pyplot(fig)
    
    st.divider()
    
    # Outliers visualization
    if 'outliers' in results and results['outliers']['total_outliers'] > 0:
        st.subheader("Outlier Detection")
        if numeric_cols:
            selected_col = st.selectbox("Select column for outlier analysis", numeric_cols, key='outlier_col')
            fig = plot_outliers(df, selected_col)
            if fig:
                st.pyplot(fig)


def render_ai_summary_tab(df: pd.DataFrame, results: Dict[str, Any]):
    """Render AI summary tab"""
    
    if 'ai_insights' in results:
        insights = results['ai_insights']
        
        st.markdown("### 📋 Executive Summary")
        st.info(insights.get('summary', 'No insights available'))
        
        st.divider()
        
        st.markdown("### 🔍 Identified Issues")
        
        # Missing Values Table
        if 'missing_values' in results and results['missing_values']['total_missing'] > 0:
            st.markdown("#### Missing Values")
            missing_issues = []
            for col in df.columns:
                missing_mask = df[col].isna()
                if missing_mask.any():
                    missing_row_indices = df[missing_mask].index.tolist()
                    for row_idx in missing_row_indices[:10]:
                        missing_issues.append({
                            'Issue Type': 'Missing Value',
                            'Column': col,
                            'Row': row_idx,
                            'Severity': '⚠️ Medium'
                        })
            
            if missing_issues:
                missing_df = pd.DataFrame(missing_issues)
                st.dataframe(missing_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        if insights.get('recommendations'):
            st.markdown("### 💡 Recommendations")
            for i, rec in enumerate(insights['recommendations'], 1):
                st.markdown(f"{i}. {rec}")
        
        if insights.get('priority_issues'):
            st.markdown("### 🚨 Priority Actions")
            for issue in insights['priority_issues']:
                st.warning(f"⚠️ {issue}")
    else:
        st.info("Enable 'AI Recommendations' in the configuration and run analysis to see AI-powered insights.")