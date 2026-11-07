
import json
from pathlib import Path
from collections import Counter

from app.config import DATA_DIR
from app.knowledge import load_records, record_to_result

LANGUAGES = ["en", "hi", "bn"]

print("=" * 55)
print("       BHARAT AI KNOWLEDGE BASE - DATABASE TEST")
print("=" * 55)

errors = []
warnings = []

# 1. Load records
try:
    records = load_records()
    print(f"\n[PASS] Records loaded: {len(records)}")
except Exception as error:
    print(f"\n[FAIL] Could not load records: {error}")
    raise SystemExit(1)

# 2. Check duplicate IDs
ids = [record.get("id") for record in records]
duplicates = [
    record_id
    for record_id, count in Counter(ids).items()
    if count > 1
]

if not duplicates and None not in ids:
    print("[PASS] Record IDs are unique")
else:
    errors.append(f"Duplicate or missing IDs: {duplicates}")
    print("[FAIL] Duplicate or missing record IDs")

# 3. Check required fields
required_fields = [
    "id",
    "category",
    "type",
    "names",
    "content",
    "tags",
    "facts",
    "sources",
    "status"
]

for record in records:
    for field in required_fields:
        if field not in record:
            errors.append(
                f"{record.get('id', 'UNKNOWN')}: missing {field}"
            )

if not any("missing" in error for error in errors):
    print("[PASS] Required fields exist")

# 4. Check multilingual fields
translation_errors = []

for record in records:
    record_id = record.get("id", "UNKNOWN")

    for field in ["names", "content", "tags"]:
        value = record.get(field)

        if not isinstance(value, dict):
            translation_errors.append(
                f"{record_id}: {field} must be a language object"
            )
            continue

        for lang in LANGUAGES:
            if not value.get(lang):
                translation_errors.append(
                    f"{record_id}: missing {lang} in {field}"
                )

if translation_errors:
    errors.extend(translation_errors)
    print(
        f"[FAIL] Translation problems: "
        f"{len(translation_errors)}"
    )
else:
    print("[PASS] English, Hindi and Bengali fields exist")

# 5. Check sources
source_errors = []

for record in records:
    record_id = record.get("id", "UNKNOWN")
    sources = record.get("sources")

    if not isinstance(sources, list) or not sources:
        source_errors.append(
            f"{record_id}: missing source list"
        )
        continue

    for source in sources:
        if not isinstance(source, dict):
            source_errors.append(
                f"{record_id}: source must be an object"
            )
        elif not source.get("url"):
            source_errors.append(
                f"{record_id}: source URL missing"
            )

if source_errors:
    warnings.extend(source_errors)
    print(f"[WARNING] Source problems: {len(source_errors)}")
else:
    print("[PASS] Source objects and URLs exist")

# 6. Check JSON files individually
json_errors = []

for path in DATA_DIR.glob("*.json"):
    try:
        with path.open("r", encoding="utf-8") as file:
            json.load(file)
    except Exception as error:
        json_errors.append(f"{path.name}: {error}")

if json_errors:
    errors.extend(json_errors)
    print(f"[FAIL] Invalid JSON files: {len(json_errors)}")
else:
    print("[PASS] All JSON files are valid")

# 7. Check localized API conversion
localization_errors = []

for record in records:
    for lang in LANGUAGES:
        try:
            result = record_to_result(record, lang)

            if not result.get("name"):
                localization_errors.append(
                    f"{record.get('id')}: empty name in {lang}"
                )

            if not result.get("answer"):
                localization_errors.append(
                    f"{record.get('id')}: empty answer in {lang}"
                )

        except Exception as error:
            localization_errors.append(
                f"{record.get('id')}: {lang}: {error}"
            )

if localization_errors:
    errors.extend(localization_errors)
    print(
        f"[FAIL] Localization problems: "
        f"{len(localization_errors)}"
    )
else:
    print("[PASS] Record localization works")

# 8. Final report
print("\n" + "=" * 55)
print("                    TEST SUMMARY")
print("=" * 55)

print("Total records:", len(records))
print("Unique IDs:", len(set(ids)))
print("Duplicate IDs:", len(duplicates))
print("Errors:", len(errors))
print("Warnings:", len(warnings))

if errors:
    print("\nERROR DETAILS:")
    for error in errors:
        print("-", error)

if warnings:
    print("\nWARNINGS:")
    for warning in warnings:
        print("-", warning)

print("\n" + "=" * 55)

if errors:
    print("RESULT: FAILED")
else:
    print("RESULT: PASSED")

print("=" * 55)
