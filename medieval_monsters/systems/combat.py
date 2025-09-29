"""Combat helpers for automated encounter resolution."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple, Literal

from medieval_monsters.creatures.monster import Monster, Skill, elemental_modifier


@dataclass
class CombatLogEntry:
    """Record a single action that occurred during an encounter."""

    event: Literal["attack", "capture"]
    actor: str
    target: str
    skill: Optional[str] = None
    damage: int = 0
    remaining_hp: int = 0
    fainted: bool = False
    success: Optional[bool] = None
    chance: Optional[float] = None


@dataclass
class CombatResult:
    """Aggregate the outcome of an automated combat sequence."""

    log: List[CombatLogEntry] = field(default_factory=list)
    winner: Optional[str] = None
    rounds: int = 0
    capture_attempted: bool = False
    captured: bool = False


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


def run_auto_battle(
    player_monster: Monster,
    wild_monster: Monster,
    *,
    rng: Optional[random.Random] = None,
    capture_threshold: float = 0.35,
    capture_bonus: float = 0.0,
    tool_bonus: float = 0.0,
) -> CombatResult:
    """Resolve an automated battle returning a combat log and winner.

    The player's monster will attempt a capture once the wild opponent falls below
    the provided health ratio threshold. A failed capture leads to a regular
    attack during the same turn to keep the encounter flowing.
    """

    rng = rng or random.Random()
    log: List[CombatLogEntry] = []
    rounds = 0
    capture_attempted = False
    captured = False

    while not player_monster.is_fainted and not wild_monster.is_fainted:
        rounds += 1
        for attacker in determine_turn_order((player_monster, wild_monster)):
            defender = wild_monster if attacker is player_monster else player_monster

            if defender.is_fainted:
                break

            if (
                attacker is player_monster
                and not capture_attempted
                and wild_monster.max_hp > 0
                and wild_monster.current_hp / wild_monster.max_hp <= capture_threshold
            ):
                capture_attempted = True
                chance = capture_monster(wild_monster, bonus=capture_bonus, tool_bonus=tool_bonus)
                success = rng.random() < chance
                log.append(
                    CombatLogEntry(
                        event="capture",
                        actor=player_monster.name,
                        target=wild_monster.name,
                        remaining_hp=wild_monster.current_hp,
                        success=success,
                        chance=chance,
                    )
                )
                if success:
                    captured = True
                    return CombatResult(
                        log=log,
                        winner=player_monster.name,
                        rounds=rounds,
                        capture_attempted=True,
                        captured=True,
                    )

            skill = attacker.choose_skill()
            damage, fainted = simulate_attack(attacker, defender, skill=skill)
            log.append(
                CombatLogEntry(
                    event="attack",
                    actor=attacker.name,
                    target=defender.name,
                    skill=skill.name if skill else None,
                    damage=damage,
                    remaining_hp=defender.current_hp,
                    fainted=fainted,
                )
            )

            if defender.is_fainted:
                return CombatResult(
                    log=log,
                    winner=attacker.name,
                    rounds=rounds,
                    capture_attempted=capture_attempted,
                    captured=captured,
                )

    return CombatResult(
        log=log,
        winner=None,
        rounds=rounds,
        capture_attempted=capture_attempted,
        captured=captured,
    )


__all__ = [
    "determine_turn_order",
    "simulate_attack",
    "capture_monster",
    "run_auto_battle",
    "CombatLogEntry",
    "CombatResult",
]
