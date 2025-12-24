"""
Visualizations Module
Handles all Plotly chart generation
"""
from typing import Dict, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import logging

logger = logging.getLogger(__name__)


def create_framework_pie_chart(metrics: Dict[str, Any]) -> go.Figure:
    """
    Create pie chart showing automation by framework

    Args:
        metrics: Dictionary containing framework metrics

    Returns:
        Plotly Figure object
    """
    try:
        framework_data = pd.DataFrame({
            'Framework': ['Java', 'Testim Desktop', 'Testim Mobile', 'Testim Both'],
            'Count': [
                metrics['automated_java'],
                metrics['automated_testim_desktop'],
                metrics['automated_testim_mobile'],
                metrics['automated_testim_both']
            ]
        })
        framework_data = framework_data[framework_data['Count'] > 0]

        if framework_data.empty:
            return go.Figure()

        fig = go.Figure(data=[go.Pie(
            labels=framework_data['Framework'],
            values=framework_data['Count'],
            hole=0.5,
            marker=dict(colors=['#636EFA', '#00CC96', '#FFA500', '#AB63FA']),
            textinfo='label+percent',
            textposition='outside'
        )])

        fig.update_layout(
            title_text="Automation by Framework",
            height=350,
            showlegend=True,
            annotations=[dict(
                text=f'{metrics["total_automated"]}<br>Total',
                x=0.5, y=0.5,
                font_size=20,
                showarrow=False
            )]
        )

        return fig

    except Exception as e:
        logger.error(f"Error creating framework pie chart: {e}")
        return go.Figure()


def create_testim_status_pie(metrics: Dict[str, Any]) -> go.Figure:
    """
    Create pie chart for Testim status distribution

    Args:
        metrics: Dictionary containing Testim metrics

    Returns:
        Plotly Figure object
    """
    try:
        testim_breakdown_data = pd.DataFrame({
            'Status': ['Automated', 'To Be Automated', 'Not Automated'],
            'Count': [
                metrics['total_testim'],
                metrics['to_be_automated'],
                metrics['not_automated']
            ]
        })

        fig = go.Figure(data=[go.Pie(
            labels=testim_breakdown_data['Status'],
            values=testim_breakdown_data['Count'],
            hole=0.4,
            marker=dict(colors=['#00CC96', '#FFA500', '#EF553B']),
            textinfo='label+value+percent',
            textposition='auto'
        )])

        fig.update_layout(
            title_text="Status Distribution",
            height=300,
            showlegend=False
        )

        return fig

    except Exception as e:
        logger.error(f"Error creating Testim status pie: {e}")
        return go.Figure()


def create_testim_device_bar(metrics: Dict[str, Any]) -> go.Figure:
    """
    Create bar chart for Testim device breakdown

    Args:
        metrics: Dictionary containing Testim device metrics

    Returns:
        Plotly Figure object
    """
    try:
        testim_device_data = pd.DataFrame({
            'Device': ['Desktop', 'Mobile', 'Both'],
            'Count': [metrics['desktop'], metrics['mobile'], metrics['both']]
        })

        fig = px.bar(
            testim_device_data,
            x='Device',
            y='Count',
            text='Count',
            color='Device',
            color_discrete_map={'Desktop': '#636EFA', 'Mobile': '#EF553B', 'Both': '#00CC96'},
            title="Automated Cases by Device"
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=250,
            yaxis_title="Number of Cases"
        )

        return fig

    except Exception as e:
        logger.error(f"Error creating Testim device bar chart: {e}")
        return go.Figure()


def create_device_totals_bar(df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart for total test cases by device

    Args:
        df: Filtered summary DataFrame

    Returns:
        Plotly Figure object
    """
    try:
        device_totals = df.groupby('Device')['Count'].sum().reset_index()

        fig = px.bar(
            device_totals,
            x='Device',
            y='Count',
            text_auto=True,
            color='Device',
            color_discrete_map={'Desktop': '#636EFA', 'Mobile': '#EF553B', 'Both': '#00CC96'},
            title="Test Cases by Device Type"
        )

        fig.update_layout(showlegend=False, height=300)
        return fig

    except Exception as e:
        logger.error(f"Error creating device totals bar: {e}")
        return go.Figure()


def create_device_status_stacked_bar(df: pd.DataFrame) -> go.Figure:
    """
    Create stacked bar chart for automation status by device

    Args:
        df: Filtered summary DataFrame

    Returns:
        Plotly Figure object
    """
    try:
        device_status = df.groupby(['Device', 'Status'])['Count'].sum().reset_index()

        fig = px.bar(
            device_status,
            x='Device',
            y='Count',
            color='Status',
            barmode='stack',
            text_auto=True,
            color_discrete_map={
                "Automated - Java": "#636EFA",
                "Automated - Testim Desktop": "#00CC96",
                "Automated - Testim Mobile": "#FFA500",
                "Automated - Testim Both": "#AB63FA",
                "To Be Automated": "#EF553B",
                "N/A": "#FEC8D8",
                "Not Automated": "#FECB52"
            },
            title="Automation Status by Device"
        )

        fig.update_layout(height=300)
        return fig

    except Exception as e:
        logger.error(f"Error creating device status stacked bar: {e}")
        return go.Figure()


def create_epic_top_bottom_bars(pivot: pd.DataFrame, top_n: int = 10) -> tuple[go.Figure, go.Figure]:
    """
    Create horizontal bar charts for top and bottom epics by coverage

    Args:
        pivot: Epic pivot DataFrame
        top_n: Number of epics to show in each chart

    Returns:
        Tuple of (top chart, bottom chart)
    """
    try:
        top_n_epics = pivot.head(top_n)
        bottom_n_epics = pivot.tail(top_n)

        # Top N chart
        fig_top = go.Figure()
        fig_top.add_trace(go.Bar(
            y=top_n_epics.index,
            x=top_n_epics['COVERAGE %'],
            orientation='h',
            marker=dict(
                color=top_n_epics['COVERAGE %'],
                colorscale='RdYlGn',
                cmin=0,
                cmax=100,
                showscale=False
            ),
            text=top_n_epics['COVERAGE %'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Coverage: %{x:.1f}%<br>Automated: ' +
                          top_n_epics['Automated'].astype(str) + '<br>Total: ' +
                          top_n_epics['TOTAL'].astype(str) + '<extra></extra>'
        ))

        fig_top.update_layout(
            height=400,
            xaxis_title="Coverage %",
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            xaxis_range=[0, 110],
            margin=dict(l=0, r=0, t=20, b=0)
        )

        # Bottom N chart
        fig_bottom = go.Figure()
        fig_bottom.add_trace(go.Bar(
            y=bottom_n_epics.index,
            x=bottom_n_epics['COVERAGE %'],
            orientation='h',
            marker=dict(
                color=bottom_n_epics['COVERAGE %'],
                colorscale='RdYlGn',
                cmin=0,
                cmax=100,
                showscale=False
            ),
            text=bottom_n_epics['COVERAGE %'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Coverage: %{x:.1f}%<br>Automated: ' +
                          bottom_n_epics['Automated'].astype(str) + '<br>Total: ' +
                          bottom_n_epics['TOTAL'].astype(str) + '<extra></extra>'
        ))

        fig_bottom.update_layout(
            height=400,
            xaxis_title="Coverage %",
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            xaxis_range=[0, 110],
            margin=dict(l=0, r=0, t=20, b=0)
        )

        return fig_top, fig_bottom

    except Exception as e:
        logger.error(f"Error creating epic bar charts: {e}")
        return go.Figure(), go.Figure()


def create_epic_complete_stacked_bar(pivot: pd.DataFrame) -> go.Figure:
    """
    Create comprehensive stacked bar chart for all epics

    Args:
        pivot: Epic pivot DataFrame

    Returns:
        Plotly Figure object
    """
    try:
        num_epics = len(pivot)
        chart_height = max(400, num_epics * 25)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=pivot.index,
            x=pivot['Automated'],
            name='Automated',
            orientation='h',
            marker=dict(color='#00CC96'),
            text=pivot['Automated'],
            textposition='inside'
        ))

        fig.add_trace(go.Bar(
            y=pivot.index,
            x=pivot['To Be Automated'],
            name='To Be Automated',
            orientation='h',
            marker=dict(color='#EF553B'),
            text=pivot['To Be Automated'],
            textposition='inside'
        ))

        fig.add_trace(go.Bar(
            y=pivot.index,
            x=pivot['Not Automated'],
            name='Not Automated',
            orientation='h',
            marker=dict(color='#636EFA'),
            text=pivot['Not Automated'],
            textposition='inside'
        ))

        fig.update_layout(
            barmode='stack',
            height=chart_height,
            yaxis={'categoryorder': 'array', 'categoryarray': pivot.index[::-1]},
            xaxis_title="Number of Test Cases",
            yaxis_title="Epic",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return fig

    except Exception as e:
        logger.error(f"Error creating epic complete stacked bar: {e}")
        return go.Figure()
