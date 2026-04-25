import click
from pipeline.collector import search_businesses, get_place_details
from pipeline.parser import parse_place
from pipeline.storage import initialize_db, upsert_lead, get_leads
from config.settings import GOOGLE_PLACES_API_KEY
print(f"[debug] API Key loaded: {GOOGLE_PLACES_API_KEY}")


@click.group()
def cli():
    """Lead Intelligence Platform CLI"""
    pass


@cli.command()
@click.option("--industry", "-i", required=True, help="e.g. 'plumbing', 'dentist', 'restaurant'")
@click.option("--location", "-l", required=True, help="e.g. 'Port of Spain, Trinidad'")
def collect(industry, location):
    """Search and store leads for an industry + location."""
    initialize_db()

    print(f"\n[*] Searching for '{industry}' in '{location}'...\n")
    results = search_businesses(industry, location)

    inserted = 0
    skipped = 0

    for raw in results:
        place_id = raw.get("place_id")
        if not place_id:
            continue

        details = get_place_details(place_id)
        lead = parse_place(raw, details, industry, location)
        outcome = upsert_lead(lead)

        if outcome == "inserted":
            inserted += 1
            print(f"  [+] {lead['business_name']} — {lead['city']}")
        else:
            skipped += 1

    print(f"\n[✓] Done. Inserted: {inserted} | Skipped (duplicates): {skipped}\n")


@cli.command()
@click.option("--industry", "-i", default=None)
@click.option("--city", "-c", default=None)
@click.option("--status", "-s", default=None)
def list_leads(industry, city, status):
    """List stored leads with optional filters."""
    leads = get_leads(industry=industry, city=city, status=status)
    if not leads:
        print("No leads found.")
        return

    for lead in leads:
        print(f"{lead['business_name']} | {lead['industry']} | {lead['city']} | {lead['phone']} | {lead['website']}")

    print(f"\nTotal: {len(leads)} leads")


if __name__ == "__main__":
    cli()