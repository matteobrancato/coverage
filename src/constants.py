"""
Application Constants
Centralized constants for the QA Coverage Dashboard
"""

# Cache TTL (Time To Live) in seconds
CACHE_TTL_DATA = 3600  # 1 hour - for raw data and transformations
CACHE_TTL_METRICS = 1800  # 30 minutes - for calculated metrics

# API Configuration
API_BATCH_SIZE = 250  # Number of records to fetch per API call

# Application Metadata
APP_VERSION = "2.0.0"
APP_NAME = "QA Coverage Dashboard"

# Health Check
HEALTH_CHECK_QUERY_PARAM = "health"
HEALTH_CHECK_VALUE = "check"
