"""Exploration helpers to move the player around the overworld."""
from __future__ import annotations

from medieval_monsters.player.player import Player
from medieval_monsters.world.regions import Region


def travel(player: Player, destination: Region) -> None:
    player.move_to(destination.name)


__all__ = ["travel"]
