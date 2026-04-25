import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
DATABASE_PATH = os.getenv("DATABASE_PATH", "db/leads.db")

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACES_DETAILS_URL     = "https://maps.googleapis.com/maps/api/place/details/json"

# Fields to request from Places Details API
# Only request what you need — each field group has a cost tier
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