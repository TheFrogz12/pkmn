"""Utility functions for loading game data files."""
from __future__ import annotations

import json
from importlib import resources
from typing import Dict, Iterable, List

from medieval_monsters.creatures.monster import Monster
from medieval_monsters.world.regions import Biome, Region


def _load_json_resource(package: str, name: str) -> Iterable[Dict]:
    with resources.files(package).joinpath(name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_monsters() -> List[Monster]:
    payload = _load_json_resource(__name__, "monsters.json")
    return [Monster.from_dict(entry) for entry in payload]


def load_regions() -> Dict[str, Region]:
    payload = _load_json_resource(__name__, "regions.json")
    regions: Dict[str, Region] = {}

    # First pass create regions
    for entry in payload:
        biome_data = entry["biome"]
        biome = Biome(
            name=biome_data["name"],
            climate=biome_data["climate"],
            resources=biome_data.get("resources", []),
            encounter_rate=biome_data.get("encounter_rate", 0.1),
        )
        region = Region(
            name=entry["name"],
            biome=biome,
            danger_level=entry.get("danger_level", 1),
            description=entry.get("description", ""),
            points_of_interest=entry.get("points_of_interest", []),
        )
        regions[region.name] = region

    # Second pass to link neighbors
    for entry in payload:
        region = regions[entry["name"]]
        for direction, neighbor_name in entry.get("neighbors", {}).items():
            neighbor = regions.get(neighbor_name)
            if neighbor:
                region.connect(neighbor, direction)

    return regions


def load_recipes() -> Dict[str, Dict[str, int]]:
    payload = _load_json_resource(__name__, "recipes.json")
    return {entry["name"]: entry["ingredients"] for entry in payload}
