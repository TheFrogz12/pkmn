"""Simplified combat scaffolding."""
from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from medieval_monsters.creatures.monster import Monster, Skill, elemental_modifier


def determine_turn_order(combatants: Sequence[Monster]) -> List[Monster]:
    """Sort combatants by agility to decide turn order."""
    return sorted(combatants, key=lambda m: (m.agility, m.level), reverse=True)


def _calculate_damage(attacker: Monster, defender: Monster, skill: Optional[Skill]) -> int:
    base_damage = attacker.damage_output(skill=skill)
    element = skill.element if skill else attacker.element
    modifier = elemental_modifier(element, defender.element)
    mitigated = int(round(base_damage * modifier - defender.defense * 0.3))
    return max(1, mitigated)


def simulate_attack(attacker: Monster, defender: Monster, *, skill: Optional[Skill] = None) -> Tuple[int, bool]:
    """Perform a lightweight attack simulation returning damage and faint status."""
    chosen_skill = skill or attacker.choose_skill()
    damage = _calculate_damage(attacker, defender, chosen_skill)
    defender.apply_damage(damage)
    return damage, defender.is_fainted


def capture_monster(monster: Monster, bonus: float = 0.0, tool_bonus: float = 0.0) -> float:
    """Proxy to monster capture probability including optional tool modifiers."""
    return monster.capture_probability(bonus + tool_bonus)


__all__ = [
    "determine_turn_order",
    "simulate_attack",
    "capture_monster",
]
