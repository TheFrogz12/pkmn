"""Regional definitions and biome descriptors."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List

# Canonical opposites for quickly wiring bidirectional paths between regions.
OPPOSITE_DIRECTIONS: Dict[str, str] = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
    "northeast": "southwest",
    "southwest": "northeast",
    "northwest": "southeast",
    "southeast": "northwest",
    "up": "down",
    "down": "up",
}


@dataclass
class Biome:
    """Lightweight data container describing a biome's feel and rewards."""

    name: str
    climate: str
    resources: List[str]
    encounter_rate: float

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Biome":
        """Create a biome from serialized data, normalising optional fields."""
        resources = list(payload.get("resources", []))
        encounter_rate = float(payload.get("encounter_rate", 0.1))
        return cls(
            name=payload["name"],
            climate=payload.get("climate", "temperate"),
            resources=resources,
            encounter_rate=encounter_rate,
        )

    def has_resources(self) -> bool:
        return bool(self.resources)


@dataclass
class Region:
    """A traversable chunk of the overworld linked to neighbouring regions."""

    name: str
    biome: Biome
    danger_level: int
    description: str
    neighbors: Dict[str, "Region"] = field(default_factory=dict)
    points_of_interest: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Region":
        biome = Biome.from_dict(payload["biome"])
        return cls(
            name=payload["name"],
            biome=biome,
            danger_level=int(payload.get("danger_level", 1)),
            description=payload.get("description", ""),
            points_of_interest=list(payload.get("points_of_interest", [])),
        )

    def connect(self, other: "Region", direction: str, *, bidirectional: bool = True) -> None:
        """Connect this region to another, optionally mirroring the connection."""
        direction_key = direction.lower()
        if direction_key not in self.neighbors:
            self.neighbors[direction_key] = other
        if bidirectional:
            reverse = OPPOSITE_DIRECTIONS.get(direction_key)
            if reverse and (reverse not in other.neighbors or other.neighbors[reverse] is not self):
                other.connect(self, reverse, bidirectional=False)

    def available_directions(self) -> List[str]:
        return sorted(self.neighbors.keys())

    def neighbor_names(self) -> Iterable[str]:
        for direction in self.available_directions():
            yield f"{direction}: {self.neighbors[direction].name}"

    def get_encounter_chance(self) -> float:
        return min(1.0, self.biome.encounter_rate * (1 + self.danger_level / 10))

    def describe(self) -> str:
        poi = ", ".join(self.points_of_interest) if self.points_of_interest else "None"
        neighbor_summary = ", ".join(self.neighbor_names()) or "None"
        resources = ", ".join(self.biome.resources) if self.biome.resources else "None"
        return (
            f"Region: {self.name}\n"
            f"Biome: {self.biome.name} ({self.biome.climate})\n"
            f"Danger Level: {self.danger_level}\n"
            f"Resources: {resources}\n"
            f"Points of Interest: {poi}\n"
            f"Neighbors: {neighbor_summary}"
        )


__all__ = ["Biome", "Region", "OPPOSITE_DIRECTIONS"]
