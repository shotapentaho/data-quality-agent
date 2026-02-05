import pandas as pd
import streamlit as st
from typing import Optional
import io

def load_csv_file(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Load a CSV file with robust error handling.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        pandas DataFrame or None if loading fails
    """
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

        for encoding in encodings:
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding=encoding)
                return df
            except UnicodeDecodeError:
                continue

        # If all encodings fail
        st.error("❌ Could not decode the file. Please check the file encoding.")
        return None

    except pd.errors.EmptyDataError:
        st.error("❌ The uploaded file is empty.")
        return None

    except pd.errors.ParserError as e:
        st.error(f"❌ Error parsing CSV file: {str(e)}")
        return None

    except Exception as e:
        st.error(f"❌ Unexpected error loading file: {str(e)}")
        return None
