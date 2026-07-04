"""
Approach 3: Newline-delimited JSON (JSONL) — read line by line, no streaming
library needed. BigQuery accepts JSONL natively, so this is usually the
simplest and fastest path.

Best for: JSONL source files.
Watch out for: a single malformed line silently failing the whole load
                if you don't handle it.
"""

import json

DRY_RUN = True
DEAD_LETTER_LOG = "dead_letters.log"


def parse_jsonl(path):
    good_rows = []
    bad_lines = []

    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                good_rows.append(record)
            except json.JSONDecodeError as e:
                bad_lines.append((line_num, line, str(e)))

    return good_rows, bad_lines


def write_dead_letters(bad_lines):
    if not bad_lines:
        return
    with open(DEAD_LETTER_LOG, "w") as f:
        for line_num, line, error in bad_lines:
            f.write(f"Line {line_num}: {error}\n  Raw: {line}\n")
    print(f"Logged {len(bad_lines)} bad line(s) to {DEAD_LETTER_LOG}")


def load_to_bigquery(rows, table_id="project.dataset.table"):
    if DRY_RUN:
        print(f"[DRY RUN] Would load {len(rows)} good rows into {table_id}")
        return

    from google.cloud import bigquery

    client = bigquery.Client()
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print("Errors while inserting rows:", errors)
    else:
        print(f"Loaded {len(rows)} rows into {table_id}")


if __name__ == "__main__":
    good_rows, bad_lines = parse_jsonl("records.jsonl")
    write_dead_letters(bad_lines)
    load_to_bigquery(good_rows)
    print(f"Parsed {len(good_rows)} good rows, skipped {len(bad_lines)} bad line(s).")
