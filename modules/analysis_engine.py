"""Quality analysis execution engine"""

import pandas as pd
from typing import Dict, Any
import streamlit as st

from utils.quality_checks import (
    check_missing_values,
    check_duplicates,
    check_data_types,
    detect_outliers,
    validate_schema,
    calculate_statistics
)
from utils.visualizations import plot_quality_dashboard
from agents.data_quality_agent import DataQualityAgent


class AnalysisEngine:
    """Handles quality check execution and result management"""
    
    def __init__(self):
        self.agent = None
    
    def initialize_ai_agent(self) -> bool:
        """Initialize AI agent for insights"""
        if self.agent is None:
            try:
                self.agent = DataQualityAgent()
                return True
            except Exception as e:
                st.warning(f"⚠️ Could not initialize AI Agent: {str(e)}")
                return False
        return True
    
    def run_quality_checks(
        self,
        df: pd.DataFrame,
        run_missing: bool = True,
        run_duplicates: bool = True,
        run_types: bool = True,
        run_outliers: bool = True,
        run_schema: bool = True,
        run_stats: bool = True
    ) -> Dict[str, Any]:
        """
        Execute selected quality checks on dataframe
        
        Args:
            df: Input DataFrame
            run_*: Boolean flags for each check type
            
        Returns:
            Dictionary of results for each check
        """
        results = {}
        
        if run_missing:
            results['missing_values'] = check_missing_values(df)
        
        if run_duplicates:
            results['duplicates'] = check_duplicates(df)
        
        if run_types:
            results['data_types'] = check_data_types(df)
        
        if run_outliers:
            results['outliers'] = detect_outliers(df)
        
        if run_schema:
            results['schema'] = validate_schema(df)
        
        if run_stats:
            results['statistics'] = calculate_statistics(df)
        
        return results
    
    def generate_ai_insights(self, df: pd.DataFrame, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered insights from analysis results"""
        if self.agent is None:
            return {}
        
        try:
            ai_insights = self.agent.analyze_quality_results(df, results)
            return ai_insights
        except Exception as e:
            st.warning(f"⚠️ Could not generate AI insights: {str(e)}")
            return {}
    
    def analyze_single_file(
        self,
        df: pd.DataFrame,
        checks_config: Dict[str, bool],
        use_ai: bool = True
    ) -> Dict[str, Any]:
        """
        Complete analysis workflow for a single file
        
        Args:
            df: Input DataFrame
            checks_config: Dictionary of check names and their enabled status
            use_ai: Whether to generate AI insights
            
        Returns:
            Complete analysis results including quality checks and metrics
        """
        # Run quality checks
        with st.spinner("Running quality checks..."):
            results = self.run_quality_checks(
                df,
                run_missing=checks_config.get('missing', True),
                run_duplicates=checks_config.get('duplicates', True),
                run_types=checks_config.get('types', True),
                run_outliers=checks_config.get('outliers', True),
                run_schema=checks_config.get('schema', True),
                run_stats=checks_config.get('stats', True)
            )
        
        # Calculate quality metrics
        quality_metrics = plot_quality_dashboard(df, results)
        
        # Generate AI insights if enabled
        if use_ai:
            with st.spinner("Generating AI insights..."):
                ai_insights = self.generate_ai_insights(df, results)
                if ai_insights:
                    results['ai_insights'] = ai_insights
        
        return {
            'results': results,
            'metrics': quality_metrics,
            'row_count': len(df),
            'column_count': len(df.columns)
        }
    
    def analyze_batch(
        self,
        uploaded_files: list,
        max_rows: int,
        checks_config: Dict[str, bool],
        use_ai: bool,
        processed_files: set
    ) -> Dict[str, Dict[str, Any]]:
        """
        Batch analysis workflow for multiple files
        
        Args:
            uploaded_files: List of uploaded file objects
            max_rows: Maximum rows to analyze per file
            checks_config: Dictionary of check configurations
            use_ai: Whether to use AI insights
            processed_files: Set of already processed file names
            
        Returns:
            Dictionary mapping file names to their analysis results
        """
        from modules.file_handler import load_uploaded_file
        
        # Filter out already processed files
        files_to_process = [f for f in uploaded_files if f.name not in processed_files]
        
        if not files_to_process:
            return {}
        
        batch_results = {}
        num_files = len(files_to_process)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, uploaded_file in enumerate(files_to_process):
            file_name = uploaded_file.name
            status_text.text(f"Processing {idx+1}/{num_files}: {file_name}")
            
            # Load file
            df = load_uploaded_file(uploaded_file, max_rows)
            
            if df is not None:
                # Analyze file
                analysis_result = self.analyze_single_file(df, checks_config, use_ai)
                
                # Store complete results including dataframe
                batch_results[file_name] = {
                    'dataframe': df,
                    **analysis_result
                }
                
                # Mark as processed
                processed_files.add(file_name)
            
            progress_bar.progress((idx + 1) / num_files)
        
        status_text.text(f"✅ Processed {num_files} new file(s)!")
        
        return batch_results