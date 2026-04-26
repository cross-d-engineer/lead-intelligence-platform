from pipeline.parser import extract_city, extract_country, parse_place, to_decimal
from decimal import Decimal


MOCK_ADDRESS_COMPONENTS = [
    {"types": ["locality"], "long_name": "Port of Spain"},
    {"types": ["country"], "long_name": "Trinidad and Tobago"}
]


def test_extract_city():
    assert extract_city(MOCK_ADDRESS_COMPONENTS) == "Port of Spain"


def test_extract_country():
    assert extract_country(MOCK_ADDRESS_COMPONENTS) == "Trinidad and Tobago"


def test_extract_city_missing():
    assert extract_city([]) == ""


def test_to_decimal_float():
    assert to_decimal(4.5) == Decimal("4.5")


def test_to_decimal_none():
    assert to_decimal(None) is None


def test_parse_place_returns_expected_keys():
    raw    = {"place_id": "abc123", "name": "Test Biz", "formatted_address": "123 Main St"}
    details = {
        "name": "Test Biz",
        "formatted_address": "123 Main St",
        "address_components": MOCK_ADDRESS_COMPONENTS,
        "rating": 4.5,
        "user_ratings_total": 100
    }
    lead = parse_place(raw, details, "plumbing", "Port of Spain")
    assert lead["place_id"] == "abc123"
    assert lead["business_name"] == "Test Biz"
    assert lead["city"] == "Port of Spain"
    assert lead["google_rating"] == Decimal("4.5")