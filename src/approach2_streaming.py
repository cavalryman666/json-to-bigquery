"""
Approach 2: Large nested files — stream-parse with ijson instead of loading
the whole file into memory, and batch writes to BigQuery.

Best for: large, deeply nested files (GBs).
Watch out for: batch size tuning — too small = too many API calls,
                too large = risk of timeouts.
"""

DRY_RUN = True
BATCH_SIZE = 5000  # tune based on record size


def stream_items(path):
    """
    Streams individual item records out of a deeply nested JSON file
    without loading the whole structure into memory.

    Requires: pip install ijson
    Falls back to a full json.load() if ijson isn't installed, so this
    script still runs for demo purposes — but on real large files, install
    ijson to get the actual memory-saving behavior.
    """
    try:
        import ijson

        with open(path, "rb") as f:
            # Path matches: warehouses -> each warehouse -> items -> each item
            for item in ijson.items(f, "warehouses.item.items.item"):
                yield item
    except ImportError:
        print("[WARNING] ijson not installed — falling back to json.load() "
              "for this demo run. Run: pip install ijson")
        import json

        with open(path, "r") as f:
            data = json.load(f)
        for warehouse in data["warehouses"]:
            for item in warehouse["items"]:
                yield item


def load_to_bigquery_batched(rows, table_id="project.dataset.table"):
    if DRY_RUN:
        print(f"[DRY RUN] Would load batch of {len(rows)} rows into {table_id}")
        return

    from google.cloud import bigquery

    client = bigquery.Client()
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print("Errors while inserting batch:", errors)


if __name__ == "__main__":
    batch = []
    total = 0

    for item in stream_items("large_nested.json"):
        batch.append(item)
        if len(batch) >= BATCH_SIZE:
            load_to_bigquery_batched(batch)
            total += len(batch)
            batch = []

    if batch:  # flush remainder
        load_to_bigquery_batched(batch)
        total += len(batch)

    print(f"Done. Streamed and loaded {total} records total.")
