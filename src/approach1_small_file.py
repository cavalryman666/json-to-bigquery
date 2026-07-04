"""
Approach 1: Small files — load the whole file into memory with json.load(),
transform, then load to BigQuery in a single batch.

Best for: files under a few hundred MB.
Watch out for: memory usage scales linearly with file size.
"""

import json

# Set this to False and configure BQ credentials to actually write to BigQuery.
DRY_RUN = True

FILE_SIZE_THRESHOLD_MB = 200  # auto-route larger files to streaming (Approach 2)


def load_small_file(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data["records"]


def load_to_bigquery(rows, table_id="project.dataset.table"):
    if DRY_RUN:
        print(f"[DRY RUN] Would load {len(rows)} rows into {table_id}")
        print("Sample row:", rows[0] if rows else None)
        return

    from google.cloud import bigquery

    client = bigquery.Client()
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print("Errors while inserting rows:", errors)
    else:
        print(f"Loaded {len(rows)} rows into {table_id}")


if __name__ == "__main__":
    import os

    path = "small_file.json"
    size_mb = os.path.getsize(path) / (1024 * 1024)

    if size_mb > FILE_SIZE_THRESHOLD_MB:
        print(f"File is {size_mb:.1f} MB — too large for this approach. "
              f"Use approach2_streaming.py instead.")
    else:
        rows = load_small_file(path)
        load_to_bigquery(rows)
