
import json
from pathlib import Path

from fetch_data import format_data


SAMPLE_FILE = Path(__file__).with_name("sample_response.json")


def load_sample():
    """Load saved sample data without making an API request."""
    with SAMPLE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_format_data_displays_city_information():
    """Verify that the formatter displays expected information."""
    city = load_sample()

    output = format_data(city)

    assert "CITY INFORMATION" in output
    assert "Miami" in output
    assert "Florida" in output
    assert "United States" in output
    assert "487,014" in output
    assert "America/New_York" in output


def test_format_data_handles_missing_fields():
    """Verify that missing API fields do not crash the formatter."""
    city = load_sample()

    city.pop("population")
    city.pop("timezone")
    city.pop("admin1")

    output = format_data(city)

    assert "City           : Miami" in output
    assert "State          : Unknown" in output
    assert "Population     : Unknown" in output
    assert "Time Zone      : Unknown" in output
