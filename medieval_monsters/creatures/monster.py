"""Definitions for monsters encountered and captured by the player."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Skill:
    name: str
    element: str
    power: int
    stamina_cost: int = 5


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

    def __post_init__(self) -> None:
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
