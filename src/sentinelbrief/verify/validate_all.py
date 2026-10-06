import json
import os
import sys
from pathlib import Path

from sentinelbrief.models import Instrument, Obligation
from sentinelbrief.verify.citation_validator import SourceTextStore
from sentinelbrief.verify.obligation_validator import validate_obligation
from sentinelbrief.verify.raw_provenance import verify_raw_dir
from sentinelbrief.verify.schema_validator import validate_all


def main() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    instruments_dir = os.path.join(base_dir, "data", "instruments")
    obligations_dir = os.path.join(base_dir, "data", "obligations")
    entities_dir = os.path.join(base_dir, "data", "entities")
    raw_dir = os.path.join(base_dir, "data", "raw")
    migrations_dir = os.path.join(base_dir, "data", "migrations")

    print("Running raw-source provenance checks...")
    prov_errors, prov_warnings = verify_raw_dir(raw_dir)
    for warning in prov_warnings:
        print(f"Warning: {warning}")
    if prov_errors:
        for error in prov_errors:
            print(f"Error: {error}")
        sys.exit(1)
    print("Raw-source provenance passed.")

    print("Running schema validation...")
    invalid_inst = validate_all(instruments_dir, "instrument.schema.json")
    invalid_obl = validate_all(obligations_dir, "obligation.schema.json")
    invalid_ent = (
        validate_all(entities_dir, "entity_class.schema.json")
        if os.path.exists(entities_dir)
        else []
    )
    invalid_migrations = []
    migration_file = os.path.join(
        migrations_dir, "rbi.nbfc-it-framework.2017__rbi.nbfc-cyber.2026.json"
    )
    if os.path.exists(migration_file):
        from sentinelbrief.verify.schema_validator import load_schema, validate_data_file

        try:
            validate_data_file(migration_file, load_schema("migration.schema.json"))
        except Exception as exc:
            print(f"Schema validation failed for {migration_file}: {exc}")
            invalid_migrations.append(migration_file)

    if invalid_inst or invalid_obl or invalid_ent or invalid_migrations:
        print(
            f"Schema validation failed: {len(invalid_inst)} instruments, {len(invalid_obl)} obligations, {len(invalid_ent)} entities, {len(invalid_migrations)} migrations"
        )
        sys.exit(1)

    print("Schema validation passed.")

    print("Running obligation and citation validation...")
    source_store = SourceTextStore(raw_dir)

    instruments: dict[str, Instrument] = {}
    if os.path.exists(instruments_dir):
        for p in Path(instruments_dir).glob("**/*.json"):
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        inst = Instrument(**item)
                        instruments[inst.id] = inst
                else:
                    inst = Instrument(**data)
                    instruments[inst.id] = inst

    total = 0
    valid_count = 0
    invalid_count = 0
    warning_count = 0

    if os.path.exists(obligations_dir):
        for p in Path(obligations_dir).glob("**/*.json"):
            with open(p, encoding="utf-8") as f:
                data = json.load(f)

            items = data if isinstance(data, list) else [data]
            for item in items:
                obl = Obligation(**item)
                total += 1
                inst_obj = instruments.get(obl.instrument_id)
                if inst_obj is None:
                    print(
                        f"Error: Instrument {obl.instrument_id} not found for obligation {obl.id}"
                    )
                    invalid_count += 1
                    continue

                source_text = source_store.get_text(obl.instrument_id)
                if not source_text:
                    print(f"Error: Source text not found for instrument {obl.instrument_id}")
                    invalid_count += 1
                    continue

                result = validate_obligation(obl, inst_obj, source_text)
                if result.valid:
                    valid_count += 1
                    if result.warnings:
                        warning_count += len(result.warnings)
                else:
                    invalid_count += 1
                    print(f"Validation failed for obligation {obl.id}: {result.errors}")

    print("\nValidation Summary:")
    print(f"Total Obligations: {total}")
    print(f"Valid: {valid_count}")
    print(f"Invalid: {invalid_count}")
    print(f"Warnings: {warning_count}")

    if invalid_count > 0:
        sys.exit(1)

    print("\nAll obligations and citations passed validation successfully!")


if __name__ == "__main__":
    main()
