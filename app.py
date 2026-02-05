"""
CX Data Quality Agent - Main Application
Modular Streamlit app for data quality analysis
"""

import streamlit as st

# Import modules
from modules.session_manager import SessionManager
from modules.ui_components import UIComponents
from modules.analysis_engine import AnalysisEngine
from modules.file_handler import load_uploaded_file

# Import existing result display functions
from views.single_file_view import render_single_file_results
from views.batch_results_view import render_batch_results

# Theme (works with our CSS overrides)
from st_ui_theme import apply_theme
apply_theme()

st.markdown(
    """
<style>
#MainMenu {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True
)
# Page configuration
st.set_page_config(
    page_title="CX Data Quality Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: left;
        margin-bottom: 0.5rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid #1f77b4;
    }
    .subheader {
        font-size: 0.9rem;
        color: #666;
        text-align: left;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
SessionManager.initialize()

# Initialize analysis engine
analysis_engine = AnalysisEngine()

# HEADER
UIComponents.render_header()

# Two-column layout
left_col, right_col = st.columns([1, 2])

with left_col:
    # File upload
    uploaded_files = UIComponents.render_file_uploader()
    
    # File list
    processed_files = SessionManager.get_processed_files()
    UIComponents.render_file_list(uploaded_files, processed_files)
    
    st.divider()
    
    # Configuration
    if uploaded_files:
        config = UIComponents.render_configuration()
        
        # Analysis button
        num_files = len(uploaded_files)
        new_files = [f for f in uploaded_files if f.name not in processed_files]
        num_new = len(new_files)
        
        analyze_button = UIComponents.render_analysis_button(num_files, num_new)

with right_col:
    if uploaded_files and analyze_button:
        # Initialize AI agent if needed
        if config['use_ai']:
            analysis_engine.initialize_ai_agent()
        
        if num_files == 1:
            # === SINGLE FILE MODE ===
            st.markdown("### 📊 Quality Analysis")
            
            uploaded_file = uploaded_files[0]
            
            with st.spinner(f"Loading {uploaded_file.name}..."):
                df = load_uploaded_file(uploaded_file, config['max_rows'])
            
            if df is not None:
                # Store in session
                SessionManager.set('df', df)
                
                # Run analysis
                analysis_result = analysis_engine.analyze_single_file(
                    df,
                    config['checks'],
                    config['use_ai']
                )
                
                # Store results
                SessionManager.set('quality_results', analysis_result['results'])
                SessionManager.mark_analysis_complete()
                
                # Render results
                render_single_file_results(df, analysis_result)
        
        else:
            # === BATCH MODE ===
            st.markdown("### 📊 Batch Analysis Progress")
            
            # Run batch analysis
            batch_results = analysis_engine.analyze_batch(
                uploaded_files,
                config['max_rows'],
                config['checks'],
                config['use_ai'],
                processed_files
            )
            
            # Update session state
            SessionManager.update_batch_results(batch_results)
            SessionManager.mark_analysis_complete()
    
    # Display results (persisted)
    if SessionManager.get('analysis_done'):
        batch_results = SessionManager.get('batch_results', {})
        
        if batch_results:
            render_batch_results(batch_results)
        elif not uploaded_files:
            UIComponents.render_welcome_screen()
    elif not uploaded_files:
        UIComponents.render_welcome_screen()
    else:
        st.info("👈 Click 'Run Analysis' or 'Analyze N Files' to start")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>CX Data Quality Agent v1.0 | Powered by Google Gemini & Streamlit</p>
    </div>
""", unsafe_allow_html=True)