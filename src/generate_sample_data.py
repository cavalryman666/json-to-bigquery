"""
Generates the sample data files used by the three parsing demos:
  - small_file.json     (Approach 1: whole-file load)
  - large_nested.json   (Approach 2: streaming with ijson)
  - records.jsonl       (Approach 3: newline-delimited JSON, with one bad line)
"""

import json
import random

# ---------- Approach 1: small file ----------
small_data = {
    "export_date": "2026-07-04",
    "records": [
        {"id": i, "sku": f"SKU-{1000+i}", "qty": random.randint(1, 500)}
        for i in range(50)
    ],
}
with open("small_file.json", "w") as f:
    json.dump(small_data, f, indent=2)

# ---------- Approach 2: large nested file ----------
large_nested = {
    "batch_id": "B-2026-07",
    "warehouses": [
        {
            "warehouse_id": f"WH-{w}",
            "items": [
                {
                    "sku": f"SKU-{1000+i}",
                    "qty": random.randint(1, 500),
                    "supplier": {
                        "id": f"SUP-{w}-{i}",
                        "lead_time_days": random.randint(1, 30),
                    },
                }
                for i in range(20)
            ],
        }
        for w in range(5)
    ],
}
with open("large_nested.json", "w") as f:
    json.dump(large_nested, f, indent=2)

# ---------- Approach 3: JSONL, with one deliberately broken line ----------
with open("records.jsonl", "w") as f:
    for i in range(20):
        record = {"id": i, "sku": f"SKU-{1000+i}", "qty": random.randint(1, 500)}
        f.write(json.dumps(record) + "\n")
    # Deliberately inject a malformed line to demonstrate dead-letter handling
    f.write('{"id": 999, "sku": "SKU-BROKEN", "qty": }\n')
    for i in range(20, 25):
        record = {"id": i, "sku": f"SKU-{1000+i}", "qty": random.randint(1, 500)}
        f.write(json.dumps(record) + "\n")

print("Sample files created: small_file.json, large_nested.json, records.jsonl")
