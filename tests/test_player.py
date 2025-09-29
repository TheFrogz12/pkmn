import pytest

from medieval_monsters.creatures.monster import Monster
from medieval_monsters.player.player import Player


def _make_monster(name: str, element: str = "fire", level: int = 1) -> Monster:
    return Monster.from_dict(
        {
            "name": name,
            "element": element,
            "level": level,
            "max_hp": 20 + level,
            "attack": 5 + level,
            "defense": 3 + level,
            "agility": 4 + level,
            "capture_rate": 0.2,
        }
    )


def test_party_management_enforces_capacity_and_cycle():
    player = Player(name="Handler")
    monsters = [_make_monster(f"Beast {idx}") for idx in range(1, player.MAX_PARTY_SIZE + 1)]
    for monster in monsters:
        player.add_to_party(monster)

    assert player.available_party_slots() == 0
    with pytest.raises(ValueError):
        player.add_to_party(_make_monster("Extra Beast"))

    chosen = player.cycle_active_monster(2)
    assert chosen == player.active_monster()


def test_inventory_helpers_report_and_consume_items():
    player = Player(name="Trader")
    assert player.inventory_summary() == ["(empty)"]

    player.add_item("herbs", 2)
    assert player.has_item("herbs")
    assert player.get_item_quantity("herbs") == 2

    consumed = player.consume_item("herbs")
    assert consumed is True
    assert player.get_item_quantity("herbs") == 1

    summary = player.inventory_summary()
    assert any(entry.startswith("herbs") for entry in summary)

    consumed_missing = player.consume_item("timber")
    assert consumed_missing is False
