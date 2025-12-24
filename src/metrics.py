"""
Metrics Calculation Module
Handles all coverage and automation metrics calculations
"""
from typing import Dict, Any, Tuple, TypeAlias
import pandas as pd
import streamlit as st
import logging
from .constants import CACHE_TTL_METRICS

# Type Aliases
MetricsDict: TypeAlias = Dict[str, Any]
EpicMetrics: TypeAlias = Tuple[pd.DataFrame, Dict[str, float]]

logger = logging.getLogger(__name__)


@st.cache_data(ttl=CACHE_TTL_METRICS, show_spinner=False)
def calculate_overall_metrics(df: pd.DataFrame) -> MetricsDict:
    """
    Calculate overall coverage metrics from summary DataFrame

    Args:
        df: Filtered summary DataFrame

    Returns:
        Dictionary containing all calculated metrics
    """
    try:
        total = df['Count'].sum()

        # Calculate automated counts by framework
        automated_java = df[df['Status'] == 'Automated - Java']['Count'].sum()
        automated_testim_desktop = df[df['Status'] == 'Automated - Testim Desktop']['Count'].sum()
        automated_testim_mobile = df[df['Status'] == 'Automated - Testim Mobile']['Count'].sum()
        automated_testim_both = df[df['Status'] == 'Automated - Testim Both']['Count'].sum()

        total_automated = automated_java + automated_testim_desktop + automated_testim_mobile + automated_testim_both
        total_testim = automated_testim_desktop + automated_testim_mobile + automated_testim_both

        # Calculate other status counts
        to_be_automated = df[df['Status'] == 'To Be Automated']['Count'].sum()
        not_applicable = df[df['Status'] == 'N/A']['Count'].sum()
        not_automated = df[df['Status'] == 'Not Automated']['Count'].sum()

        # Calculate coverage
        effective_total = total - not_applicable
        coverage = (total_automated / effective_total * 100) if effective_total > 0 else 0

        metrics = {
            'total': total,
            'automated_java': automated_java,
            'automated_testim_desktop': automated_testim_desktop,
            'automated_testim_mobile': automated_testim_mobile,
            'automated_testim_both': automated_testim_both,
            'total_automated': total_automated,
            'total_testim': total_testim,
            'to_be_automated': to_be_automated,
            'not_applicable': not_applicable,
            'not_automated': not_automated,
            'effective_total': effective_total,
            'coverage': coverage
        }

        logger.debug(f"Calculated overall metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error calculating overall metrics: {e}", exc_info=True)
        return {}


@st.cache_data(ttl=CACHE_TTL_METRICS, show_spinner=False)
def calculate_testim_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate Testim-specific metrics

    Args:
        df: Filtered summary DataFrame

    Returns:
        Dictionary containing Testim metrics
    """
    try:
        automated_testim_desktop = df[df['Status'] == 'Automated - Testim Desktop']['Count'].sum()
        automated_testim_mobile = df[df['Status'] == 'Automated - Testim Mobile']['Count'].sum()
        automated_testim_both = df[df['Status'] == 'Automated - Testim Both']['Count'].sum()

        total_testim = automated_testim_desktop + automated_testim_mobile + automated_testim_both

        testim_total = total_testim + df[
            (df['Status'] == 'To Be Automated') |
            (df['Status'] == 'Not Automated')
        ]['Count'].sum()

        testim_coverage = (total_testim / testim_total * 100) if testim_total > 0 else 0

        # Calculate device percentages
        desktop_pct = (automated_testim_desktop / total_testim * 100) if total_testim > 0 else 0
        mobile_pct = (automated_testim_mobile / total_testim * 100) if total_testim > 0 else 0
        both_pct = (automated_testim_both / total_testim * 100) if total_testim > 0 else 0

        metrics = {
            'testim_total': testim_total,
            'total_testim': total_testim,
            'testim_coverage': testim_coverage,
            'desktop': automated_testim_desktop,
            'mobile': automated_testim_mobile,
            'both': automated_testim_both,
            'desktop_pct': desktop_pct,
            'mobile_pct': mobile_pct,
            'both_pct': both_pct,
            'to_be_automated': df[df['Status'] == 'To Be Automated']['Count'].sum(),
            'not_automated': df[df['Status'] == 'Not Automated']['Count'].sum()
        }

        logger.debug(f"Calculated Testim metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error calculating Testim metrics: {e}", exc_info=True)
        return {}


@st.cache_data(ttl=CACHE_TTL_METRICS, show_spinner=False)
def calculate_device_metrics(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Calculate coverage metrics by device type

    Args:
        df: Filtered summary DataFrame

    Returns:
        Dictionary containing device-specific metrics
    """
    try:
        device_metrics = {}

        for device in ['Desktop', 'Mobile', 'Both']:
            device_data = df[df['Device'] == device]
            device_automated = device_data[device_data['Status'].str.contains('Automated -', na=False)]['Count'].sum()
            device_total = device_data['Count'].sum()
            device_coverage = (device_automated / device_total * 100) if device_total > 0 else 0

            device_metrics[device] = {
                'automated': device_automated,
                'total': device_total,
                'coverage': device_coverage
            }

        logger.debug(f"Calculated device metrics: {device_metrics}")
        return device_metrics

    except Exception as e:
        logger.error(f"Error calculating device metrics: {e}", exc_info=True)
        return {}


@st.cache_data(ttl=CACHE_TTL_METRICS, show_spinner=False)
def calculate_epic_metrics(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Calculate epic-level coverage metrics

    Args:
        df: Filtered summary DataFrame

    Returns:
        Tuple of (epic pivot DataFrame, epic statistics)
    """
    try:
        epic_summary = df.groupby(['Epic', 'Status'])['Count'].sum().reset_index()

        def aggregate_epic_status(group):
            automated_count = group[group['Status'].str.contains('Automated -', na=False)]['Count'].sum()
            to_be_count = group[group['Status'] == 'To Be Automated']['Count'].sum()
            na_count = group[group['Status'] == 'N/A']['Count'].sum()
            not_auto_count = group[group['Status'] == 'Not Automated']['Count'].sum()
            total = group['Count'].sum()

            return pd.Series({
                'Automated': automated_count,
                'To Be Automated': to_be_count,
                'N/A': na_count,
                'Not Automated': not_auto_count,
                'TOTAL': total
            })

        pivot = epic_summary.groupby('Epic').apply(aggregate_epic_status).reset_index()
        pivot.set_index('Epic', inplace=True)

        pivot['EFFECTIVE TOTAL'] = pivot['TOTAL'] - pivot['N/A']
        pivot['COVERAGE %'] = ((pivot['Automated'] / pivot['EFFECTIVE TOTAL']) * 100).round(1)
        pivot['COVERAGE %'] = pivot['COVERAGE %'].fillna(0).replace([float('inf')], 0)
        pivot = pivot.sort_values(by='COVERAGE %', ascending=False)

        # Calculate statistics
        num_epics = len(pivot)
        avg_coverage = pivot['COVERAGE %'].mean()
        epics_above_50 = len(pivot[pivot['COVERAGE %'] >= 50])
        epics_below_30 = len(pivot[pivot['COVERAGE %'] < 30])

        stats = {
            'num_epics': num_epics,
            'avg_coverage': avg_coverage,
            'epics_above_50': epics_above_50,
            'epics_below_30': epics_below_30
        }

        logger.debug(f"Calculated epic metrics for {num_epics} epics")
        return pivot, stats

    except Exception as e:
        logger.error(f"Error calculating epic metrics: {e}", exc_info=True)
        return pd.DataFrame(), {}


def filter_epic_by_search(pivot: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """
    Filter epic pivot by search term

    Args:
        pivot: Epic pivot DataFrame
        search_term: Search string

    Returns:
        Filtered DataFrame
    """
    if not search_term:
        return pivot

    try:
        return pivot[pivot.index.str.contains(search_term, case=False, na=False)]
    except Exception as e:
        logger.error(f"Error filtering epics: {e}")
        return pivot
