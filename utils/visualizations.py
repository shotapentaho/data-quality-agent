import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, Any

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def plot_missing_values_heatmap(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Create a heatmap visualization of missing values.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        matplotlib Figure object
    """
    try:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create missing values matrix
        missing_matrix = df.isnull().astype(int)
        
        # Plot heatmap
        sns.heatmap(
            missing_matrix.T,
            cbar=True,
            cmap='RdYlGn_r',
            ax=ax,
            yticklabels=df.columns,
            cbar_kws={'label': 'Missing (1) vs Present (0)'}
        )
        
        ax.set_title('Missing Values Heatmap', fontsize=16, fontweight='bold')
        ax.set_xlabel('Row Index', fontsize=12)
        ax.set_ylabel('Columns', fontsize=12)
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        print(f"Error creating missing values heatmap: {e}")
        return None


def plot_distributions(df: pd.DataFrame, column: str) -> Optional[plt.Figure]:
    """
    Create distribution plots for a numeric column.
    
    Args:
        df: pandas DataFrame
        column: Column name to plot
        
    Returns:
        matplotlib Figure object
    """
    try:
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        data = df[column].dropna()
        
        # Histogram
        axes[0].hist(data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0].set_title(f'Histogram - {column}', fontsize=14, fontweight='bold')
        axes[0].set_xlabel(column)
        axes[0].set_ylabel('Frequency')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        axes[1].boxplot(data, vert=True)
        axes[1].set_title(f'Box Plot - {column}', fontsize=14, fontweight='bold')
        axes[1].set_ylabel(column)
        axes[1].grid(True, alpha=0.3)
        
        # KDE plot
        data.plot(kind='kde', ax=axes[2], color='green', linewidth=2)
        axes[2].set_title(f'KDE Plot - {column}', fontsize=14, fontweight='bold')
        axes[2].set_xlabel(column)
        axes[2].set_ylabel('Density')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        print(f"Error creating distribution plots: {e}")
        return None


def plot_correlation_matrix(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Create a correlation matrix heatmap for numeric columns.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        matplotlib Figure object
    """
    try:
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Create heatmap
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={'label': 'Correlation Coefficient'},
            ax=ax
        )
        
        ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        print(f"Error creating correlation matrix: {e}")
        return None


def plot_quality_dashboard(df: pd.DataFrame, results: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate quality metrics for dashboard display.
    
    Args:
        df: pandas DataFrame
        results: Dictionary containing quality check results
        
    Returns:
        Dictionary with quality metrics
    """
    metrics = {}
    
    # Completeness (percentage of non-missing values)
    if 'missing_values' in results:
        metrics['completeness'] = 100 - results['missing_values']['missing_percentage']
    else:
        metrics['completeness'] = 100.0
    
    # Uniqueness (percentage of non-duplicate records)
    if 'duplicates' in results:
        metrics['uniqueness'] = 100 - results['duplicates']['duplicate_percentage']
    else:
        metrics['uniqueness'] = 100.0
    
    # Validity (percentage of columns with correct data types)
    if 'data_types' in results:
        total_cols = len(df.columns)
        issues = len(results['data_types'].get('type_mismatches', []))
        metrics['validity'] = ((total_cols - issues) / total_cols) * 100
    else:
        metrics['validity'] = 100.0
    
    # Overall score (weighted average)
    metrics['overall_score'] = (
        metrics['completeness'] * 0.4 +
        metrics['uniqueness'] * 0.3 +
        metrics['validity'] * 0.3
    )
    
    return metrics


def plot_outliers(df: pd.DataFrame, column: str) -> Optional[plt.Figure]:
    """
    Create outlier visualization for a numeric column.
    
    Args:
        df: pandas DataFrame
        column: Column name to analyze
        
    Returns:
        matplotlib Figure object
    """
    try:
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        data = df[column].dropna()
        
        # Calculate IQR
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Box plot with outliers
        axes[0].boxplot(data, vert=True)
        axes[0].axhline(y=lower_bound, color='r', linestyle='--', label='Lower Bound')
        axes[0].axhline(y=upper_bound, color='r', linestyle='--', label='Upper Bound')
        axes[0].set_title(f'Box Plot with Outlier Bounds - {column}', fontsize=14, fontweight='bold')
        axes[0].set_ylabel(column)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Scatter plot showing outliers
        is_outlier = (data < lower_bound) | (data > upper_bound)
        
        axes[1].scatter(
            range(len(data)),
            data,
            c=['red' if x else 'blue' for x in is_outlier],
            alpha=0.6,
            s=50
        )
        axes[1].axhline(y=lower_bound, color='r', linestyle='--', label='Lower Bound')
        axes[1].axhline(y=upper_bound, color='r', linestyle='--', label='Upper Bound')
        axes[1].set_title(f'Outlier Detection - {column}', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Index')
        axes[1].set_ylabel(column)
        axes[1].legend(['Lower Bound', 'Upper Bound', 'Normal', 'Outlier'])
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        print(f"Error creating outlier plots: {e}")
        return None