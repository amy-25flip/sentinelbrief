import json
import os
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

SCHEMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "schema"))


def build_schema_registry() -> Registry:
    """Builds a referencing.Registry containing all schemas in SCHEMA_DIR."""
    schema_path = Path(SCHEMA_DIR)
    registry = Registry()
    if schema_path.exists():
        for p in schema_path.glob("*.schema.json"):
            try:
                schema_json = json.loads(p.read_text(encoding="utf-8"))
                resource = Resource.from_contents(schema_json)
                registry = registry.with_resource(p.name, resource)
                if "$id" in schema_json:
                    registry = registry.with_resource(schema_json["$id"], resource)
            except Exception:
                continue
    return registry


def load_schema(schema_name: str) -> dict[str, Any]:
    path = os.path.join(SCHEMA_DIR, schema_name)
    with open(path, encoding="utf-8") as f:
        res: dict[str, Any] = json.load(f)
        return res


def validate_data_file(
    file_path: str, schema: dict[str, Any], registry: Registry | None = None
) -> None:
    if registry is None:
        registry = build_schema_registry()

    validator = Draft202012Validator(schema, registry=registry)

    with open(file_path, encoding="utf-8") as f:
        if file_path.endswith(".yaml") or file_path.endswith(".yml"):
            data = yaml.safe_load(f)
        else:
            data = json.load(f)

    if schema.get("type") == "object" and isinstance(data, list):
        for i, item in enumerate(data):
            try:
                validator.validate(item)
            except ValidationError as e:
                raise ValidationError(
                    f"Item {i} in {file_path} failed validation: {e.message}"
                ) from e
    else:
        validator.validate(data)


def validate_all(data_dir: str, schema_name: str) -> list[str]:
    """Validates all JSON/YAML files in data_dir against the given schema. Returns list of invalid paths."""
    schema = load_schema(schema_name)
    registry = build_schema_registry()
    invalid_files: list[str] = []

    path = Path(data_dir)
    if not path.exists():
        return invalid_files

    for file_path in path.glob("**/*"):
        if (
            file_path.is_file()
            and file_path.suffix in (".json", ".yaml", ".yml")
            and not file_path.name.endswith(".gitkeep")
        ):
            try:
                validate_data_file(str(file_path), schema, registry=registry)
            except Exception as e:
                print(f"Schema validation failed for {file_path}: {e}")
                invalid_files.append(str(file_path))

    return invalid_files
