import os
import json
import boto3
from datetime import datetime
from collector import search_businesses, get_place_details
from parser import parse_place

# AWS clients
dynamodb = boto3.resource("dynamodb")
s3       = boto3.client("s3")
ssm      = boto3.client("ssm")


def get_api_key() -> str:
    """Fetch API key securely from SSM Parameter Store."""
    param_name = os.environ["SSM_PARAM_NAME"]
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def upsert_lead_dynamo(table, lead: dict) -> str:
    """Insert lead into DynamoDB — skips if place_id exists."""
    try:
        table.put_item(
            Item=lead,
            ConditionExpression="attribute_not_exists(place_id)"
        )
        return "inserted"
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return "skipped"


def save_raw_to_s3(bucket: str, results: list, industry: str, location: str):
    """Archive raw API response to S3 for audit trail."""
    key = f"raw/{datetime.utcnow().strftime('%Y/%m/%d')}/{industry}_{location}.json"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(results),
        ContentType="application/json"
    )


def handler(event, context):
    """Lambda entry point."""
    # Inject API key into environment for collector module
    os.environ["GOOGLE_PLACES_API_KEY"] = get_api_key()

    table          = dynamodb.Table(os.environ["DYNAMODB_TABLE"])
    s3_bucket      = os.environ["S3_BUCKET"]
    search_configs = json.loads(os.environ["SEARCH_CONFIGS"])

    total_inserted = 0
    total_skipped  = 0

    for config in search_configs:
        industry = config["industry"]
        location = config["location"]

        print(f"[handler] Searching: {industry} in {location}")
        results = search_businesses(industry, location)

        save_raw_to_s3(s3_bucket, results, industry, location)

        for raw in results:
            place_id = raw.get("place_id")
            if not place_id:
                continue

            details = get_place_details(place_id)
            lead    = parse_place(raw, details, industry, location)
            outcome = upsert_lead_dynamo(table, lead)

            if outcome == "inserted":
                total_inserted += 1
            else:
                total_skipped += 1

    print(f"[handler] Complete — Inserted: {total_inserted} | Skipped: {total_skipped}")
    return {"inserted": total_inserted, "skipped": total_skipped}
