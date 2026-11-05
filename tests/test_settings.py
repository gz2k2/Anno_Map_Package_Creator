"""Tests for GUID range validation."""
import pytest
from app.config.config_app import SUPPORTED_GAMES
from app.functions import function_settings
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

def test_save_settings_accepts_empty_guid_ranges(tmp_path, monkeypatch):
    """Allow settings to be saved before optional import GUID ranges are configured."""
    monkeypatch.setattr(function_settings, 'config_path', lambda: tmp_path / 'config.json')
    monkeypatch.setattr(function_settings, 'database_path', lambda game: tmp_path / f'{game}.json')
    settings = {
        'selected_game': SUPPORTED_GAMES[0],
        'games': {
            game: {
                'guid_start': '',
                'guid_end': '',
                'custom_regions': [],
                'default_export_path': '',
            }
            for game in SUPPORTED_GAMES
        },
    }

    function_settings.save_settings(settings)

    assert (tmp_path / 'config.json').is_file()
    assert all((tmp_path / f'{game}.json').is_file() for game in SUPPORTED_GAMES)

def test_save_settings_rejects_partial_guid_range(tmp_path, monkeypatch):
    """Reject partially configured GUID ranges before writing settings files."""
    monkeypatch.setattr(function_settings, 'config_path', lambda: tmp_path / 'config.json')
    monkeypatch.setattr(function_settings, 'database_path', lambda game: tmp_path / f'{game}.json')
    settings = {
        'selected_game': SUPPORTED_GAMES[0],
        'games': {
            game: {
                'guid_start': '100' if game == SUPPORTED_GAMES[0] else '',
                'guid_end': '',
                'custom_regions': [],
                'default_export_path': '',
            }
            for game in SUPPORTED_GAMES
        },
    }

    with pytest.raises(ValueError):
        function_settings.save_settings(settings)

    assert not list(tmp_path.iterdir())
