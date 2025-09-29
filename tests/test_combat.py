from medieval_monsters.creatures.monster import Monster
from medieval_monsters.data import load_monsters
from medieval_monsters.systems.combat import (
    capture_monster,
    determine_turn_order,
    simulate_attack,
)


def test_turn_order_sorted_by_agility():
    monsters = load_monsters()
    slower, faster = sorted(monsters, key=lambda m: m.agility)
    order = determine_turn_order(monsters)
    assert order[0].agility >= order[1].agility
    assert order[0] == faster


def test_simulate_attack_and_capture_probability():
    monster = Monster.from_dict(
        {
            "name": "Test Beast",
            "element": "fire",
            "level": 2,
            "max_hp": 20,
            "attack": 8,
            "defense": 3,
            "agility": 4,
            "capture_rate": 0.3,
        }
    )
    defender = Monster.from_dict(
        {
            "name": "Dummy",
            "element": "water",
            "level": 1,
            "max_hp": 10,
            "attack": 5,
            "defense": 1,
            "agility": 1,
            "capture_rate": 0.1,
        }
    )
    damage, fainted = simulate_attack(monster, defender)
    assert damage > 0
    assert defender.current_hp == defender.max_hp - damage
    assert fainted == defender.is_fainted

    defender.apply_damage(8)
    chance = capture_monster(defender, bonus=0.1)
    assert 0.05 <= chance <= 0.95
    assert chance >= defender.capture_rate
