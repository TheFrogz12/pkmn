"""Basic survival system helpers."""
from __future__ import annotations



from medieval_monsters.player.player import Player
from medieval_monsters.world.regions import Region



    for _ in range(hours):
        hunger_rate = 4 + region.danger_level
        exposure_rate = 2 + int(region.danger_level / 2)
        morale_drain = max(1, region.danger_level - 1)
        player.apply_survival_tick(
            hunger_rate=hunger_rate,
            exposure_rate=exposure_rate,
            morale_drain=morale_drain,
        )



__all__ = ["apply_survival_tick"]
