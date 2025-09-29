from medieval_monsters.creatures.monster import Monster
from medieval_monsters.data import load_monsters
from medieval_monsters.systems.combat import (
    CombatLogEntry,
    capture_monster,
    determine_turn_order,
    run_auto_battle,
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


class SequenceRandom:
    def __init__(self, rolls):
        self._rolls = iter(rolls)

    def random(self):
        return next(self._rolls, 0.0)


def test_auto_battle_attempts_capture_and_succeeds():
    player = _make_monster(
        name="Warden",
        attack=15,
        agility=9,
        skills=[{"name": "Blazing Edge", "element": "fire", "power": 18}],
    )
    foe = _make_monster(name="Fen Stalker", max_hp=18, defense=2, agility=6, capture_rate=0.35)

    rng = SequenceRandom([0.1])
    result = run_auto_battle(player, foe, rng=rng, capture_threshold=1.0, capture_bonus=0.15)

    assert result.captured is True
    assert result.capture_attempted is True
    assert result.winner == player.name
    assert any(entry.event == "capture" and entry.success for entry in result.log)


def test_auto_battle_logs_attacks_when_capture_fails():
    player = _make_monster(
        name="Champion",
        attack=20,
        agility=8,
        skills=[{"name": "Solar Strike", "element": "fire", "power": 22}],
    )
    foe = _make_monster(name="Wildling", max_hp=16, defense=3, agility=5)

    rng = SequenceRandom([0.99])
    result = run_auto_battle(player, foe, rng=rng, capture_threshold=1.0)

    assert result.captured is False
    assert result.capture_attempted is True
    assert result.winner == player.name

    attack_entries = [entry for entry in result.log if entry.event == "attack"]
    assert attack_entries
    assert foe.is_fainted
    assert all(isinstance(entry, CombatLogEntry) for entry in result.log)
