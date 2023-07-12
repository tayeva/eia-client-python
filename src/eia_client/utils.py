"""
EIA client utilities (common helper functions) module.
"""

def list_if_str(obj) -> list:
    """Helper function for converting a string object to a list."""
    return [obj] if isinstance(obj, str) else obj


def list_if_none(obj) -> list:
    """Helper function for converting a None object to an empty list."""
    return [] if obj is None else obj
