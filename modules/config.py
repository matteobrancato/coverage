"""
Configuration module for Business Units and application settings
"""
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class BusinessUnitConfig:
    """Configuration for a single Business Unit"""
    name: str
    project_id: int
    suite_id: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "project_id": self.project_id,
            "suite_id": self.suite_id
        }


# Business Unit Configurations
BU_CONFIG: Dict[str, BusinessUnitConfig] = {
    "Microservices": BusinessUnitConfig(
        name="Microservices",
        project_id=17,
        suite_id=9570
    ),
    "ICI Paris XL": BusinessUnitConfig(
        name="ICI Paris XL",
        project_id=4,
        suite_id=1399
    ),
    "Kruidvat": BusinessUnitConfig(
        name="Kruidvat",
        project_id=11,
        suite_id=115
    ),
    "Trekpleister": BusinessUnitConfig(
        name="Trekpleister",
        project_id=3,
        suite_id=30784
    ),
    "Superdrug": BusinessUnitConfig(
        name="Superdrug",
        project_id=5,
        suite_id=71
    ),
    "Savers": BusinessUnitConfig(
        name="Savers",
        project_id=3,
        suite_id=30784
    ),
    "The Perfume Shop": BusinessUnitConfig(
        name="The Perfume Shop",
        project_id=22,
        suite_id=11833
    ),
    "Marionnaud": BusinessUnitConfig(
        name="Marionnaud",
        project_id=3,
        suite_id=30784
    ),
    "Drogas": BusinessUnitConfig(
        name="Drogas",
        project_id=22,
        suite_id=16093
    )
}


def get_bu_names() -> list[str]:
    """Get list of all business unit names"""
    return list(BU_CONFIG.keys())


def get_bu_config(bu_name: str) -> BusinessUnitConfig:
    """Get configuration for a specific business unit"""
    if bu_name not in BU_CONFIG:
        raise ValueError(f"Unknown business unit: {bu_name}")
    return BU_CONFIG[bu_name]


# Country Mappings
COUNTRY_MAPPINGS: Dict[str, Dict[str, str]] = {
    "Marionnaud": {
        '3': 'MRN',
        '9': 'MFR',
        '10': 'MCH',
        '11': 'MAT',
        '12': 'MRO',
        '13': 'MIT',
        '14': 'MCZ',
        '15': 'MSK',
        '16': 'MHU',
        '22': 'MCH_SPR',
        '23': 'MAT_SPR',
        '24': 'MRO_SPR',
        '25': 'MIT_SPR',
        '26': 'MCZ_SPR',
        '27': 'MSK_SPR',
        '28': 'MHU_SPR'
    },
    "Drogas": {
        '5': 'LT',
        '6': 'LV',
        '7': 'RU'
    }
}


# Priority Mappings
PRIORITY_MAPPINGS: Dict[int, str] = {
    3: 'High',
    4: 'Highest',
    5: 'Medium'
}


# Device Mappings
DEVICE_MAPPINGS: Dict[int, str] = {
    1: "Desktop",
    2: "Mobile",
    3: "Both"
}


# Automation Status Mappings for Java
JAVA_STATUS_MAPPINGS: Dict[int, str] = {
    1: "Not Automated",
    2: "To Be Automated",
    3: "Automated",
    4: "N/A",
    5: "To Be Automated",
    6: "To Be Automated",
    7: "Not Automated",
    8: "Automated",
    9: "Automated",
    10: "To Be Automated"
}


# Automation Status Mappings for Testim
TESTIM_STATUS_MAPPINGS: Dict[int, str] = {
    1: "Not Automated",
    2: "To Be Automated",
    3: "Automated",
    4: "N/A",
    5: "To Be Automated",
    6: "To Be Automated",
    7: "Not Automated",
    8: "Automated",
    9: "Automated"
}


# Field Name Variations
FIELD_VARIATIONS = {
    "java": ['custom_automation_status', 'automation_status'],
    "testim_desktop": [
        'custom_case_automation_status_testim',
        'custom_automation_status_testim_desktop_view',
        'automation_status_testim_desktop'
    ],
    "testim_mobile": [
        'custom_case_automation_status_mobile_view',
        'custom_automation_status_testim_mobile_view',
        'automation_status_testim_mobile'
    ],
    "epic": ['custom_epic_reference', 'custom_epicreference', 'custom_epic', 'refs'],
    "device": ['custom_device', 'device', 'custom_devices'],
    "country": ['multi_countries', 'custom_multi_countries', 'countries'],
    "priority": ['priority_id', 'priority', 'custom_priority']
}
