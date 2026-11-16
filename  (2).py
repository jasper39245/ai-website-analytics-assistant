"""Part 1: plain Python that reads the CSV and calculates the numbers.
The AI never does the maths. Code does, so the numbers are always correct."""
import csv
import io
from collections import defaultdict


def parse_csv(text: str) -> list[dict]:
    """Turn CSV text into a list of dictionaries, one per row."""
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        rows.append({
            "date": row["date"],
            "page": row["page"],
            "visits": int(row["visits"]),
            "bounce_rate": float(row["bounce_rate"]),
            "avg_time_sec": float(row["avg_time_sec"]),
        })
    if not rows:
        raise ValueError("CSV has no rows")
    return rows


def compute_stats(rows: list[dict]) -> dict:
    """Group rows by page and calculate totals, averages and growth."""
    pages = defaultdict(list)
    for r in rows:
        pages[r["page"]].append(r)

    per_page = []
    for page, items in pages.items():
        items.sort(key=lambda r: r["date"])
        half = len(items) // 2 or 1
        first = sum(i["visits"] for i in items[:half])
        second = sum(i["visits"] for i in items[half:])
        growth = ((second - first) / first * 100) if first else 0.0
        per_page.append({
            "page": page,
            "total_visits": sum(i["visits"] for i in items),
            "avg_bounce_rate": round(sum(i["bounce_rate"] for i in items) / len(items), 1),
            "avg_time_sec": round(sum(i["avg_time_sec"] for i in items) / len(items), 1),
            "growth_pct": round(growth, 1),
        })

    per_page.sort(key=lambda p: p["total_visits"], reverse=True)
    return {
        "total_visits": sum(p["total_visits"] for p in per_page),
        "top_page": per_page[0]["page"],
        "highest_bounce_page": max(per_page, key=lambda p: p["avg_bounce_rate"])["page"],
        "fastest_growing_page": max(per_page, key=lambda p: p["growth_pct"])["page"],
        "pages": per_page,
    }
