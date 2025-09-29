"""Definitions for monsters encountered and captured by the player."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Coarse elemental effectiveness table used by combat calculations.
ELEMENTAL_EFFECTIVENESS: Dict[str, Dict[str, float]] = {
    "fire": {"nature": 1.25, "water": 0.75},
    "water": {"fire": 1.25, "electric": 0.75},
    "nature": {"earth": 1.15, "fire": 0.75},
    "earth": {"electric": 1.25, "nature": 0.85},
    "electric": {"water": 1.3, "earth": 0.7},
}


def elemental_modifier(attacking_element: Optional[str], defending_element: str) -> float:
    element = attacking_element or "neutral"
    return ELEMENTAL_EFFECTIVENESS.get(element, {}).get(defending_element, 1.0)


@dataclass
class Skill:
    name: str
    element: str
    power: int
    stamina_cost: int = 5

    def effectiveness_against(self, element: str) -> float:
        return elemental_modifier(self.element, element)


@dataclass
class Monster:
    name: str
    element: str
    level: int
    max_hp: int
    attack: int
    defense: int
    agility: int
    capture_rate: float
    skills: List[Skill] = field(default_factory=list)
    lore: str = ""

    current_hp: int = field(init=False)
    experience: int = 0

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.current_hp = self.max_hp

    @property
    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def apply_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int) -> None:
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def capture_probability(self, bonus: float = 0.0) -> float:
        """Compute capture chance using base rate, current health and provided bonus."""
        health_factor = 1.0 - (self.current_hp / max(self.max_hp, 1))
        chance = min(0.95, max(0.05, self.capture_rate + health_factor * 0.5 + bonus))
        return round(chance, 3)

    def choose_skill(self) -> Optional[Skill]:
        if not self.skills:
            return None
        return max(self.skills, key=lambda skill: skill.power)

    def damage_output(self, *, skill: Optional[Skill] = None) -> int:
        base_power = skill.power if skill else self.attack
        return max(1, base_power + self.attack // 2)

    def copy(self) -> "Monster":
        """Create a fresh instance with the same attributes and skills."""
        return Monster(
            name=self.name,
            element=self.element,
            level=self.level,
            max_hp=self.max_hp,
            attack=self.attack,
            defense=self.defense,
            agility=self.agility,
            capture_rate=self.capture_rate,
            skills=[
                Skill(
                    name=skill.name,
                    element=skill.element,
                    power=skill.power,
                    stamina_cost=skill.stamina_cost,
                )
                for skill in self.skills
            ],
            lore=self.lore,
        )

    @classmethod
    def from_dict(cls, data: Dict) -> "Monster":
        skills = [Skill(**skill) for skill in data.get("skills", [])]
        return cls(
            name=data["name"],
            element=data.get("element", "mystic"),
            level=data.get("level", 1),
            max_hp=data.get("max_hp", 20),
            attack=data.get("attack", 5),
            defense=data.get("defense", 5),
            agility=data.get("agility", 5),
            capture_rate=data.get("capture_rate", 0.2),
            skills=skills,
            lore=data.get("lore", ""),
        )


__all__ = ["Monster", "Skill", "ELEMENTAL_EFFECTIVENESS", "elemental_modifier"]
