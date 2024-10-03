import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def plot_count_plot(df: pd.DataFrame, column_name: str, color_column: str = None) -> px.histogram:
    """
    Generate a count plot for a specified column in the DataFrame using Plotly.
    
    Parameters
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column_name : str
        The name of the column for which to create the count plot.
    color_column : str optional
        The name of the column used for facet differentiation. Default
        
    Returns
    -----------
    plotly.graph_objs._figure.Figure
        The Plotly figure object representing the count plot.
    """
    category_order = df[column_name].value_counts().index.tolist()

    if color_column is None:
        fig = px.histogram(df, x= column_name, title = f'Count Plot of {column_name}', category_orders = 
                       {column_name : category_order})
    else:
        print(color_column)
        unique_values = df[color_column].unique()
        num_plots = len(unique_values)

        # Create subplots
        fig = make_subplots(rows = 1, cols = num_plots, shared_yaxes = False, subplot_titles = [str(val) for val in unique_values])

        # Add traces to subplots
        for i, value in enumerate(unique_values):
            filtered_df = df[df[color_column] == value]
            fig.add_trace(
                go.histogram(x=filtered_df[column_name], name=str(value)),
                row = 1, col = i+1
            )

        # Update layout to synchronize x-axes order
        for i in range(num_plots):
            fig.update_xaxes(categoryorder = 'array', categoryarray = category_order, row = 1, col = i+1)

        fig.update_layout(title_text = f'Count Plot of {column_name} by {color_column}')

    return fig

def plot_histogram(df: pd.DataFrame, column_name: str) -> px.histogram:
    """
    Generate a histogram for a specified column in the DataFrame using Plotly.
    
    Parameters
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column_name : str
        The name of the column for which to create the histogram.
        
    Returns
    -----------
    plotly.graph_objs._figure.Figure
        The Plotly figure object representing the histogram.
    """
    fig = px.histogram(df, x= column_name, title = f'Histogram of {column_name}')
    return fig

def plot_dataframe(df: pd.DataFrame) -> None:
    """
    Generate and display count plots or histograms for all columns in the DataFrame.
    For numeric columns, generate histograms.
    For categorical columns, generate count plots.
    
    Parameters
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data.

    Returns
    -----------
    None
    """
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            fig = plot_histogram(df, column)
        elif pd.api.types.is_object_dtype(df[column]):
            fig = plot_count_plot(df, column)
        else:
            continue
        fig.show()
