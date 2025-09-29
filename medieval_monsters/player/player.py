"""Player module containing core player classes and helpers."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from medieval_monsters.creatures.monster import Monster


@dataclass
class InventoryItem:
    """Representation of a stackable item in the player's inventory."""

    name: str
    quantity: int = 0

    def add(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot add a negative amount of items.")
        self.quantity += amount

    def remove(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot remove a negative amount of items.")
        if amount > self.quantity:
            raise ValueError("Not enough items to remove.")
        self.quantity -= amount


@dataclass
class Player:
    """Container for the player's party, inventory and survival vitals."""

    name: str
    party: List[Monster] = field(default_factory=list)
    inventory: Dict[str, InventoryItem] = field(default_factory=dict)
    location: Optional[str] = None
    health: int = 100
    stamina: int = 100
    hunger: int = 0
    morale: int = 70
    exposure: int = 0

    MAX_STAT: int = 100

    def add_to_party(self, monster: Monster) -> None:
        """Append a monster to the player's party if it isn't already present."""
        if monster in self.party:
            return
        self.party.append(monster)

    def remove_from_party(self, monster: Monster) -> None:
        if monster in self.party:
            self.party.remove(monster)

    def add_item(self, name: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        item = self.inventory.setdefault(name, InventoryItem(name))
        item.add(quantity)

    def remove_item(self, name: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        item = self.inventory.get(name)
        if not item:
            raise KeyError(f"{name} not found in inventory")
        item.remove(quantity)
        if item.quantity == 0:
            del self.inventory[name]

    def has_item(self, name: str) -> bool:
        return name in self.inventory and self.inventory[name].quantity > 0

    def active_monster(self) -> Optional[Monster]:
        return self.party[0] if self.party else None

    def apply_survival_tick(self, *, hunger_rate: int = 5, exposure_rate: int = 3, morale_drain: int = 2) -> None:
        """Update the player's survival stats for a single tick of time."""
        self.hunger = min(self.MAX_STAT, self.hunger + hunger_rate)
        self.exposure = min(self.MAX_STAT, self.exposure + exposure_rate)
        self.morale = max(0, self.morale - morale_drain)
        if self.hunger >= self.MAX_STAT:
            self.health = max(0, self.health - 10)
        if self.exposure >= self.MAX_STAT:
            self.stamina = max(0, self.stamina - 10)

    def rest(self) -> None:
        self.stamina = min(self.MAX_STAT, self.stamina + 20)
        self.health = min(self.MAX_STAT, self.health + 10)
        self.hunger = max(0, self.hunger - 15)
        self.exposure = max(0, self.exposure - 20)
        self.morale = min(self.MAX_STAT, self.morale + 10)

    def move_to(self, region_name: str) -> None:
        self.location = region_name
