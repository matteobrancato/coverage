"""
Unit tests for metrics module
"""
import pytest
import pandas as pd
from src.metrics import (
    calculate_overall_metrics,
    calculate_testim_metrics,
    calculate_device_metrics,
    filter_epic_by_search
)


@pytest.fixture
def sample_summary_df():
    """Create sample summary DataFrame for testing"""
    return pd.DataFrame({
        'Epic': ['Epic1', 'Epic1', 'Epic2', 'Epic2', 'Epic3'],
        'Status': [
            'Automated - Java',
            'Automated - Testim Desktop',
            'To Be Automated',
            'Not Automated',
            'N/A'
        ],
        'Device': ['Desktop', 'Desktop', 'Mobile', 'Both', 'Desktop'],
        'Country': ['MRN', 'MFR', 'MRN', 'MRN', 'Unknown'],
        'Priority': ['High', 'Highest', 'Medium', 'High', 'Unknown'],
        'Count': [10, 20, 15, 5, 8]
    })


class TestOverallMetrics:
    """Tests for calculate_overall_metrics function"""

    def test_total_calculation(self, sample_summary_df):
        metrics = calculate_overall_metrics(sample_summary_df)
        assert metrics['total'] == 58

    def test_automated_counts(self, sample_summary_df):
        metrics = calculate_overall_metrics(sample_summary_df)
        assert metrics['automated_java'] == 10
        assert metrics['automated_testim_desktop'] == 20
        assert metrics['total_automated'] == 30

    def test_other_status_counts(self, sample_summary_df):
        metrics = calculate_overall_metrics(sample_summary_df)
        assert metrics['to_be_automated'] == 15
        assert metrics['not_automated'] == 5
        assert metrics['not_applicable'] == 8

    def test_coverage_calculation(self, sample_summary_df):
        metrics = calculate_overall_metrics(sample_summary_df)
        # Total = 58, N/A = 8, Effective = 50, Automated = 30
        # Coverage = 30/50 * 100 = 60%
        assert metrics['coverage'] == 60.0

    def test_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=['Status', 'Count'])
        metrics = calculate_overall_metrics(empty_df)
        assert metrics['total'] == 0
        assert metrics['coverage'] == 0


class TestTestimMetrics:
    """Tests for calculate_testim_metrics function"""

    def test_testim_totals(self, sample_summary_df):
        metrics = calculate_testim_metrics(sample_summary_df)
        assert metrics['total_testim'] == 20  # Only Testim Desktop in sample

    def test_device_breakdown(self, sample_summary_df):
        metrics = calculate_testim_metrics(sample_summary_df)
        assert metrics['desktop'] == 20
        assert metrics['mobile'] == 0
        assert metrics['both'] == 0

    def test_testim_coverage(self, sample_summary_df):
        metrics = calculate_testim_metrics(sample_summary_df)
        # Total Testim = 20, To Be + Not = 20, Total = 40
        # Coverage = 20/40 * 100 = 50%
        assert metrics['testim_coverage'] == 50.0


class TestDeviceMetrics:
    """Tests for calculate_device_metrics function"""

    def test_device_metrics_calculation(self, sample_summary_df):
        metrics = calculate_device_metrics(sample_summary_df)

        assert 'Desktop' in metrics
        assert 'Mobile' in metrics
        assert 'Both' in metrics

    def test_desktop_metrics(self, sample_summary_df):
        metrics = calculate_device_metrics(sample_summary_df)
        desktop = metrics['Desktop']

        # Desktop has: Automated Java (10), Testim Desktop (20), N/A (8) = 38 total, 30 automated
        assert desktop['total'] == 38
        assert desktop['automated'] == 30
        assert desktop['coverage'] == pytest.approx(78.95, rel=0.01)

    def test_mobile_metrics(self, sample_summary_df):
        metrics = calculate_device_metrics(sample_summary_df)
        mobile = metrics['Mobile']

        # Mobile has: To Be Automated (15) = 15 total, 0 automated
        assert mobile['total'] == 15
        assert mobile['automated'] == 0
        assert mobile['coverage'] == 0.0


class TestEpicFiltering:
    """Tests for filter_epic_by_search function"""

    def test_filter_epics(self):
        pivot = pd.DataFrame(
            {'Automated': [10, 20, 30]},
            index=['Epic One', 'Epic Two', 'Story Three']
        )

        filtered = filter_epic_by_search(pivot, 'Epic')
        assert len(filtered) == 2
        assert 'Epic One' in filtered.index
        assert 'Epic Two' in filtered.index

    def test_case_insensitive_search(self):
        pivot = pd.DataFrame(
            {'Automated': [10, 20]},
            index=['EPIC ONE', 'epic two']
        )

        filtered = filter_epic_by_search(pivot, 'epic')
        assert len(filtered) == 2

    def test_empty_search(self):
        pivot = pd.DataFrame(
            {'Automated': [10, 20]},
            index=['Epic One', 'Epic Two']
        )

        filtered = filter_epic_by_search(pivot, '')
        assert len(filtered) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
