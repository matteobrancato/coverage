"""
Unit tests for transformer module
"""
import pytest
import pandas as pd
import numpy as np
from src.transformer import (
    map_country_id,
    map_priority,
    map_device_status,
    map_automation_status_java,
    map_automation_status_testim,
    determine_final_status,
    find_field
)


class TestCountryMapping:
    """Tests for map_country_id function"""

    def test_marionnaud_country_mapping(self):
        assert map_country_id('3', 'Marionnaud') == 'MRN'
        assert map_country_id('9', 'Marionnaud') == 'MFR'
        assert map_country_id('10', 'Marionnaud') == 'MCH'

    def test_drogas_country_mapping(self):
        assert map_country_id('5', 'Drogas') == 'LT'
        assert map_country_id('6', 'Drogas') == 'LV'
        assert map_country_id('7', 'Drogas') == 'RU'

    def test_unknown_country_id(self):
        assert map_country_id('999', 'Marionnaud') == 'ID_999'
        assert map_country_id('abc', 'Drogas') == 'ID_abc'

    def test_empty_country_list(self):
        assert map_country_id([], 'Marionnaud') == 'Unknown'

    def test_country_list(self):
        result = map_country_id(['3', '9'], 'Marionnaud')
        assert 'MRN' in result
        assert 'MFR' in result

    def test_nan_country(self):
        assert map_country_id(np.nan, 'Marionnaud') == 'Unknown'


class TestPriorityMapping:
    """Tests for map_priority function"""

    def test_priority_id_mapping(self):
        assert map_priority(3) == 'High'
        assert map_priority(4) == 'Highest'
        assert map_priority(5) == 'Medium'

    def test_priority_float_conversion(self):
        assert map_priority(3.0) == 'High'
        assert map_priority(4.0) == 'Highest'

    def test_priority_string_matching(self):
        assert map_priority('highest') == 'Highest'
        assert map_priority('high') == 'High'
        assert map_priority('medium') == 'Medium'

    def test_unknown_priority(self):
        assert map_priority(99) == 'Unknown'
        assert map_priority('low') == 'Unknown'

    def test_nan_priority(self):
        assert map_priority(np.nan) == 'Unknown'


class TestDeviceMapping:
    """Tests for map_device_status function"""

    def test_device_id_mapping(self):
        assert map_device_status(1) == 'Desktop'
        assert map_device_status(2) == 'Mobile'
        assert map_device_status(3) == 'Both'

    def test_device_float_conversion(self):
        assert map_device_status(1.0) == 'Desktop'
        assert map_device_status(2.0) == 'Mobile'

    def test_unknown_device(self):
        assert map_device_status(99) == 'Both'

    def test_nan_device(self):
        assert map_device_status(np.nan) == 'Both'


class TestAutomationStatusJava:
    """Tests for map_automation_status_java function"""

    def test_java_status_mapping(self):
        assert map_automation_status_java(1) == 'Not Automated'
        assert map_automation_status_java(2) == 'To Be Automated'
        assert map_automation_status_java(3) == 'Automated'
        assert map_automation_status_java(4) == 'N/A'

    def test_java_status_float(self):
        assert map_automation_status_java(3.0) == 'Automated'

    def test_java_status_unknown(self):
        assert map_automation_status_java(99) is None

    def test_java_status_nan(self):
        assert map_automation_status_java(np.nan) is None


class TestAutomationStatusTestim:
    """Tests for map_automation_status_testim function"""

    def test_testim_status_mapping(self):
        assert map_automation_status_testim(1) == 'Not Automated'
        assert map_automation_status_testim(2) == 'To Be Automated'
        assert map_automation_status_testim(3) == 'Automated'
        assert map_automation_status_testim(4) == 'N/A'

    def test_testim_status_float(self):
        assert map_automation_status_testim(3.0) == 'Automated'

    def test_testim_status_unknown(self):
        assert map_automation_status_testim(99) is None

    def test_testim_status_nan(self):
        assert map_automation_status_testim(np.nan) is None


class TestDetermineFinalStatus:
    """Tests for determine_final_status function"""

    def test_both_testim_automated(self):
        row = pd.Series({
            'Java_Status': 'Automated',
            'Testim_Desktop_Status': 'Automated',
            'Testim_Mobile_Status': 'Automated'
        })
        assert determine_final_status(row) == 'Automated - Testim Both'

    def test_testim_desktop_only(self):
        row = pd.Series({
            'Java_Status': 'Not Automated',
            'Testim_Desktop_Status': 'Automated',
            'Testim_Mobile_Status': 'Not Automated'
        })
        assert determine_final_status(row) == 'Automated - Testim Desktop'

    def test_testim_mobile_only(self):
        row = pd.Series({
            'Java_Status': 'Not Automated',
            'Testim_Desktop_Status': 'Not Automated',
            'Testim_Mobile_Status': 'Automated'
        })
        assert determine_final_status(row) == 'Automated - Testim Mobile'

    def test_java_only(self):
        row = pd.Series({
            'Java_Status': 'Automated',
            'Testim_Desktop_Status': 'Not Automated',
            'Testim_Mobile_Status': 'Not Automated'
        })
        assert determine_final_status(row) == 'Automated - Java'

    def test_na_status(self):
        row = pd.Series({
            'Java_Status': 'N/A',
            'Testim_Desktop_Status': 'Not Automated',
            'Testim_Mobile_Status': 'Not Automated'
        })
        assert determine_final_status(row) == 'N/A'

    def test_to_be_automated(self):
        row = pd.Series({
            'Java_Status': 'To Be Automated',
            'Testim_Desktop_Status': 'Not Automated',
            'Testim_Mobile_Status': 'Not Automated'
        })
        assert determine_final_status(row) == 'To Be Automated'

    def test_not_automated(self):
        row = pd.Series({
            'Java_Status': 'Not Automated',
            'Testim_Desktop_Status': 'Not Automated',
            'Testim_Mobile_Status': 'Not Automated'
        })
        assert determine_final_status(row) == 'Not Automated'


class TestFindField:
    """Tests for find_field function"""

    def test_find_java_field(self):
        df = pd.DataFrame(columns=['custom_automation_status', 'other_field'])
        assert find_field(df, 'java') == 'custom_automation_status'

    def test_find_alternate_field(self):
        df = pd.DataFrame(columns=['automation_status', 'other_field'])
        assert find_field(df, 'java') == 'automation_status'

    def test_field_not_found(self):
        df = pd.DataFrame(columns=['other_field', 'another_field'])
        assert find_field(df, 'java') is None

    def test_find_epic_field(self):
        df = pd.DataFrame(columns=['custom_epic_reference', 'other_field'])
        assert find_field(df, 'epic') == 'custom_epic_reference'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
