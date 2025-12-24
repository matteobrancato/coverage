"""
TestRail API Connector Module
Handles authentication and data fetching from TestRail
"""
from typing import Optional, Dict, Any
import os
import pandas as pd
import streamlit as st
from testrail_api import TestRailAPI
import logging
from .constants import CACHE_TTL_DATA, API_BATCH_SIZE

logger = logging.getLogger(__name__)


def _get_credentials() -> Dict[str, str]:
    """
    Get TestRail credentials from Streamlit secrets or environment variables

    Returns:
        Dictionary with url, email, and api_key

    Raises:
        KeyError: If credentials are not found in either source
    """
    try:
        # Try Streamlit secrets first
        creds = st.secrets["testrail"]
        return {
            "url": creds["url"],
            "email": creds["email"],
            "api_key": creds["api_key"]
        }
    except (KeyError, FileNotFoundError):
        # Fall back to environment variables
        logger.info("Streamlit secrets not found, trying environment variables")
        url = os.getenv("TESTRAIL_URL")
        email = os.getenv("TESTRAIL_EMAIL")
        api_key = os.getenv("TESTRAIL_API_KEY")

        if not all([url, email, api_key]):
            raise KeyError(
                "TestRail credentials not found in secrets.toml or environment variables. "
                "Set TESTRAIL_URL, TESTRAIL_EMAIL, and TESTRAIL_API_KEY environment variables, "
                "or configure .streamlit/secrets.toml"
            )

        return {"url": url, "email": email, "api_key": api_key}


@st.cache_resource
def get_api_client() -> Optional[TestRailAPI]:
    """
    Get authenticated TestRail API client with credentials

    Credentials are loaded from:
    1. Streamlit secrets (.streamlit/secrets.toml) - preferred
    2. Environment variables (TESTRAIL_URL, TESTRAIL_EMAIL, TESTRAIL_API_KEY) - fallback

    Returns:
        TestRailAPI client instance or None if authentication fails
    """
    try:
        creds = _get_credentials()
        client = TestRailAPI(creds["url"], creds["email"], creds["api_key"])
        logger.info("TestRail API client initialized successfully")
        return client
    except KeyError as e:
        error_msg = f"Credential error: {e}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except Exception as e:
        error_msg = f"API Connection Failed: {e}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None


@st.cache_data(ttl=CACHE_TTL_DATA, show_spinner=False)
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
    limit = API_BATCH_SIZE

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
