"""
Data Transformation Module
Handles mapping and processing of TestRail data
"""
from typing import Optional, Any, Union
import pandas as pd
import numpy as np
import streamlit as st
import logging
from .config import (
    COUNTRY_MAPPINGS,
    PRIORITY_MAPPINGS,
    DEVICE_MAPPINGS,
    JAVA_STATUS_MAPPINGS,
    TESTIM_STATUS_MAPPINGS,
    FIELD_VARIATIONS
)
from .constants import CACHE_TTL_DATA

logger = logging.getLogger(__name__)


def _map_field_value(val: Any, mapping: dict[Any, str], default: str = "Unknown") -> str:
    """
    Generic field value mapper

    Args:
        val: Value to map
        mapping: Mapping dictionary
        default: Default value if not found

    Returns:
        Mapped value or default
    """
    if pd.isna(val):
        return default

    # Try direct lookup
    if val in mapping:
        return mapping[val]

    # Try as integer
    try:
        val_int = int(float(val))
        if val_int in mapping:
            return mapping[val_int]
    except (ValueError, TypeError):
        pass

    return default


def map_country_id(val: Any, bu_name: str = "Marionnaud") -> str:
    """
    Map country IDs to readable country codes

    Args:
        val: Country ID or list of IDs
        bu_name: Business unit name for specific mapping

    Returns:
        Mapped country code(s) or 'Unknown'
    """
    country_map = COUNTRY_MAPPINGS.get(bu_name, {})

    if isinstance(val, (list, tuple, np.ndarray)):
        if len(val) == 0:
            return 'Unknown'
        mapped = [country_map.get(str(v).strip(), f'ID_{v}') for v in val]
        return ', '.join(mapped)

    if pd.isna(val):
        return 'Unknown'

    val_str = str(val).strip()

    if val_str in country_map:
        return country_map[val_str]

    try:
        val_int = int(float(val_str))
        val_key = str(val_int)
        if val_key in country_map:
            return country_map[val_key]
    except (ValueError, TypeError):
        pass

    return f'ID_{val_str}'


def map_priority(val: Any) -> str:
    """
    Map priority IDs to readable priority levels

    Args:
        val: Priority ID

    Returns:
        Mapped priority level or 'Unknown'
    """
    if pd.isna(val):
        return 'Unknown'

    try:
        val_int = int(float(val))
    except (ValueError, TypeError):
        val_str = str(val).strip().lower()
        if 'highest' in val_str:
            return 'Highest'
        elif 'high' in val_str:
            return 'High'
        elif 'medium' in val_str:
            return 'Medium'
        return 'Unknown'

    return PRIORITY_MAPPINGS.get(val_int, 'Unknown')


def map_device_status(val: Any) -> str:
    """Map device type IDs to readable device names"""
    return _map_field_value(val, DEVICE_MAPPINGS, "Both")


def map_automation_status_java(val: Any) -> Optional[str]:
    """Map Java automation status IDs to readable status"""
    if pd.isna(val):
        return None
    try:
        val_int = int(float(val))
        return JAVA_STATUS_MAPPINGS.get(val_int)
    except (ValueError, TypeError):
        return None


def map_automation_status_testim(val: Any) -> Optional[str]:
    """Map Testim automation status IDs to readable status"""
    if pd.isna(val):
        return None
    try:
        val_int = int(float(val))
        return TESTIM_STATUS_MAPPINGS.get(val_int)
    except (ValueError, TypeError):
        return None


def determine_final_status(row: pd.Series) -> str:
    """
    Determine final automation status based on Java and Testim statuses
    Priority: Testim > Java

    Args:
        row: DataFrame row containing status fields

    Returns:
        Final automation status
    """
    java_status = row.get('Java_Status')
    testim_desktop = row.get('Testim_Desktop_Status')
    testim_mobile = row.get('Testim_Mobile_Status')

    testim_desktop_automated = testim_desktop == "Automated"
    testim_mobile_automated = testim_mobile == "Automated"
    java_automated = java_status == "Automated"

    # Check for Testim automation (highest priority)
    if testim_desktop_automated and testim_mobile_automated:
        return "Automated - Testim Both"
    elif testim_desktop_automated and java_automated:
        return "Automated - Testim Desktop"
    elif testim_mobile_automated and java_automated:
        return "Automated - Testim Mobile"
    elif testim_desktop_automated:
        return "Automated - Testim Desktop"
    elif testim_mobile_automated:
        return "Automated - Testim Mobile"
    elif java_automated:
        return "Automated - Java"

    # Check for N/A status
    if java_status == "N/A" or testim_desktop == "N/A" or testim_mobile == "N/A":
        return "N/A"

    # Check for To Be Automated
    if java_status == "To Be Automated" or testim_desktop == "To Be Automated" or testim_mobile == "To Be Automated":
        return "To Be Automated"

    return "Not Automated"


def find_field(df: pd.DataFrame, field_type: str) -> Optional[str]:
    """
    Find the correct field name from possible variations

    Args:
        df: DataFrame to search
        field_type: Type of field to find (java, testim_desktop, etc.)

    Returns:
        Field name if found, None otherwise
    """
    possible_fields = FIELD_VARIATIONS.get(field_type, [])

    for field in possible_fields:
        if field in df.columns:
            logger.debug(f"Found {field_type} field: {field}")
            return field

    logger.warning(f"No {field_type} field found in columns")
    return None


@st.cache_data(ttl=CACHE_TTL_DATA, show_spinner=False)
def process(df: pd.DataFrame, bu_name: str = "Marionnaud") -> pd.DataFrame:
    """
    Process raw TestRail data and create summary DataFrame

    Args:
        df: Raw DataFrame from TestRail
        bu_name: Business unit name for country mapping

    Returns:
        Processed and summarized DataFrame
    """
    if df.empty:
        logger.error("Empty DataFrame provided for processing")
        st.error("❌ No data to process")
        return pd.DataFrame()

    try:
        logger.info(f"Starting data processing for {bu_name}")
        logger.debug(f"Input DataFrame shape: {df.shape}")

        # Find field names
        java_field = find_field(df, "java")
        testim_desktop_field = find_field(df, "testim_desktop")
        testim_mobile_field = find_field(df, "testim_mobile")

        if not java_field:
            logger.error("Java automation status field not found")
            st.error("❌ Java automation status field not found")
            return pd.DataFrame()

        # Map automation statuses
        df['Java_Status'] = df[java_field].apply(map_automation_status_java)

        if testim_desktop_field:
            df['Testim_Desktop_Status'] = df[testim_desktop_field].apply(map_automation_status_testim)
        else:
            df['Testim_Desktop_Status'] = None
            logger.warning("Testim Desktop field not found, defaulting to None")

        if testim_mobile_field:
            df['Testim_Mobile_Status'] = df[testim_mobile_field].apply(map_automation_status_testim)
        else:
            df['Testim_Mobile_Status'] = None
            logger.warning("Testim Mobile field not found, defaulting to None")

        # Determine final status
        df['Status'] = df.apply(determine_final_status, axis=1)

        # Map Epic
        epic_field = find_field(df, "epic")
        if epic_field:
            df['Epic'] = df[epic_field].fillna('No Epic Assigned').astype(str)
        else:
            df['Epic'] = 'No Epic Assigned'
            logger.warning("Epic field not found, using default")

        # Map Device
        device_field = find_field(df, "device")
        if device_field:
            df['Device'] = df[device_field].apply(map_device_status)
        else:
            df['Device'] = 'Both'
            logger.warning("Device field not found, defaulting to 'Both'")

        # Map Country
        country_field = find_field(df, "country")
        if country_field:
            df['Country'] = df[country_field].apply(lambda x: map_country_id(x, bu_name))
        else:
            df['Country'] = 'Unknown'
            logger.warning("Country field not found, defaulting to 'Unknown'")

        # Map Priority
        priority_field = find_field(df, "priority")
        if priority_field:
            df['Priority'] = df[priority_field].apply(map_priority)
        else:
            df['Priority'] = 'Unknown'
            logger.warning("Priority field not found, defaulting to 'Unknown'")

        # Create summary
        summary = df.groupby(
            ['Epic', 'Status', 'Device', 'Country', 'Priority'],
            dropna=False
        ).size().reset_index(name='Count')

        logger.info(f"Processing complete. Output shape: {summary.shape}")
        return summary

    except Exception as e:
        logger.error(f"Processing Error: {e}", exc_info=True)
        st.error(f"❌ Processing Error: {e}")
        import traceback
        st.code(traceback.format_exc())
        return pd.DataFrame()
