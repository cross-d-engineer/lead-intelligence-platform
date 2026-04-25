import os
import requests
import time

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACES_DETAILS_URL     = "https://maps.googleapis.com/maps/api/place/details/json"

DETAIL_FIELDS = [
    "name",
    "formatted_address",
    "formatted_phone_number",
    "website",
    "rating",
    "user_ratings_total",
    "address_components",
    "place_id",
    "types"
]


def search_businesses(industry: str, location: str) -> list[dict]:
    api_key = os.environ["GOOGLE_PLACES_API_KEY"]
    query   = f"{industry} in {location}"
    params  = {
        "query": query,
        "key":   api_key,
    }

    all_results = []

    while True:
        response = requests.get(PLACES_TEXT_SEARCH_URL, params=params)
        response.raise_for_status()
        data   = response.json()
        status = data.get("status")

        if status not in ("OK", "ZERO_RESULTS"):
            raise RuntimeError(f"Places API error: {status} — {data.get('error_message', '')}")

        all_results.extend(data.get("results", []))

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

        paginated_params = {
            "pagetoken": next_page_token,
            "key":       api_key
        }

        for attempt in range(5):
            time.sleep(3)
            retry_response = requests.get(PLACES_TEXT_SEARCH_URL, params=paginated_params)
            retry_data     = retry_response.json()
            retry_status   = retry_data.get("status")

            if retry_status == "OK":
                data   = retry_data
                params = paginated_params
                break
            elif retry_status == "INVALID_REQUEST":
                continue
            else:
                raise RuntimeError(f"Pagination error: {retry_status}")
        else:
            print("[collector] Warning: Could not load next page, keeping current results.")
            break

        all_results.extend(data.get("results", []))

        if not data.get("next_page_token"):
            break

    print(f"[collector] Found {len(all_results)} results for '{query}'")
    return all_results


def get_place_details(place_id: str) -> dict:
    api_key = os.environ["GOOGLE_PLACES_API_KEY"]
    params  = {
        "place_id": place_id,
        "fields":   ",".join(DETAIL_FIELDS),
        "key":      api_key,
    }
    response = requests.get(PLACES_DETAILS_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK":
        print(f"[collector] Warning: Could not fetch details for {place_id}")
        return {}

    return data.get("result", {})