import requests
import time
from config.settings import (
    GOOGLE_PLACES_API_KEY,
    PLACES_TEXT_SEARCH_URL,
    PLACES_DETAILS_URL,
    DETAIL_FIELDS
)


def search_businesses(industry: str, location: str) -> list[dict]:
    query = f"{industry} in {location}"
    params = {
        "query": query,
        "key": GOOGLE_PLACES_API_KEY,
    }

    all_results = []

    while True:
        response = requests.get(PLACES_TEXT_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

        status = data.get("status")
        #print(f"[debug] Status: {status}")

        if status not in ("OK", "ZERO_RESULTS"):
            raise RuntimeError(f"Places API error: {status} — {data.get('error_message', '')}")

        results = data.get("results", [])
        all_results.extend(results)

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

        # Retry loop — token can take up to 3s to activate on Google's side
        paginated_params = {
            "pagetoken": next_page_token,
            "key": GOOGLE_PLACES_API_KEY
        }

        for attempt in range(5):
            time.sleep(3)
            retry_response = requests.get(PLACES_TEXT_SEARCH_URL, params=paginated_params)
            retry_data = retry_response.json()
            retry_status = retry_data.get("status")
            #print(f"[debug] Pagination attempt {attempt + 1}: {retry_status}")

            if retry_status == "OK":
                data = retry_data
                params = paginated_params
                break
            elif retry_status == "INVALID_REQUEST":
                continue  # Token not ready yet, wait and retry
            else:
                raise RuntimeError(f"Pagination error: {retry_status}")
        else:
            # Exhausted retries — skip remaining pages, keep what we have
            print("[collector] Warning: Could not load next page, keeping current results.")
            break

        results = data.get("results", [])
        all_results.extend(results)

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

    print(f"[collector] Found {len(all_results)} results for '{query}'")
    return all_results


def get_place_details(place_id: str) -> dict:
    """
    Fetch enriched details for a single place.
    """
    params = {
        "place_id": place_id,
        "fields": ",".join(DETAIL_FIELDS),
        "key": GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(PLACES_DETAILS_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK":
        print(f"[collector] Warning: Could not fetch details for {place_id}")
        return {}

    return data.get("result", {})