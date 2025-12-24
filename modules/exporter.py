"""
Data Export Module
Handles exporting data to various formats (CSV, Excel)
"""
from typing import Dict, Any
import pandas as pd
import io
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def export_to_csv(df: pd.DataFrame, filename_prefix: str = "coverage_data") -> bytes:
    """
    Export DataFrame to CSV format

    Args:
        df: DataFrame to export
        filename_prefix: Prefix for the filename

    Returns:
        CSV data as bytes
    """
    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=True)
        logger.info(f"Successfully exported {len(df)} rows to CSV")
        return csv_buffer.getvalue().encode('utf-8')
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        raise


def export_epic_data_to_excel(
    pivot: pd.DataFrame,
    summary_metrics: Dict[str, Any],
    bu_name: str
) -> bytes:
    """
    Export epic coverage data to Excel with multiple sheets

    Args:
        pivot: Epic pivot DataFrame
        summary_metrics: Overall summary metrics
        bu_name: Business unit name

    Returns:
        Excel file as bytes
    """
    try:
        output = io.BytesIO()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Summary sheet
            summary_df = pd.DataFrame({
                'Metric': [
                    'Business Unit',
                    'Report Generated',
                    'Total Test Cases',
                    'Total Automated',
                    'Effective Coverage %',
                    'Java Automated',
                    'Testim Automated',
                    'To Be Automated',
                    'Not Automated',
                    'Not Applicable'
                ],
                'Value': [
                    bu_name,
                    timestamp,
                    f"{summary_metrics.get('total', 0):,}",
                    f"{summary_metrics.get('total_automated', 0):,}",
                    f"{summary_metrics.get('coverage', 0):.1f}%",
                    f"{summary_metrics.get('automated_java', 0):,}",
                    f"{summary_metrics.get('total_testim', 0):,}",
                    f"{summary_metrics.get('to_be_automated', 0):,}",
                    f"{summary_metrics.get('not_automated', 0):,}",
                    f"{summary_metrics.get('not_applicable', 0):,}"
                ]
            })
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Epic details sheet
            epic_export = pivot[['Automated', 'To Be Automated', 'Not Automated', 'N/A', 'TOTAL', 'COVERAGE %']].copy()
            epic_export.to_excel(writer, sheet_name='Epic Coverage')

            # Top 10 epics
            top_10 = pivot.head(10)[['COVERAGE %', 'Automated', 'TOTAL']]
            top_10.to_excel(writer, sheet_name='Top 10 Epics')

            # Bottom 10 epics
            bottom_10 = pivot.tail(10)[['COVERAGE %', 'Automated', 'TOTAL']]
            bottom_10.to_excel(writer, sheet_name='Bottom 10 Epics')

        logger.info(f"Successfully exported epic data to Excel for {bu_name}")
        output.seek(0)
        return output.getvalue()

    except Exception as e:
        logger.error(f"Error exporting to Excel: {e}")
        raise


def export_complete_data_to_excel(
    df_summary: pd.DataFrame,
    pivot: pd.DataFrame,
    overall_metrics: Dict[str, Any],
    testim_metrics: Dict[str, Any],
    device_metrics: Dict[str, Dict[str, Any]],
    bu_name: str
) -> bytes:
    """
    Export complete dashboard data to Excel with all sheets

    Args:
        df_summary: Complete summary DataFrame
        pivot: Epic pivot DataFrame
        overall_metrics: Overall metrics dictionary
        testim_metrics: Testim metrics dictionary
        device_metrics: Device metrics dictionary
        bu_name: Business unit name

    Returns:
        Excel file as bytes
    """
    try:
        output = io.BytesIO()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = {
                'Metric': [],
                'Value': []
            }

            # Overall metrics
            summary_data['Metric'].extend([
                'Business Unit',
                'Report Generated',
                '',
                '=== OVERALL METRICS ===',
                'Total Test Cases',
                'Effective Total',
                'Total Automated',
                'Coverage %',
                '',
                '=== BY FRAMEWORK ===',
                'Java Automated',
                'Testim Automated (Total)',
                'Testim Desktop',
                'Testim Mobile',
                'Testim Both',
                '',
                '=== STATUS BREAKDOWN ===',
                'To Be Automated',
                'Not Automated',
                'Not Applicable'
            ])

            summary_data['Value'].extend([
                bu_name,
                timestamp,
                '',
                '',
                f"{overall_metrics.get('total', 0):,}",
                f"{overall_metrics.get('effective_total', 0):,}",
                f"{overall_metrics.get('total_automated', 0):,}",
                f"{overall_metrics.get('coverage', 0):.1f}%",
                '',
                '',
                f"{overall_metrics.get('automated_java', 0):,}",
                f"{overall_metrics.get('total_testim', 0):,}",
                f"{overall_metrics.get('automated_testim_desktop', 0):,}",
                f"{overall_metrics.get('automated_testim_mobile', 0):,}",
                f"{overall_metrics.get('automated_testim_both', 0):,}",
                '',
                '',
                f"{overall_metrics.get('to_be_automated', 0):,}",
                f"{overall_metrics.get('not_automated', 0):,}",
                f"{overall_metrics.get('not_applicable', 0):,}"
            ])

            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Device metrics sheet
            device_data = []
            for device_name, metrics in device_metrics.items():
                device_data.append({
                    'Device': device_name,
                    'Automated': metrics['automated'],
                    'Total': metrics['total'],
                    'Coverage %': f"{metrics['coverage']:.1f}%"
                })
            device_df = pd.DataFrame(device_data)
            device_df.to_excel(writer, sheet_name='Device Metrics', index=False)

            # Epic coverage
            epic_export = pivot[['Automated', 'To Be Automated', 'Not Automated', 'N/A', 'TOTAL', 'COVERAGE %']].copy()
            epic_export.to_excel(writer, sheet_name='Epic Coverage')

            # Raw data
            df_summary.to_excel(writer, sheet_name='Raw Data', index=False)

        logger.info(f"Successfully exported complete data to Excel for {bu_name}")
        output.seek(0)
        return output.getvalue()

    except Exception as e:
        logger.error(f"Error exporting complete data to Excel: {e}")
        raise


def get_export_filename(bu_name: str, export_type: str = "coverage") -> str:
    """
    Generate export filename with timestamp

    Args:
        bu_name: Business unit name
        export_type: Type of export (coverage, epic, complete)

    Returns:
        Formatted filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bu_clean = bu_name.replace(" ", "_")
    return f"{export_type}_{bu_clean}_{timestamp}"
