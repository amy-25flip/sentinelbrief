"""Entity taxonomy management and hierarchy resolution."""

import json
from pathlib import Path

from sentinelbrief.models import EntityClass


class EntityTaxonomy:
    """Loads and resolves the entity hierarchy from versioned data."""

    def __init__(self, entities_dir: Path):
        self.entities_dir = entities_dir
        self.classes: dict[str, EntityClass] = {}
        self._ancestors: dict[str, set[str]] = {}
        self._load()

    def _load(self) -> None:
        if not self.entities_dir.exists():
            raise FileNotFoundError(f"Entities directory does not exist: {self.entities_dir}")

        for path in sorted(self.entities_dir.glob("*.json")):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                items = data if isinstance(data, list) else [data]
                for item in items:
                    ec = EntityClass(**item)
                    if ec.id in self.classes:
                        raise ValueError(f"Duplicate entity class id: {ec.id}")
                    self.classes[ec.id] = ec

        if not self.classes:
            raise ValueError(f"No entity classes found in {self.entities_dir}")

        # Compute transitive closure of ancestors for each entity class
        for eid, ec in self.classes.items():
            ancestors = {eid}
            curr = ec.parent
            visited = {eid}
            while curr is not None:
                if curr not in self.classes:
                    raise ValueError(f"Entity class {eid} references unknown parent: {curr}")
                if curr in visited:
                    raise ValueError(f"Cyclic entity hierarchy detected involving {curr}")
                visited.add(curr)
                ancestors.add(curr)
                curr = self.classes[curr].parent
            self._ancestors[eid] = ancestors

    def __contains__(self, entity_class: str) -> bool:
        return entity_class in self.classes

    def get_ancestors_and_self(self, entity_class: str) -> set[str]:
        if entity_class not in self.classes:
            raise ValueError(f"Unknown entity class: {entity_class}")
        return self._ancestors[entity_class]

    def matches(self, profile_class: str, target_classes: list[str]) -> bool:
        if not target_classes:
            return True
        if profile_class not in self.classes:
            raise ValueError(f"Unknown entity class: {profile_class}")
        ancestors = self._ancestors[profile_class]
        return bool(ancestors & set(target_classes))
