"""Regional definitions and biome descriptors."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Biome:
    name: str
    climate: str
    resources: List[str]
    encounter_rate: float


@dataclass
class Region:
    name: str
    biome: Biome
    danger_level: int
    description: str
    neighbors: Dict[str, "Region"] = field(default_factory=dict)
    points_of_interest: List[str] = field(default_factory=list)

    def connect(self, other: "Region", direction: str) -> None:
        self.neighbors[direction] = other

    def available_directions(self) -> List[str]:
        return list(self.neighbors.keys())

    def get_encounter_chance(self) -> float:
        return min(1.0, self.biome.encounter_rate * (1 + self.danger_level / 10))

    def describe(self) -> str:
        poi = ", ".join(self.points_of_interest) if self.points_of_interest else "None"
        return (
            f"Region: {self.name}\n"
            f"Biome: {self.biome.name} ({self.biome.climate})\n"
            f"Danger Level: {self.danger_level}\n"
            f"Resources: {', '.join(self.biome.resources)}\n"
            f"Points of Interest: {poi}"
        )
