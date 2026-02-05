import pandas as pd
import numpy as np
from typing import Dict, Any, List

def check_missing_values(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Check for missing values in the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with missing value statistics
    """
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    missing_percentage = (missing_cells / total_cells) * 100
    
    # Per column analysis
    missing_by_column = pd.DataFrame({
        'Missing_Count': df.isnull().sum(),
        'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
    })
    missing_by_column = missing_by_column[missing_by_column['Missing_Count'] > 0]
    missing_by_column = missing_by_column.sort_values('Missing_Count', ascending=False)
    
    return {
        'total_missing': int(missing_cells),
        'missing_percentage': float(missing_percentage),
        'by_column': missing_by_column
    }


def check_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Check for duplicate records in the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with duplicate statistics
    """
    duplicate_rows = df[df.duplicated(keep=False)]
    duplicate_count = df.duplicated().sum()
    duplicate_percentage = (duplicate_count / len(df)) * 100
    
    return {
        'duplicate_count': int(duplicate_count),
        'duplicate_percentage': float(duplicate_percentage),
        'duplicate_rows': duplicate_rows
    }


def check_data_types(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate and analyze data types in the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with data type information
    """
    column_types = pd.DataFrame({
        'Column': df.columns,
        'Data_Type': df.dtypes.astype(str),
        'Unique_Values': [df[col].nunique() for col in df.columns],
        'Sample_Value': [str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else 'N/A' 
                        for col in df.columns]
    })
    
    # Check for potential type mismatches
    type_mismatches = []
    
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if numeric values stored as strings
            try:
                pd.to_numeric(df[col].dropna(), errors='raise')
                type_mismatches.append(f"Column '{col}' appears to contain numeric values but is stored as text")
            except (ValueError, TypeError):
                pass
            
            # Check if dates stored as strings
            try:
                sample = df[col].dropna().head(100)
                if len(sample) > 0:
                    parsed = pd.to_datetime(sample, errors='coerce')
                    if parsed.notna().sum() / len(sample) > 0.8:  # 80% parseable as dates
                        type_mismatches.append(f"Column '{col}' appears to contain dates but is stored as text")
            except:
                pass
    
    return {
        'column_types': column_types,
        'type_mismatches': type_mismatches
    }


def detect_outliers(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect outliers in numeric columns using IQR method.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with outlier information
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_info = []
    total_outliers = 0
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)
        
        if outlier_count > 0:
            outlier_percentage = (outlier_count / len(df)) * 100
            outlier_info.append({
                'Column': col,
                'Outlier_Count': outlier_count,
                'Outlier_Percentage': round(outlier_percentage, 2),
                'Lower_Bound': round(lower_bound, 2),
                'Upper_Bound': round(upper_bound, 2)
            })
            total_outliers += outlier_count
    
    outlier_df = pd.DataFrame(outlier_info)
    
    return {
        'total_outliers': int(total_outliers),
        'by_column': outlier_df
    }


def validate_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate and analyze the schema of the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with schema information
    """
    schema_info = []
    
    for col in df.columns:
        col_data = {
            'Column': col,
            'Data_Type': str(df[col].dtype),
            'Non_Null_Count': int(df[col].count()),
            'Null_Count': int(df[col].isnull().sum()),
            'Unique_Count': int(df[col].nunique()),
            'Memory_Usage': f"{df[col].memory_usage(deep=True) / 1024:.2f} KB"
        }
        
        # Add type-specific info
        if df[col].dtype in ['int64', 'float64']:
            col_data['Min'] = float(df[col].min())
            col_data['Max'] = float(df[col].max())
            col_data['Mean'] = float(df[col].mean())
        elif df[col].dtype == 'object':
            col_data['Max_Length'] = int(df[col].astype(str).str.len().max())
            col_data['Min_Length'] = int(df[col].astype(str).str.len().min())
        
        schema_info.append(col_data)
    
    schema_df = pd.DataFrame(schema_info)
    
    return {
        'schema_info': schema_df
    }


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics for the dataset.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        Dictionary with statistical information
    """
    # Numeric columns
    numeric_stats = df.describe()
    
    # Categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    categorical_stats = []
    
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        categorical_stats.append({
            'Column': col,
            'Unique_Values': len(value_counts),
            'Most_Common': value_counts.index[0] if len(value_counts) > 0 else 'N/A',
            'Most_Common_Count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
            'Most_Common_Percentage': round((value_counts.iloc[0] / len(df)) * 100, 2) if len(value_counts) > 0 else 0
        })
    
    categorical_df = pd.DataFrame(categorical_stats)
    
    return {
        'numeric_stats': numeric_stats,
        'categorical_stats': categorical_df
    }