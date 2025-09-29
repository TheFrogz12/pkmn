"""Utility functions for loading game data files."""
from __future__ import annotations

import json
from importlib import resources
from typing import Dict, Iterable, List

from medieval_monsters.creatures.monster import Monster



def _load_json_resource(package: str, name: str) -> Iterable[Dict]:
    with resources.files(package).joinpath(name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_monsters() -> List[Monster]:
    payload = _load_json_resource(__name__, "monsters.json")
    return [Monster.from_dict(entry) for entry in payload]


def load_regions() -> Dict[str, Region]:
    payload = _load_json_resource(__name__, "regions.json")

    for entry in payload:
        region = regions[entry["name"]]
        for direction, neighbor_name in entry.get("neighbors", {}).items():
            neighbor = regions.get(neighbor_name)
            if neighbor:
                region.connect(neighbor, direction)

    return regions


def load_recipes() -> Dict[str, Dict[str, int]]:
    payload = _load_json_resource(__name__, "recipes.json")

