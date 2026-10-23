
import pytest

from extract import parse_response


SAMPLE_ITEMS = [
    {
        "item_name": "Bottled Water",
        "quantity": 3,
        "unit": "case",
        "unit_price": 12.50
    },
    {
        "item_name": "Napkins",
        "quantity": 2,
        "unit": "box",
        "unit_price": 8.00
    }
]


def test_clean_json():
    """A valid JSON array should parse successfully."""
    response = """
    [
        {
            "item_name": "Bottled Water",
            "quantity": 3,
            "unit": "case",
            "unit_price": 12.50
        },
        {
            "item_name": "Napkins",
            "quantity": 2,
            "unit": "box",
            "unit_price": 8.00
        }
    ]
    """

    items, error = parse_response(response)

    assert error is None
    assert items == SAMPLE_ITEMS


def test_json_inside_code_fence():
    """Markdown code fences should not break parsing."""
    response = """
    ```json
    [
        {
            "item_name": "Bottled Water",
            "quantity": 3,
            "unit": "case",
            "unit_price": 12.50
        }
    ]
    ```
    """

    items, error = parse_response(response)

    assert error is None
    assert len(items) == 1
    assert items[0]["item_name"] == "Bottled Water"


def test_json_after_friendly_sentence():
    """An introductory sentence should not break parsing."""
    response = """
    Here are the invoice items I found:

    [
        {
            "item_name": "Napkins",
            "quantity": 2,
            "unit": "box",
            "unit_price": 8.00
        }
    ]
    """

    items, error = parse_response(response)

    assert error is None
    assert len(items) == 1
    assert items[0]["item_name"] == "Napkins"


def test_response_without_json():
    """A response without JSON must fail gracefully."""
    response = "Sorry, I could not extract any invoice items."

    items, error = parse_response(response)

    assert items == []
    assert error is not None


def test_truncated_json():
    """Incomplete JSON must fail without raising an exception."""
    response = """
    [
        {
            "item_name": "Bottled Water",
            "quantity": 3,
            "unit": "case",
            "unit_price":
    """

    items, error = parse_response(response)

    assert items == []
    assert error is not None


def test_invalid_unit():
    """A valid JSON structure with an invalid unit must be rejected."""
    response = """
    [
        {
            "item_name": "Bottled Water",
            "quantity": 3,
            "unit": "pallet",
            "unit_price": 12.50
        }
    ]
    """

    items, error = parse_response(response)

    assert items == []
    assert "invalid unit" in error.lower()


def test_missing_required_field():
    """An object missing a required field must be rejected."""
    response = """
    [
        {
            "item_name": "Napkins",
            "quantity": 2,
            "unit": "box"
        }
    ]
    """

    items, error = parse_response(response)

    assert items == []
    assert "incorrect fields" in error.lower()

