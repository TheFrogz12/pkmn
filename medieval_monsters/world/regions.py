"""Regional definitions and biome descriptors."""
from __future__ import annotations

from dataclasses import dataclass, field



@dataclass
class Biome:

    name: str
    climate: str
    resources: List[str]
    encounter_rate: float


    name: str
    biome: Biome
    danger_level: int
    description: str
    neighbors: Dict[str, "Region"] = field(default_factory=dict)
    points_of_interest: List[str] = field(default_factory=list)



    def get_encounter_chance(self) -> float:
        return min(1.0, self.biome.encounter_rate * (1 + self.danger_level / 10))

    def describe(self) -> str:
        poi = ", ".join(self.points_of_interest) if self.points_of_interest else "None"

        return (
            f"Region: {self.name}\n"
            f"Biome: {self.biome.name} ({self.biome.climate})\n"
            f"Danger Level: {self.danger_level}\n"

