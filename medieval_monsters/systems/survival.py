"""Basic survival system helpers."""
from __future__ import annotations

from typing import List

from medieval_monsters.player.player import Player
from medieval_monsters.world.regions import Region


def apply_survival_tick(
    player: Player,
    region: Region,
    hours: int = 1,
    *,
    auto_consume_rations: bool = True,
    ration_item: str = "Trail Rations",
) -> List[str]:
    """Advance survival stats based on region danger and elapsed hours."""
    events: List[str] = []
    for _ in range(hours):
        hunger_rate = 4 + region.danger_level
        exposure_rate = 2 + int(region.danger_level / 2)
        morale_drain = max(1, region.danger_level - 1)
        player.apply_survival_tick(
            hunger_rate=hunger_rate,
            exposure_rate=exposure_rate,
            morale_drain=morale_drain,
        )
        if auto_consume_rations and player.hunger >= 70 and player.consume_item(ration_item):
            player.hunger = max(0, player.hunger - 35)
            player.morale = min(player.MAX_STAT, player.morale + 5)
            events.append(f"Consumed {ration_item} to keep hunger at bay.")
    return events


__all__ = ["apply_survival_tick"]
