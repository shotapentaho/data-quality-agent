"""File handling and loading operations"""

import pandas as pd
from pathlib import Path
import json
from typing import Optional
import streamlit as st


def load_uploaded_file(uploaded_file, max_rows: Optional[int] = None) -> Optional[pd.DataFrame]:
    """
    Load data from Streamlit uploaded file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        max_rows: Maximum number of rows to load
        
    Returns:
        DataFrame or None if loading fails
    """
    try:
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        if file_extension == '.csv':
            df = pd.read_csv(uploaded_file, nrows=max_rows, low_memory=False)
            
        elif file_extension in ['.json', '.jsonl']:
            try:
                uploaded_file.seek(0)
                df = pd.read_json(uploaded_file, lines=True, nrows=max_rows)
            except ValueError:
                uploaded_file.seek(0)
                content = uploaded_file.read()
                data = json.loads(content)
                
                if isinstance(data, list):
                    if max_rows and len(data) > max_rows:
                        data = data[:max_rows]
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame([data])
                    
        elif file_extension == '.parquet':
            df = pd.read_parquet(uploaded_file)
            if max_rows and len(df) > max_rows:
                df = df.head(max_rows)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
        
        return df
        
    except Exception as e:
        st.error(f"Error loading {uploaded_file.name}: {str(e)}")
        return None


def get_file_info(uploaded_file) -> dict:
    """Get file metadata"""
    return {
        'name': uploaded_file.name,
        'size_mb': uploaded_file.size / (1024 * 1024),
        'extension': Path(uploaded_file.name).suffix.lower()
    }