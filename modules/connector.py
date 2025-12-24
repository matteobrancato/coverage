"""
TestRail API Connector Module
Handles authentication and data fetching from TestRail
"""
from typing import Optional, Dict, Any
import pandas as pd
import streamlit as st
from testrail_api import TestRailAPI
import logging

logger = logging.getLogger(__name__)


@st.cache_resource
def get_api_client() -> Optional[TestRailAPI]:
    """
    Get authenticated TestRail API client with credentials from secrets

    Returns:
        TestRailAPI client instance or None if authentication fails
    """
    try:
        creds = st.secrets["testrail"]
        client = TestRailAPI(creds["url"], creds["email"], creds["api_key"])
        logger.info("TestRail API client initialized successfully")
        return client
    except KeyError as e:
        error_msg = f"Missing credential in secrets.toml: {e}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except Exception as e:
        error_msg = f"API Connection Failed: {e}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_data_recursive(project_id: int, suite_id: int) -> pd.DataFrame:
    """
    Fetch all test cases from TestRail with pagination

    Args:
        project_id: TestRail project ID
        suite_id: TestRail suite ID

    Returns:
        DataFrame containing all test cases
    """
    api = get_api_client()
    if not api:
        logger.error("API client not available")
        return pd.DataFrame()

    all_cases = []
    offset = 0
    limit = 250

    status_bar = st.empty()

    try:
        logger.info(f"Starting data fetch for project {project_id}, suite {suite_id}")

        while True:
            status_bar.text(f"🔍 Fetching cases {offset} to {offset + limit}...")

            response = api.cases.get_cases(
                project_id=project_id,
                suite_id=suite_id,
                limit=limit,
                offset=offset
            )

            batch = response.get('cases', []) if isinstance(response, dict) else response

            if not batch:
                break

            all_cases.extend(batch)
            logger.debug(f"Fetched {len(batch)} cases (offset: {offset})")

            if len(batch) < limit:
                break

            offset += limit

        status_bar.empty()

        if not all_cases:
            warning_msg = "No test cases found in this suite"
            logger.warning(warning_msg)
            st.warning(f"⚠️ {warning_msg}")
            return pd.DataFrame()

        logger.info(f"Successfully fetched {len(all_cases)} test cases")
        return pd.DataFrame(all_cases)

    except Exception as e:
        status_bar.empty()
        error_msg = f"Fetch Error: {e}"
        logger.error(error_msg, exc_info=True)
        st.error(f"❌ {error_msg}")
        return pd.DataFrame()


def validate_credentials() -> bool:
    """
    Validate TestRail credentials without making API calls

    Returns:
        True if credentials are configured, False otherwise
    """
    try:
        creds = st.secrets["testrail"]
        required_keys = ["url", "email", "api_key"]

        for key in required_keys:
            if key not in creds:
                logger.error(f"Missing required credential: {key}")
                return False

        return True
    except Exception as e:
        logger.error(f"Credential validation failed: {e}")
        return False
