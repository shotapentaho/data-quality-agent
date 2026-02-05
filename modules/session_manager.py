"""Session state management"""

import streamlit as st
from typing import Any, Optional


class SessionManager:
    """Manages Streamlit session state"""
    
    @staticmethod
    def initialize():
        """Initialize all session state variables"""
        defaults = {
            'df': None,
            'quality_results': {},
            'agent': None,
            'batch_results': {},
            'analysis_done': False,
            'processed_files': set()
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get value from session state"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any):
        """Set value in session state"""
        st.session_state[key] = value
    
    @staticmethod
    def update_batch_results(new_results: dict):
        """Update batch results with new analysis results"""
        current_results = st.session_state.get('batch_results', {})
        current_results.update(new_results)
        st.session_state['batch_results'] = current_results
    
    @staticmethod
    def mark_analysis_complete():
        """Mark analysis as completed"""
        st.session_state['analysis_done'] = True
    
    @staticmethod
    def get_processed_files() -> set:
        """Get set of processed file names"""
        return st.session_state.get('processed_files', set())
    
    @staticmethod
    def is_file_processed(filename: str) -> bool:
        """Check if a file has been processed"""
        return filename in st.session_state.get('processed_files', set())
    
    @staticmethod
    def clear_results():
        """Clear all analysis results"""
        st.session_state['quality_results'] = {}
        st.session_state['batch_results'] = {}
        st.session_state['analysis_done'] = False
        st.session_state['processed_files'] = set()