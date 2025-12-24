# QA Global Automation Coverage Dashboard

A modern, high-performance Streamlit dashboard for tracking test automation coverage across multiple business units using TestRail data.

## Overview

This dashboard provides comprehensive visibility into automation coverage across different frameworks (Java, Testim), devices (Desktop, Mobile, Both), and organizational epics. It features real-time data fetching, advanced filtering, and export capabilities.

### Key Features

- **Multi-Framework Support**: Track Java and Testim (Desktop/Mobile/Both) automation separately
- **Business Unit Coverage**: Support for 9 business units with individual configurations
- **Advanced Filtering**: Filter by Device, Country, and Priority
- **Epic-Level Tracking**: Detailed coverage metrics by epic with top/bottom performers
- **Data Export**: Export complete dashboard data or epic summaries to Excel
- **Performance Optimized**: Caching system for fast data loading and processing
- **Type-Safe**: Full type hints throughout the codebase
- **Well-Tested**: Comprehensive unit test suite

## Project Structure

```
coverage/
├── .devcontainer/           # Development container configuration
├── .streamlit/              # Streamlit secrets and configuration (git-ignored)
├── config/                  # Additional configuration files
├── modules/                 # Core application modules
│   ├── __init__.py
│   ├── config.py           # Business unit and mapping configurations
│   ├── connector.py        # TestRail API integration
│   ├── transformer.py      # Data transformation and processing
│   ├── metrics.py          # Metrics calculations
│   ├── visualizations.py   # Plotly chart generation
│   └── exporter.py         # Data export functionality
├── tests/                   # Unit test suite
│   ├── __init__.py
│   ├── test_transformer.py # Transformer module tests
│   └── test_metrics.py     # Metrics module tests
├── dashboard.py            # Main application entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.11 or higher
- TestRail account with API access
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   cd /path/to/your/projects
   git clone <repository-url>
   cd coverage
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure TestRail credentials**

   Create a `.streamlit/secrets.toml` file:
   ```bash
   mkdir .streamlit
   ```

   Add your TestRail credentials:
   ```toml
   [testrail]
   url = "https://your-instance.testrail.io"
   email = "your-email@company.com"
   api_key = "your-api-key-here"
   ```

5. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

## Configuration

### Business Units

Business units are configured in `modules/config.py`. Each BU requires:
- **name**: Display name
- **project_id**: TestRail project ID
- **suite_id**: TestRail suite ID

Example:
```python
"Microservices": BusinessUnitConfig(
    name="Microservices",
    project_id=17,
    suite_id=9570
)
```

### Country Mappings

Country ID mappings are defined in `COUNTRY_MAPPINGS` within `modules/config.py`:

```python
COUNTRY_MAPPINGS = {
    "Marionnaud": {
        '3': 'MRN',
        '9': 'MFR',
        # ... more mappings
    },
    "Drogas": {
        '5': 'LT',
        '6': 'LV',
        '7': 'RU'
    }
}
```

### Custom Field Names

The dashboard automatically detects TestRail custom field names using variations defined in `FIELD_VARIATIONS`. Add your custom field names to support different TestRail configurations.

## Usage

### Loading Data

1. Select a Business Unit from the dropdown
2. Click "Update Dashboard" to fetch and process data
3. Data is cached for 1 hour for performance

### Filtering

Use the multi-select filters to narrow down your view:
- **Device Type**: Desktop, Mobile, Both
- **Country**: Filter by specific countries
- **Priority**: Filter by priority levels (High, Highest, Medium)

Click "Reset Filters" to restore all filters to default.

### Viewing Metrics

The dashboard provides several metric views:

#### Overall Coverage Summary
- Total test cases and effective coverage percentage
- Framework breakdown (Java vs Testim)
- Automation status distribution

#### Testim Framework Breakdown
- Testim-specific coverage metrics
- Device-type breakdown (Desktop, Mobile, Both)
- Testim status distribution

#### Distribution by Device
- Test cases by device type
- Automation status by device
- Device-specific coverage percentages

#### Coverage by Epic
- Top 10 and Bottom 10 epics by coverage
- Epic search functionality
- Complete epic breakdown with stacked bar charts
- Epic statistics (average coverage, thresholds)

### Exporting Data

Two export options are available:

1. **Export Epic Coverage**: Excel file with epic-focused data
   - Summary sheet with overall metrics
   - Epic coverage details
   - Top 10 and Bottom 10 epics

2. **Export Complete Dashboard**: Comprehensive Excel file with all data
   - Summary metrics
   - Device metrics
   - Epic coverage
   - Raw filtered data

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=modules --cov-report=html

# Run specific test file
pytest tests/test_transformer.py -v
```

### Code Quality

The codebase follows these practices:
- **Type Hints**: All functions have type annotations
- **Logging**: Comprehensive logging throughout
- **Error Handling**: Graceful error handling with user feedback
- **Caching**: Strategic use of Streamlit caching for performance
- **Modularity**: Clean separation of concerns

### Adding a New Business Unit

1. Open `modules/config.py`
2. Add a new entry to `BU_CONFIG`:
   ```python
   "New BU Name": BusinessUnitConfig(
       name="New BU Name",
       project_id=XX,
       suite_id=YYYY
   )
   ```
3. If the BU has custom country mappings, add them to `COUNTRY_MAPPINGS`
4. Restart the dashboard

### Adding Custom Metrics

1. Add calculation logic to `modules/metrics.py`
2. Add visualization in `modules/visualizations.py`
3. Integrate into `dashboard.py` render functions
4. Add unit tests in `tests/test_metrics.py`

## Performance Optimization

The dashboard uses several optimization techniques:

- **@st.cache_data**: Caches API responses and data processing (1-hour TTL)
- **@st.cache_resource**: Caches API client connection
- **Pagination**: Fetches data in batches of 250 records
- **Efficient Grouping**: Pandas groupby operations for aggregations
- **Session State**: Maintains state between reruns

## Troubleshooting

### Common Issues

**Issue**: "Missing credential in secrets.toml"
- **Solution**: Ensure `.streamlit/secrets.toml` exists with correct TestRail credentials

**Issue**: "No test cases found in this suite"
- **Solution**: Verify project_id and suite_id are correct for the selected BU

**Issue**: "Processing Error"
- **Solution**: Check that required custom fields exist in TestRail (check logs for specific field names)

**Issue**: Dashboard is slow
- **Solution**: Data is cached for 1 hour. Clear cache: Click "C" in Streamlit menu → Clear Cache

### Logging

Logs are output to console with timestamps. Set logging level in `dashboard.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # For detailed logs
```

## Architecture

### Data Flow

1. **Fetch**: `connector.py` fetches raw data from TestRail API
2. **Transform**: `transformer.py` processes and maps data
3. **Calculate**: `metrics.py` computes coverage metrics
4. **Visualize**: `visualizations.py` creates Plotly charts
5. **Render**: `dashboard.py` orchestrates UI rendering
6. **Export**: `exporter.py` generates Excel exports

### Caching Strategy

- **API Client**: Cached at resource level (never expires)
- **Raw Data**: Cached for 1 hour with project/suite as key
- **Processed Data**: Cached for 1 hour with BU name as key
- **Metrics**: Cached for 30 minutes with filtered data hash as key

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Add docstrings to modules and functions
- Write unit tests for new functionality
- Update README for new features

### Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Run test suite
5. Update documentation
6. Submit pull request

## License

[Add your license information here]

## Support

For issues, questions, or contributions:
- **Issues**: [Add issue tracker link]
- **Documentation**: This README and inline code comments
- **Contact**: [Add contact information]

## Changelog

### Version 2.0.0 (Current - "coverage" project)
- Complete refactor with modular architecture
- Added comprehensive type hints
- Implemented unit test suite
- Added Excel export functionality
- Improved error handling and logging
- Performance optimizations with caching
- Enhanced Priority filter (fully functional)
- Better code documentation

### Version 1.0.0 (Original "Dashboard" project)
- Initial implementation
- Basic dashboard functionality
- Multi-BU support
- Epic tracking
- Testim metrics

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [TestRail API](https://www.gurock.com/testrail/) - Test management integration
