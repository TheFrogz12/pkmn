from medieval_monsters.creatures.monster import Monster
from medieval_monsters.data import load_monsters
from medieval_monsters.systems.combat import (
    capture_monster,
    determine_turn_order,
    simulate_attack,
)


def _make_monster(**overrides):
    payload = {
        "name": "Test Beast",
        "element": "fire",
        "level": 3,
        "max_hp": 30,
        "attack": 10,
        "defense": 4,
        "agility": 6,
        "capture_rate": 0.3,
    }
    payload.update(overrides)
    return Monster.from_dict(payload)


def test_turn_order_sorted_by_agility_and_level_breaker():
    monsters = load_monsters()
    order = determine_turn_order(monsters)
    best = max(monsters, key=lambda m: (m.agility, m.level))
    assert order[0].agility >= order[1].agility
    assert order[0].agility >= order[-1].agility
    assert order[0] == best


def test_simulate_attack_uses_elemental_advantage():
    attacker = _make_monster(skills=[{"name": "Flame Bite", "element": "fire", "power": 18}])
    nature_defender = _make_monster(name="Grove Sentinel", element="nature", defense=5)
    water_defender = _make_monster(name="River Watcher", element="water", defense=5)

    damage_vs_nature, _ = simulate_attack(attacker, nature_defender, skill=attacker.skills[0])
    damage_vs_water, _ = simulate_attack(attacker, water_defender, skill=attacker.skills[0])

    assert damage_vs_nature > damage_vs_water
    assert water_defender.current_hp == water_defender.max_hp - damage_vs_water


def test_simulate_attack_and_capture_probability():
    monster = _make_monster()
    defender = _make_monster(name="Dummy", element="earth", max_hp=20, defense=2)
    damage, fainted = simulate_attack(monster, defender)
    assert damage > 0
    assert defender.current_hp == defender.max_hp - damage
    assert fainted == defender.is_fainted

    defender.apply_damage(8)
    chance = capture_monster(defender, bonus=0.1, tool_bonus=0.05)
    assert 0.05 <= chance <= 0.95
    assert chance >= defender.capture_rate
