# Video Script: "3 Ways to Parse JSON Before Loading into BigQuery"

**Format:** Screen recording + voiceover
**Length:** ~3–4 minutes
**Style:** Terminal/code editor walkthrough, casual explainer tone

---

## SCENE 1 — Hook (0:00–0:15)
**Visual:** Face cam or title card: "3 ways to parse JSON before loading into BigQuery"

**Voiceover:**
"If you're loading JSON into BigQuery, the way you parse it depends entirely on file size and structure — not habit. Here are three approaches I used this month, what broke, and how I fixed it."

---

## SCENE 2 — Approach 1: Small Files (0:15–1:00)
**Visual:** Code editor open on `approach1_small_file.py`. Cursor highlights `json.load()`.

**Voiceover:**
"First — small files, a few hundred MB or less. Just load the whole thing into memory with `json.load()`, transform it, and push it to BigQuery in one batch."

**On-screen text overlay:** `✅ Simple  ⚠️ Memory scales with file size`

**Voiceover (cont.):**
"The catch — memory usage scales linearly with file size. Fine until it isn't. I set a hard file-size threshold so anything bigger auto-routes to streaming instead."

**Visual:** Run the script live, show terminal output loading into a mock BQ table.

---

## SCENE 3 — Approach 2: Large Nested Files (1:00–2:00)
**Visual:** Switch to `approach2_streaming.py`. Highlight `ijson` import and the batching loop.

**Voiceover:**
"Second — large, deeply nested files. Loading the whole thing stopped making sense, so I switched to streaming with `ijson`, processing record by record instead of holding everything in memory."

**On-screen text overlay:** `✅ Handles huge files  ⚠️ Batch size tuning needed`

**Voiceover (cont.):**
"The issue here was batching. Too small, and you make too many API calls to BigQuery. Too large, and you risk timeouts. I landed on batching every 5,000 records."

**Visual:** Show the batch counter incrementing in terminal as the script runs.

---

## SCENE 4 — Approach 3: JSONL (2:00–2:45)
**Visual:** Switch to `approach3_jsonl.py`. Highlight the simple line-by-line loop.

**Voiceover:**
"Third — newline-delimited JSON, or JSONL. This turned out to be the easiest case. Each line is its own valid JSON object, and BigQuery actually accepts JSONL natively — so a lot of this can skip custom parsing entirely."

**On-screen text overlay:** `✅ Simplest & fastest  ⚠️ One bad line can break the load`

**Voiceover (cont.):**
"One gotcha — a single malformed line would silently fail the whole load if I didn't handle it. So I wrapped each line in a try/except and logged bad lines to a dead-letter file instead of failing the batch."

**Visual:** Show a deliberately broken line in the sample file, run the script, show it logged to `dead_letters.log` instead of crashing.

---

## SCENE 5 — Broader Implications (2:45–3:20)
**Visual:** Face cam or slide with 3 bullet points appearing one at a time.

**Voiceover:**
"A few things this taught me, beyond just the code:

Schema drift was the real recurring headache — a new optional field in a nested file can break your BigQuery schema mapping without warning.

Cost matters too. `json.load()` on large files spiked memory costs on compute, while streaming kept memory flat but took longer wall-clock time.

And picking the method after actually inspecting the file — not out of habit — saved real debugging time later."

**On-screen text overlay:** `Speed vs. Memory vs. Fault Tolerance — pick two, plan for the third.`

---

## SCENE 6 — Close (3:20–3:40)
**Visual:** Face cam, title card with GitHub/code link.

**Voiceover:**
"Full code for all three approaches is linked below. Curious how you're handling schema drift on your own JSON-to-BQ loads — drop it in the comments."

**On-screen text overlay:** "Code + sample files linked below 👇"

---

## Shot List Summary
| Scene | Visual | Duration |
|---|---|---|
| 1 | Title card / face cam | 15s |
| 2 | `approach1_small_file.py` demo | 45s |
| 3 | `approach2_streaming.py` demo | 60s |
| 4 | `approach3_jsonl.py` demo | 45s |
| 5 | Bullet point slide | 35s |
| 6 | Close + CTA | 20s |
