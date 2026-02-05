"""Batch analysis results view"""

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


def render_batch_results(batch_results: Dict[str, Dict[str, Any]]):
    """
    Render batch analysis results
    
    Args:
        batch_results: Dictionary mapping file names to their analysis results
    """
    st.markdown("### 📊 Batch Analysis Results")
    
    # Summary table
    summary_data = []
    for file_name, data in batch_results.items():
        metrics = data.get('metrics', {})
        summary_data.append({
            'File': file_name,
            'Rows': f"{data['row_count']:,}",
            'Columns': data['column_count'],
            'Quality Score': f"{metrics.get('overall_score', 0):.1f}%",
            'Completeness': f"{metrics.get('completeness', 0):.1f}%",
            'Uniqueness': f"{metrics.get('uniqueness', 0):.1f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Individual file results
    st.markdown("### 📄 Individual File Details")
    
    selected_file_name = st.selectbox("Select file to view details", list(batch_results.keys()))
    
    if selected_file_name:
        file_data = batch_results[selected_file_name]
        df = file_data['dataframe']
        results = file_data['results']
        metrics = file_data['metrics']
        
        # Show metrics
        UIComponents.render_quality_metrics(metrics)
        
        st.divider()
        
        # Tabs for detailed view
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Data Preview",
            "🔍 Quality Issues",
            "📈 Charts",
            "🤖 AI Summary"
        ])
        
        with tab1:
            render_batch_data_preview(df)
        
        with tab2:
            render_batch_quality_issues(results)
        
        with tab3:
            render_batch_charts(df, results, selected_file_name)
        
        with tab4:
            render_batch_ai_summary(results)


def render_batch_data_preview(df: pd.DataFrame):
    """Render data preview for batch file"""
    UIComponents.render_data_preview(df)


def render_batch_quality_issues(results: Dict[str, Any]):
    """Render quality issues summary for batch file"""
    
    if 'missing_values' in results and results['missing_values']['total_missing'] > 0:
        st.subheader("🔴 Missing Values")
        missing_data = results['missing_values']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Missing", f"{missing_data['total_missing']:,}")
        with col2:
            st.metric("Missing %", f"{missing_data['missing_percentage']:.2f}%")
    
    if 'duplicates' in results and results['duplicates']['duplicate_count'] > 0:
        st.subheader("🔄 Duplicates")
        dup_data = results['duplicates']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Duplicate Rows", f"{dup_data['duplicate_count']:,}")
        with col2:
            st.metric("Duplicate %", f"{dup_data['duplicate_percentage']:.2f}%")
    
    if 'outliers' in results and results['outliers']['total_outliers'] > 0:
        st.subheader("📉 Outliers")
        st.metric("Total Outliers", f"{results['outliers']['total_outliers']:,}")


def render_batch_charts(df: pd.DataFrame, results: Dict[str, Any], file_name: str):
    """Render charts for batch file"""
    
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
        selected_col = st.selectbox(
            "Select column for distribution",
            numeric_cols,
            key=f"dist_{file_name}"
        )
        fig = plot_distributions(df, selected_col)
        if fig:
            st.pyplot(fig)
    else:
        st.info("No numeric columns available")
    
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
            selected_col = st.selectbox(
                "Select column for outlier analysis",
                numeric_cols,
                key=f"outlier_{file_name}"
            )
            fig = plot_outliers(df, selected_col)
            if fig:
                st.pyplot(fig)


def render_batch_ai_summary(results: Dict[str, Any]):
    """Render AI summary for batch file"""
    
    if 'ai_insights' in results:
        insights = results['ai_insights']
        
        st.markdown("### 📋 Executive Summary")
        st.info(insights.get('summary', 'No insights available'))
        
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
        st.info("AI insights not available for this file.")