"""Exploration helpers to move the player around the overworld."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal, Optional

from medieval_monsters.player.player import Player
from medieval_monsters.world.regions import Region


@dataclass
class ExplorationEvent:
    outcome: Literal["calm", "resource", "encounter"]
    description: str
    encounter_chance: float


def travel(player: Player, destination: Region, *, rng: Optional[random.Random] = None) -> ExplorationEvent:
    player.move_to(destination.name)
    return roll_event(destination, rng=rng)


def roll_event(region: Region, *, rng: Optional[random.Random] = None) -> ExplorationEvent:
    rng = rng or random.Random()
    encounter_chance = region.get_encounter_chance()
    roll = rng.random()
    if roll < encounter_chance:
        return ExplorationEvent("encounter", "A hostile presence emerges!", encounter_chance)
    resource_threshold = min(1.0, encounter_chance + 0.25)
    if roll < resource_threshold:
        if region.biome.has_resources():
            resource = rng.choice(region.biome.resources)
            description = f"You spot fresh {resource} ripe for gathering."
        else:
            description = "You scout the area but find little of use."
        return ExplorationEvent("resource", description, encounter_chance)
    return ExplorationEvent("calm", "The journey is uneventful.", encounter_chance)


def forage(player: Player, region: Region, *, rng: Optional[random.Random] = None) -> Optional[str]:
    rng = rng or random.Random()
    if not region.biome.has_resources():
        return None
    resource = rng.choice(region.biome.resources)
    player.add_item(resource)
    return resource


__all__ = ["travel", "roll_event", "forage", "ExplorationEvent"]
