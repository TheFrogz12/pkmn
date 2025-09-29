"""Simplified combat scaffolding."""
from __future__ import annotations

from typing import List, Sequence, Tuple

from medieval_monsters.creatures.monster import Monster


def determine_turn_order(combatants: Sequence[Monster]) -> List[Monster]:
    """Sort combatants by agility to decide turn order."""
    return sorted(combatants, key=lambda m: m.agility, reverse=True)


def simulate_attack(attacker: Monster, defender: Monster) -> Tuple[int, bool]:
    """Perform a lightweight attack simulation returning damage and faint status."""
    base_damage = max(1, attacker.attack - defender.defense // 2)
    defender.apply_damage(base_damage)
    return base_damage, defender.is_fainted


def capture_monster(monster: Monster, bonus: float = 0.0) -> float:
    """Proxy to monster capture probability for tests."""
    return monster.capture_probability(bonus)


__all__ = ["determine_turn_order", "simulate_attack", "capture_monster"]
