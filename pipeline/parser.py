# pipeline/parser.py

from decimal import Decimal


def extract_city(address_components: list) -> str:
    for component in address_components:
        if "locality" in component.get("types", []):
            return component.get("long_name", "")
    return ""


def extract_country(address_components: list) -> str:
    for component in address_components:
        if "country" in component.get("types", []):
            return component.get("long_name", "")
    return ""


def to_decimal(value) -> Decimal | None:
    """Safely convert float/int to Decimal for DynamoDB compatibility."""
    if value is None:
        return None
    return Decimal(str(value))  # str() avoids float precision issues


def parse_place(raw_result: dict, details: dict, industry: str, location: str) -> dict:
    address_components = details.get("address_components", [])

    lead = {
        "place_id":        raw_result.get("place_id", ""),
        "business_name":   details.get("name") or raw_result.get("name", ""),
        "industry":        industry,
        "address":         details.get("formatted_address") or raw_result.get("formatted_address", ""),
        "city":            extract_city(address_components),
        "country":         extract_country(address_components),
        "phone":           details.get("formatted_phone_number", ""),
        "website":         details.get("website", ""),
        "google_rating":   to_decimal(details.get("rating") or raw_result.get("rating")),
        "total_reviews":   to_decimal(details.get("user_ratings_total") or raw_result.get("user_ratings_total")),
        "search_query":    f"{industry} in {location}",
        "search_location": location,
        "status":          "new",
    }

    # DynamoDB does not accept empty strings — remove any None or empty values
    return {k: v for k, v in lead.items() if v is not None and v != ""}