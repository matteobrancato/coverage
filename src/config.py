"""
Configuration module for Business Units and application settings
"""
from typing import Dict, Any, TypeAlias
from dataclasses import dataclass

# Type Aliases for better readability
CountryMapping: TypeAlias = Dict[str, str]
StatusMapping: TypeAlias = Dict[int, str]
FieldVariations: TypeAlias = Dict[str, list[str]]


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
# Format: "BU Name": (project_id, suite_id)
_BU_DATA: Dict[str, tuple[int, int]] = {
    "Microservices": (17, 9570),
    "ICI Paris XL": (4, 1399),
    "Kruidvat": (11, 115),
    "Trekpleister": (3, 30784),
    "Superdrug": (5, 71),
    "Savers": (3, 30784),
    "The Perfume Shop": (22, 11833),
    "Marionnaud": (3, 30784),
    "Drogas": (22, 16093)
}

# Build BusinessUnitConfig objects from data
BU_CONFIG: Dict[str, BusinessUnitConfig] = {
    name: BusinessUnitConfig(name=name, project_id=pid, suite_id=sid)
    for name, (pid, sid) in _BU_DATA.items()
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
