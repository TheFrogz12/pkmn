"""Exploration helpers to move the player around the overworld."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional

from medieval_monsters.player.player import Player
from medieval_monsters.world.regions import Region


@dataclass
class ExplorationEvent:
    outcome: Literal["calm", "resource", "encounter", "hazard"]
    description: str
    encounter_chance: float
    payload: Optional[Dict[str, Any]] = None


def travel(player: Player, destination: Region, *, rng: Optional[random.Random] = None) -> ExplorationEvent:
    player.move_to(destination.name)
    return roll_event(destination, rng=rng)


def roll_event(region: Region, *, rng: Optional[random.Random] = None) -> ExplorationEvent:
    rng = rng or random.Random()
    encounter_chance = region.get_encounter_chance()
    roll = rng.random()
    if roll < encounter_chance:
        return ExplorationEvent("encounter", "A hostile presence emerges!", encounter_chance)

    resource_threshold = min(1.0, encounter_chance + 0.3)
    hazard_threshold = min(1.0, resource_threshold + 0.2 + region.danger_level * 0.03)

    if roll < resource_threshold:
        if region.biome.has_resources():
            resource = rng.choice(region.biome.resources)
            description = f"You spot fresh {resource} ripe for gathering."
            return ExplorationEvent(
                "resource",
                description,
                encounter_chance,
                payload={"resource": resource},
            )
        return ExplorationEvent("resource", "You scout the area but find little of use.", encounter_chance)

    if roll < hazard_threshold:
        severity = max(1, region.danger_level)
        payload = {
            "health_loss": 2 * severity,
            "stamina_loss": 3 * severity,
            "morale_loss": max(1, severity // 2),
        }
        description = "Perilous terrain batters you as you press onward."
        return ExplorationEvent("hazard", description, encounter_chance, payload=payload)

    return ExplorationEvent("calm", "The journey is uneventful.", encounter_chance)


def resolve_event(
    player: Player,
    region: Region,
    event: ExplorationEvent,
    *,
    rng: Optional[random.Random] = None,
) -> List[str]:
    """Apply the mechanical impact of an exploration event and return notes."""

    rng = rng or random.Random()
    notes: List[str] = []

    if event.outcome == "resource":
        resource = (event.payload or {}).get("resource") if event.payload else None
        if not resource and region.biome.has_resources():
            resource = rng.choice(region.biome.resources)
        if resource:
            player.add_item(resource)
            notes.append(f"You secure {resource} from the wilds.")
    elif event.outcome == "hazard":
        payload = event.payload or {}
        health_loss = int(payload.get("health_loss", max(1, region.danger_level * 2)))
        stamina_loss = int(payload.get("stamina_loss", max(1, region.danger_level * 3 // 2)))
        morale_loss = int(payload.get("morale_loss", max(1, region.danger_level // 2)))

        if health_loss:
            player.health = max(0, player.health - health_loss)
        if stamina_loss:
            player.stamina = max(0, player.stamina - stamina_loss)
        if morale_loss:
            player.morale = max(0, player.morale - morale_loss)

        losses = []
        if health_loss:
            losses.append(f"-{health_loss} health")
        if stamina_loss:
            losses.append(f"-{stamina_loss} stamina")
        if morale_loss:
            losses.append(f"-{morale_loss} morale")
        if losses:
            notes.append(f"Hazards sap your strength ({', '.join(losses)}).")

    return notes


def forage(player: Player, region: Region, *, rng: Optional[random.Random] = None) -> Optional[str]:
    rng = rng or random.Random()
    if not region.biome.has_resources():
        return None
    resource = rng.choice(region.biome.resources)
    player.add_item(resource)
    return resource


__all__ = ["travel", "roll_event", "resolve_event", "forage", "ExplorationEvent"]
