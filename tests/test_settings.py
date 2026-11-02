"""Tests for GUID range validation."""
import pytest
from app.functions.function_settings import validate_guid_range

def test_valid_guid_range():
    """Accept ordered numeric boundaries."""
    assert validate_guid_range("100", "200") == (100, 200)

def test_non_numeric_guid_rejected():
    """Reject non-numeric GUID text."""
    with pytest.raises(ValueError): validate_guid_range("abc", "200")

def test_reversed_guid_range_rejected():
    """Reject a start value greater than the end value."""
    with pytest.raises(ValueError): validate_guid_range("201", "200")
