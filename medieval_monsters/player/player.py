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
    MAX_PARTY_SIZE: int = 4

    def add_to_party(self, monster: Monster) -> None:
        """Append a monster to the player's party if room is available."""
        if monster in self.party:
            return
        if len(self.party) >= self.MAX_PARTY_SIZE:
            raise ValueError("Party is full.")
        self.party.append(monster)

    def remove_from_party(self, monster: Monster) -> None:
        if monster in self.party:
            self.party.remove(monster)

    def cycle_active_monster(self, index: int) -> Monster:
        if not self.party:
            raise ValueError("No monsters in the party.")
        if index < 0 or index >= len(self.party):
            raise IndexError("Party index out of range.")
        monster = self.party.pop(index)
        self.party.insert(0, monster)
        return monster

    def available_party_slots(self) -> int:
        return max(0, self.MAX_PARTY_SIZE - len(self.party))

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

    def consume_item(self, name: str, quantity: int = 1) -> bool:
        try:
            self.remove_item(name, quantity)
        except (KeyError, ValueError):
            return False
        return True

    def get_item_quantity(self, name: str) -> int:
        item = self.inventory.get(name)
        return item.quantity if item else 0

    def inventory_summary(self) -> List[str]:
        if not self.inventory:
            return ["(empty)"]
        return [f"{item.name}: {item.quantity}" for item in self.inventory.values()]

    def has_item(self, name: str) -> bool:
        return self.get_item_quantity(name) > 0

    def active_monster(self) -> Optional[Monster]:
        return self.party[0] if self.party else None

    def apply_survival_tick(
        self,
        *,
        hunger_rate: int = 5,
        exposure_rate: int = 3,
        morale_drain: int = 2,
    ) -> Dict[str, int]:
        """Update the player's survival stats for a single tick of time."""
        before = {
            "health": self.health,
            "stamina": self.stamina,
            "hunger": self.hunger,
            "morale": self.morale,
            "exposure": self.exposure,
        }
        self.hunger = min(self.MAX_STAT, self.hunger + hunger_rate)
        self.exposure = min(self.MAX_STAT, self.exposure + exposure_rate)
        self.morale = max(0, self.morale - morale_drain)
        if self.hunger >= self.MAX_STAT:
            self.health = max(0, self.health - 10)
        if self.exposure >= self.MAX_STAT:
            self.stamina = max(0, self.stamina - 10)
        return before

    def rest(self, *, full: bool = False) -> None:
        stamina_gain = 40 if full else 20
        health_gain = 20 if full else 10
        hunger_drop = 30 if full else 15
        exposure_drop = 35 if full else 20
        morale_gain = 20 if full else 10

        self.stamina = min(self.MAX_STAT, self.stamina + stamina_gain)
        self.health = min(self.MAX_STAT, self.health + health_gain)
        self.hunger = max(0, self.hunger - hunger_drop)
        self.exposure = max(0, self.exposure - exposure_drop)
        self.morale = min(self.MAX_STAT, self.morale + morale_gain)

    def status_report(self) -> str:
        return (
            f"Health: {self.health}/{self.MAX_STAT} | Stamina: {self.stamina}/{self.MAX_STAT}\n"
            f"Hunger: {self.hunger}/{self.MAX_STAT} | Exposure: {self.exposure}/{self.MAX_STAT} | Morale: {self.morale}/{self.MAX_STAT}"
        )

    def move_to(self, region_name: str) -> None:
        self.location = region_name
